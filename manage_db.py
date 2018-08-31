"""
Script to instantiate the tools to run alemic migrations
"""
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from webapp import app, db


app.config.from_object(os.environ['APP_SETTINGS'])

MIGRATE = Migrate(app, db)
MANAGER = Manager(app)

MANAGER.add_command('db', MigrateCommand)

if __name__ == '__main__':
    MANAGER.run()
