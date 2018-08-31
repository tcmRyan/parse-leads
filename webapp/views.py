from flask import request, redirect, url_for
from flask_security import login_required
from webapp import app, db
import email
from email.policy import SMTP

from webapp.models import Lead, Email


@app.route('/')
@login_required
def index():
    return redirect(url_for('admin.index'))


@app.route('/incoming-messages', methods=['GET', 'POST'])
def incoming_messages():
    data = request.get_json()
    date_received = data['headers']['date']
    received_from = data['envelope']['from']
    message_meta = Email(
        date_received=date_received,
        received_from=received_from,
        success=False,
    )
    db.session.add(message_meta)
    db.session.commit()

    raw = email.message_from_string(data['plain'], policy=SMTP)

    lead_info = {}
    for part in raw.walk():
        info = find_and_update(part)
        if info:
            lead_info.update(info)

    lead = Lead(
        first_name=lead_info['first_name'],
        last_name=lead_info['last_name'],
        company=lead_info['company'],
        source=lead_info['source'],
        email=lead_info['email'],
        phone=lead_info['phone'],
        comments=lead_info['comments']
    )
    db.session.add(lead)
    message_meta.success = True
    db.session.add(message_meta)
    db.session.commit()
    return 'OK'


def find_and_update(line):
    for key in template_map.keys():
        if key in line:
            return {template_map[key]: line.lspilt(key)[-1]}


template_map = {
    'First Name: ': 'first_name',
    'Last Name: ': 'last_name',
    'Company Name: ': 'company',
    'Source: ': 'source',
    'Primary Email: ': 'email',
    'Primary Phone: ': 'phone',
    'Comments: ': 'comments'
}
