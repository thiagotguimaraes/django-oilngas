find ./main/wells/migrations -name "*.py" -not -name "__init__.py" -delete
find ./main/wells/migrations -name "*.pyc" -delete
find ./main/datasets/migrations -name "*.py" -not -name "__init__.py" -delete
find ./main/datasets/migrations -name "*.pyc" -delete

docker-compose down -v
docker-compose up -d
sleep 5

source venv/bin/activate

python manage.py makemigrations wells
python manage.py makemigrations datasets
python manage.py migrate
