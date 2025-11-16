#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler