#!/usr/bin/env bash
# build_files.sh
echo " BUILD START"
pip --upgrade install -r requirements.txt
echo "Make Migration..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput --clear
echo " BUILD END"