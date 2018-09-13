import os

from flask import Flask, url_for
from werkzeug.contrib.fixers import ProxyFix
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_security import Security, SQLAlchemyUserDatastore
from flask_dance.contrib.zoho import make_zoho_blueprint

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.wsgi_app = ProxyFix(app.wsgi_app)
db = SQLAlchemy(app)
zoho_bp = make_zoho_blueprint(
    offline=True,
    scope="ZohoCRM.modules.ALL,ZohoCRM.settings.all,ZohoCRM.org.all,ZohoCRM.users.all",

)
app.register_blueprint(zoho_bp, url_prefix='/login')


# Imports needed for Admin view but after app init
from webapp.admin_model_view import AdminModelView, ParseAdminIndexView, SettingsView
from webapp.models import Email, Lead, User, Role
admin = Admin(app,
              name='parseLeads',
              index_view=ParseAdminIndexView(),
              base_template='master_admin.html',
              template_mode='bootstrap3'
              )

admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Role, db.session))
admin.add_view(AdminModelView(Lead, db.session))
admin.add_view(AdminModelView(Email, db.session))
admin.add_view(SettingsView(name='Settings'))

# Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# define a context processor for merging flask-admin's template context into the
# flask-security views
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


import webapp.views
