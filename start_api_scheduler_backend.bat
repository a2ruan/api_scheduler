title api_scheduler_backend_server

pushd %~dp0
cd api_scheduler_backend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
popd