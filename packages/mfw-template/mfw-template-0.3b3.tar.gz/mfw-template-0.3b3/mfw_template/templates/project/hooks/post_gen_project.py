import shutil
import os

project_name = '{{ cookiecutter.project_name }}'
project_type = '{{ cookiecutter.project_type }}'

if project_type != 'morpcc':
    shutil.rmtree('%s/templates' % project_name)
    shutil.rmtree('%s/static_files' % project_name)
    os.unlink('%s/static.py' % project_name)
