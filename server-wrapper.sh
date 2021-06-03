#!/bin/sh

source ../p/bin/activate

while [ true ]; do
	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py runserver
	sleep 2
done
