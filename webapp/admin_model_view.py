"""
Custom view to integrate flask-admin with the authentication and
authorization of flask-security
"""
import threading

from flask import abort, redirect, url_for, request, flash
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, BaseView, expose
from flask_security import current_user, url_for_security
from wtforms import StringField, Form, validators
from zcrmsdk import ZCRMRestClient, ZohoOAuth

from webapp import app


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
        ZCRM_REQUIRED_SCOPES = 'aaaserver.profile.READ'
                # 'ZohoCRM.org.ALL,'\
                # 'ZohoCRM.modules.ALL,'\
                # 'ZohoCRM.users.ALL,'\
                # 'ZohoCRM.settings.ALL'

        redirect_uri = app.config.get('BASE_URL') + url_for('zcrm_oauth_callback')

        zcrm_auth_url = 'https://accounts.zoho.com/oauth/v2/auth?' \
                        'response_type=code&access_type=online&' \
                        'scope={scope}&'\
                        'client_id={client_id}&'\
                        'redirect_uri={redirect_uri}'.format(scope=ZCRM_REQUIRED_SCOPES,
                                                             client_id=app.config.get('ZCRM_CLIENT_ID'),
                                                             redirect_uri=redirect_uri)
        form = GrantForm(request.form)
        zmodules = []
        if request.method == 'POST':
            grant_token = request.form['grant']

            if form.validate():
                flash('Initializing Zoho CRM ')
                threading.current_thread().__setattr__('current_user_email', 'admin@prestopianolessons.com')
                ZCRMRestClient.initialize()
                oauth_client = ZohoOAuth.get_client_instance()
                oauth_client.generate_access_token(grant_token)
                resp = ZCRMRestClient.get_instance().get_all_modules()
                zmodules = resp.data
            else:
                flash('Please re-submit grant token')

        zcrm_authenticated = request.args.get('zcrm', False)
        if zcrm_authenticated:
            flash('ZohoCRM Successfully Authenticated')

        return self.render('settings.html',
                           form=form,
                           zmodules=zmodules,
                           zcrm_auth_url=zcrm_auth_url)


class GrantForm(Form):
    grant = StringField('Zoho Grant Token: ', validators=[validators.required()])
