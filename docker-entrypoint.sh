#!/bin/bash

# Exit on error
set -e

echo "Activating virtual environment..."
source .venv/bin/activate

# Coletar arquivos estáticos (WhiteNoise vai comprimir e adicionar hash)
RUN uv run manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser if needed..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@grupi.pavops.net').exists():
    User.objects.create_superuser(
        email='admin@grupi.pavops.net',
        password='changeme123',
        first_name='Admin',
        last_name='GruPI'
    )
    print('Superuser created successfully')
else:
    print('Superuser already exists')
END

echo "Run settings debug command..."
python manage.py check_settings


echo "\n Importing polos..."
python manage.py import_polos

echo "Starting Gunicorn..."
exec gunicorn GruPI.wsgi:application \
    --bind 0.0.0.0:3000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
