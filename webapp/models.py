from webapp import db

from flask_security import UserMixin, RoleMixin

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    """
    Roles for authorization.
    """
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    """Authorized Users For the ParseLeads
    :param str email: email address of user
    "param str password: encrypted password for the user
    """

    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    active = db.Column(db.Boolean, default=False)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role',
                            secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    company = db.Column(db.String)
    source = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    comments = db.Column(db.String)


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    date_received = db.Column(db.DateTime)
    received_from = db.Column(db.String)
    success = db.Column(db.Boolean)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'))
    lead = db.relationship(Lead, uselist=False)
