#!/bin/sh
cd "$(dirname "$0")"/..
./hardware/start-hw-server
tmux new-session -d -s gunicorn "authbind gunicorn3 -b 0.0.0.0:80 web:app"
