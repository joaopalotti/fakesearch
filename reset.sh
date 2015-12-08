rm db.sqlite3 ; rm fakesearch/migrations/*
python manage.py makemigrations fakesearch; python manage.py migrate
python manage.py createsuperuser
