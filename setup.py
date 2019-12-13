import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'rb') as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-crud-app',
    version='0.1.0',
    packages=find_packages(exclude=('django_crud_app',)),
    tall_requires=['django', ],
    include_package_data=True,
    license='MIT License',
    description='Easy start crud app',
    long_description=README.decode(),
    url='https://github.com/YutaUra/django_crud_app',
    author='Yuta Ura',
    author_email='yuuta3594@outlook.jp',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Japanese',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
