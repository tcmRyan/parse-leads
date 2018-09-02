from webapp.models import User
from webapp import db, user_datastore as user_ds


def create_role_and_admin():
    """
    Run this script to create a temporary admin user on a new db.
    """
    user_ds.find_or_create_role(name='superuser', description='Administrative Access')
    user_ds.create_user(
        email='admin',
        password='changeme1234',
        name='tmp_admin'
    )
    db.session.commit()
    user_ds.add_role_to_user('admin', 'superuser')
    db.session.commit()


if __name__ == '__main__':
    users = User.query.limit(1).all()
    if not users:
        create_role_and_admin()
