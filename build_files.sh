echo " BUILD START"
pip install -r requirements.txt
echo "Make Migration..."
manage.py makemigrations --noinput
manage.py migrate --noinput
manage.py collectstatic --noinput --clear
echo " BUILD END"

