#!/bin/sh
set -e
echo "starting django app"

if [ -z "$DJANGO_SUPERUSER_USERNAME" ] || [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "app failed to start, pass -e SUPERUSER_USERNAME=<username>"
  echo "pass -e DJANGO_SUPERUSER_USERNAME=<username>"
  echo "And -e DJANGO_SUPERUSER_PASSWORD=<password>"
  exit 1
fi

touch "$DB_FILE"

python manage.py migrate
python manage.py create_groups
python manage.py createsuperuser --no-input || true

exec "$@"