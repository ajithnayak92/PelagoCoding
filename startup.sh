#!/usr/bin/bash
echo "Checking python version"
python --verison
echo "Creating virtual env"
pip install virtual_env
virtualenv -p python p3
source p3/bin/activate
python manage.py runserver