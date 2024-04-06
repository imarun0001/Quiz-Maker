echo " BUILD START"
pip3 install -r requirements.txt
echo "Make Migration..."
python3.10 manage.py makemigrations --noinput
python3.10 manage.py migrate --noinput
python3.10 manage.py collectstatic --noinput --clear
echo " BUILD END"