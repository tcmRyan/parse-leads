from flask import request, redirect, url_for, render_template
from flask_security import login_required
from zcrmsdk import ZCRMRestClient, ZohoOAuth

from webapp import app, db
from webapp.parse import save_lead
from webapp.models import Email


@app.route('/')
@login_required
def index():
    return redirect(url_for('admin.index'))


@app.route('/incoming-messages', methods=['GET', 'POST'])
def incoming_messages():
    data = request.get_json()
    date_received = data['headers']['Date']
    received_from = data['headers']['From']
    message_meta = Email(
        date_received=date_received,
        received_from=received_from,
        success=False,
    )
    db.session.add(message_meta)
    db.session.commit()

    save_lead(data)

    message_meta.success = True
    db.session.add(message_meta)
    db.session.commit()
    return 'OK'


@app.route('/oauth2callback', methods=['GET'])
def zcrm_oauth_callback():
    grant_token = request.args.get('code')
    ZCRMRestClient.initialize()
    oauth_client = ZohoOAuth.get_client_instance()
    oauth_client.generate_access_token(grant_token)
    return redirect(url_for('settingsview.index', zcrm=True))


@app.route('/config')
def config():
    tunnel = app.config.get('BASE_URL')
    return render_template('config.html', tunnel=tunnel)


