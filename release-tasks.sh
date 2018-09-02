#!/bin/sh
python manage_db.py db init || true
python manage_db.py db upgrade
python ensure_admin.py
python zcrm_config.py $HEROKU_APP_NAME/oauth2callback