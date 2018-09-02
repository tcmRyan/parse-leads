from webapp import db
from webapp.models import Lead

PARSE_MAP = {
    'First Name: ': 'first_name',
    'Last Name: ': 'last_name',
    'Company Name: ': 'company',
    'Source: ': 'source',
    'Primary Email: ': 'email',
    'Primary Phone: ': 'phone',
    'Comments: ': 'comments'
}


def find_and_update(line):
    for key in PARSE_MAP.keys():
        if key in line:
            return PARSE_MAP[key], line.split(key, maxsplit=1)[-1]
    return None, None


def save_lead(msg):
    # Couldn't get the darn python email parser to work, just doing it the simple way
    lines = msg['plain'].split('\r\n')

    lead_info = {}
    for line in lines:
        key, value = find_and_update(line)
        if key:
            lead_info[key] = value

    print(lead_info)
    lead = Lead(
        first_name=lead_info.get('first_name'),
        last_name=lead_info.get('last_name'),
        company=lead_info.get('company'),
        source=lead_info.get('source'),
        email=lead_info.get('email'),
        phone=lead_info.get('phone'),
        comments=lead_info.get('comments')
    )
    db.session.add(lead)
