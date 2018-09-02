#!/bin/sh
python manage_db.py db init || true
python manage_db.py db upgrade
python ensure_admin.py
python zcrm_config.py https://parseleads.herokuapp.com/oauth2callback