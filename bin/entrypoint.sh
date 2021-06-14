#!/bin/bash
# set -euo pipefail
set -e

if [ $# -eq 0 ]
  then
    echo "
No arguments passed
Usage: bash entrypoint.sh [..]

Options:
--wait wait for db
--migrate migrate db
--test  run tests
--dev   run dev server
--prod  run prod server (gunicorn)
"
    exit 0
fi


while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    --wait)
    WAIT=1
    shift
    ;;
    --test)
    TEST=1
    shift
    ;;
    --dev)
    DEV=1
    shift
    ;;
    --prod)
    PROD=1
    shift
    ;;
    --migrate)
    MIGRATE_DB=1
    shift
    ;;
    *)
    shift
    ;;
esac
done

if [ -n "${WAIT}" ]
then 
    CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    ${CURR_DIR}/wait-for-it.sh -t 0 ${POSTGRES_SERVICE_HOST}:5432
fi

if [ -n "${MIGRATE_DB}" ]
then
    python manage.py makemigrations
    python manage.py migrate
fi

if [ -n "${TEST}" ]
then
    pytest -p no:cacheprovider
fi

if [ -n "${DEV}" ]
then
    python manage.py runserver 0.0.0.0:8000
fi
if [ -n "${PROD}" ]
then
    python manage.py collectstatic --no-input --clear
    gunicorn -b :8000 huspy.wsgi:application
fi