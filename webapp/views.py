from flask import request, redirect, url_for, render_template
from flask_security import login_required
from flask_dance.contrib.zoho import zoho
from webapp.vendors import create_vendor_lead

from webapp import app, db
from webapp.parse import save_lead
from webapp.models import Email


@app.route('/')
def index():
    if not zoho.authorized:
        return redirect(url_for(('zoho.login')))
    resp = zoho.get('/crm/v2/users', params={'type': 'CurrentUser'})
    data = resp.json()
    user = data['users'][0]['full_name']
    # return redirect(url_for('admin.index'))
    return 'hi {}'.format(user)


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

    lead = save_lead(data)
    resp = create_vendor_lead(lead)

    message_meta.success = True if resp.status == '200' else False
    db.session.add(message_meta)
    db.session.commit()
    return 'OK'


@app.route('/config')
def config():
    tunnel = app.config.get('BASE_URL')
    return render_template('config.html', tunnel=tunnel)


