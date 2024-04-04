echo " BUILD START"
py -m pip install -r requirements.txt
echo "Make Migration..."
py manage.py makemigrations --noinput
py manage.py migrate --noinput
py manage.py collectstatic --noinput --clear
echo " BUILD END"

