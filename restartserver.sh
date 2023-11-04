#!/bin/bash

. setenv.sh

python manage.py collectstatic --no-input

sudo systemctl restart aocid
sudo systemctl restart nginx

