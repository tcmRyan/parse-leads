"""
Custom view to integrate flask-admin with the authentication and
authorization of flask-security
"""
from flask import abort, redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, BaseView, expose
from flask_security import current_user, url_for_security
from wtforms import StringField, Form, validators


class ParseAdminIndexView(AdminIndexView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when the view is not accessible
        """
        print('WAT')
        if not self.is_accessible():
            if current_user.is_authenticated:
                # Permission Denied
                abort(403)
            else:
                # login
                return redirect(url_for_security('login', next="/admin"))


class AdminModelView(ModelView):
    """
    Override some defaults of the flask-admin modelview to take advantage of flask-security
    """

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when the view is not accessible
        """

        if not self.is_accessible():
            if current_user.is_authenticated:
                # Permission Denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class SettingsView(BaseView):

    @expose('/', methods=['GET', 'POST'])
    def index(self):

        return self.render('settings.html')


class GrantForm(Form):
    grant = StringField('Zoho Grant Token: ', validators=[validators.required()])
