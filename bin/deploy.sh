#!/bin/sh
set -e
cd "$(dirname "$0")"/..
if [ -z "$MONOCHROMECAST_HOST" ]; then
    echo "MONOCHROMECAST_HOST not set"
    exit 1
fi
rsync -avz . "$MONOCHROMECAST_HOST":MonochromeCast/ --exclude .git --exclude-from .gitignore --delete
ssh "$MONOCHROMECAST_HOST" 'pkill -HUP gunicorn'
