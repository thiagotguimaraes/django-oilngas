find wells/migrations -name "*.py" -not -name "__init__.py" -delete
find wells/migrations -name "*.pyc" -delete

docker-compose down -v
docker-compose up -d
sleep 10

python manage.py makemigrations wells
python manage.py migrate
