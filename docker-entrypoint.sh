#!/bin/sh

set -e

flask db upgrade

gunicorn -c gunicorn.config.py wsgi:transfer_flask
