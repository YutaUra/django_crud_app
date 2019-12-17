import re

from crud.management.templates import MyTemplateCommand


class Command(MyTemplateCommand):
    help = (
        "Creates a Django CRUD app directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide an application name."

    def handle(self, **options):
        app_name = options.pop('name')
        options.update({
            'files': [],
            'template': None,
            'app_name': app_name,
            'snake_case_model_name': re.sub(
                '([^A-Z][A-Z])',
                lambda x: x.group(1)[0] + "_" + x.group(1)[1],
                options['model_name']).lower()
        })
        if options['auth_user']:
            app_or_project = 'user'
        elif app_name.lower() in ('user', 'users'):
            while True:
                ans = input('Is this for AUTH_USER_MODEL? [y/n]').lower()
                if not ans or ans not in ('y', 'yes', 'n', 'no'):
                    print('Try to answer')
                    continue
                if ans in ('y', 'yes'):
                    app_or_project = 'user'
                else:
                    app_or_project = 'app'
                break
        else:
            app_or_project = 'app'
        return super().handle(app_or_project, app_name, **options)
