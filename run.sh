#!/bin/sh
uwsgi --http :9090 --wsgi-file app.py
