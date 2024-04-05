echo " BUILD START"
pip uninstall django
python3.12 -m pip install -r requirements.txt
echo "Make Migration..."
python3.12 manage.py makemigrations --noinput
python3.12 manage.py migrate --noinput
python3.12 manage.py collectstatic --noinput --clear
echo " BUILD END"