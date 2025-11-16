#!/bin/bash

set -o errexit
set -o nounset

celery -A config worker --loglevel=info