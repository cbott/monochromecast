#!/bin/sh
cd "$(dirname "$0")"/..
./hardware/start-hw-server
tmux new-session -d -s gunicorn "gunicorn3 -b 0.0.0.0:8000 web:app"
