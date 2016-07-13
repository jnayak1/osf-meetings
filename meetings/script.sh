#!/bin/bash


conf=$1

rm -rf db.sqlite
rm api/migrations/0*
./manage.py makemigrations
./manage.py migrate
if [[ -n "$conf" ]]; then
	./manage.py loadtestdata conferences.Conference:${conf}
else 
	echo "creating empty database"
fi
./manage.py runserver
