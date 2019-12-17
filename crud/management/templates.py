import os
import re
import shutil

import django
from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand
from django.core.management.utils import handle_extensions
from django.template import Context, Engine

import crud
import argparse


class ModelNameAction(argparse.Action):
    # adapted from documentation
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        default_model_name = getattr(namespace, 'model_name')
        if default_model_name:
            model_name = default_model_name.title().replace('_', '')
        else:
            app_name = getattr(namespace, 'name')
            model_name = app_name.title().replace('_', '')
        setattr(namespace, 'model_name', model_name)


class MyTemplateCommand(TemplateCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'name',
            action=ModelNameAction,
            help='Name of the application or project.',
        )
        parser.add_argument(
            '--model-name',
            action=ModelNameAction,
            help='Name of the Model. default:camel case of app name.',
            default=''
        )
        parser.add_argument(
            '--auth-user',
            help='if auth user is True, this model is made for AUTH_USER_MODEL',
            default=False,
            type=bool,
        )
        parser.add_argument(
            '--extension', '-e', dest='extensions',
            action='append', default=['py'],
            help='The file extension(s) to render (default: "py"). '
                 'Separate multiple extensions with commas, or use '
                 '-e multiple times.'
        )

    def handle(self, app_or_project, name, **options):
        self.app_or_project = app_or_project
        self.a_or_an = 'an' if app_or_project == 'app' else 'a'
        self.paths_to_remove = []
        self.verbosity = options['verbosity']

        self.validate_name(name)

        # if some directory is given, make sure it's nicely expanded
        top_dir = os.path.join(os.getcwd(), name)
        try:
            os.makedirs(top_dir)
        except FileExistsError:
            raise CommandError("'%s' already exists" % top_dir)
        except OSError as e:
            raise CommandError(e)

        extensions = tuple(handle_extensions(options['extensions']))
        extra_files = []
        for file in options['files']:
            extra_files.extend(map(lambda x: x.strip(), file.split(',')))
        if self.verbosity >= 2:
            self.stdout.write("Rendering %s template files with "
                              "extensions: %s\n" %
                              (app_or_project, ', '.join(extensions)))
            self.stdout.write("Rendering %s template files with "
                              "filenames: %s\n" %
                              (app_or_project, ', '.join(extra_files)))

        base_name = '%s_name' % app_or_project
        base_subdir = '%s_template' % app_or_project
        base_directory = '%s_directory' % app_or_project
        camel_case_name = 'camel_case_%s_name' % app_or_project
        camel_case_value = ''.join(x for x in name.title() if x != '_')

        context = Context({
            **options,
            base_name: name,
            base_directory: top_dir,
            camel_case_name: camel_case_value,
        }, autoescape=False)

        # Setup a stub settings environment for template rendering
        if not settings.configured:
            settings.configure()
            django.setup()

        template_dir = self.handle_template(options['template'],
                                            base_subdir)
        prefix_length = len(template_dir) + 1

        for root, dirs, files in os.walk(template_dir):

            path_rest = root[prefix_length:]
            relative_dir = path_rest.replace(base_name, name)
            if relative_dir:
                target_dir = os.path.join(top_dir, relative_dir)
                os.makedirs(target_dir, exist_ok=True)

            for dirname in dirs[:]:
                if dirname.startswith('.') or dirname == '__pycache__':
                    dirs.remove(dirname)

            for filename in files:
                if filename.endswith(('.pyo', '.pyc', '.py.class')):
                    # Ignore some files as they cause various breakages.
                    continue
                old_path = os.path.join(root, filename)
                new_path = os.path.join(
                    top_dir, relative_dir,
                    filename.replace(base_name, name).replace(
                        'snake_case_model_name', options['snake_case_model_name']
                    ))
                for old_suffix, new_suffix in self.rewrite_template_suffixes:
                    if new_path.endswith(old_suffix):
                        new_path = new_path[:-len(old_suffix)] + new_suffix
                        break  # Only rewrite once

                if os.path.exists(new_path):
                    raise CommandError(
                        "%s already exists. Overlaying %s %s into an existing "
                        "directory won't replace conflicting files." % (
                            new_path, self.a_or_an, app_or_project,
                        )
                    )

                # Only render the Python files, as we don't want to
                # accidentally render Django templates files
                if new_path.endswith(extensions) or filename in extra_files:
                    with open(old_path, encoding='utf-8') as template_file:
                        content = template_file.read()
                    template = Engine().from_string(content)
                    content = template.render(context)
                    with open(new_path, 'w', encoding='utf-8') as new_file:
                        new_file.write(content)
                elif new_path.endswith('html'):
                    with open(old_path, encoding='utf-8') as html_file:
                        content = html_file.read()
                    for key, value in context.dicts[1].items():
                        if key.endswith('_directory'):
                            continue
                        content = re.sub(r'{{\s*' + str(key) + r'\s*}}', str(value), content)
                    with open(new_path, 'w', encoding='utf-8') as new_file:
                        new_file.write(content)
                else:
                    shutil.copyfile(old_path, new_path)

                if self.verbosity >= 2:
                    self.stdout.write("Creating %s\n" % new_path)
                try:
                    shutil.copymode(old_path, new_path)
                    self.make_writeable(new_path)
                except OSError:
                    self.stderr.write(
                        "Notice: Couldn't set permission bits on %s. You're "
                        "probably using an uncommon filesystem setup. No "
                        "problem." % new_path, self.style.NOTICE)

        if self.paths_to_remove:
            if self.verbosity >= 2:
                self.stdout.write("Cleaning up temporary files.\n")
            for path_to_remove in self.paths_to_remove:
                if os.path.isfile(path_to_remove):
                    os.remove(path_to_remove)
                else:
                    shutil.rmtree(path_to_remove)

    def handle_template(self, template, subdir):
        """
        Determine where the app or project templates are.
        Use django.__path__[0] as the default because the Django install
        directory isn't known.
        """
        if template is None:
            return os.path.join(crud.__path__[0], subdir)
        else:
            if template.startswith('file://'):
                template = template[7:]
            expanded_template = os.path.expanduser(template)
            expanded_template = os.path.normpath(expanded_template)
            if os.path.isdir(expanded_template):
                return expanded_template
            if self.is_url(template):
                # downloads the file and returns the path
                absolute_path = self.download(template)
            else:
                absolute_path = os.path.abspath(expanded_template)
            if os.path.exists(absolute_path):
                return self.extract(absolute_path)

        raise CommandError("couldn't handle %s template %s." %
                           (self.app_or_project, template))
