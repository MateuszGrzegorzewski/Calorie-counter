#!/bin/sh

flask db upgrade

exec gunicorn --bind 0.0.0.0:80 "main:create_app()"