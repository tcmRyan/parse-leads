from flask_dance.contrib.zoho import zoho


def create_vendor_lead(lead):
    data = {
        "Company": lead.company,
        "Last_Name": lead.last_name,
        "First_Name": lead.first_name,
        "Email": lead.email,
        "Lead_Source": lead.source,
        "Phone": lead.phone,
        "Details": lead.comments
    }
    resp = zoho.post('/crm/v2/Leads/upsert', data={'data': [data]})
    return resp
