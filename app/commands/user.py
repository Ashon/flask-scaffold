from flask_script import Manager

from models.user import User


UserCommand = Manager(usage='Manage User models')


@UserCommand.command
def create(email, password):
    """Create user
    """

    user = User(email=email, password=password)
    user.save()

    print(user)


@UserCommand.command
def get(uuid):
    """Get user
    """
    user = User.query.filter(User.uuid == uuid).one()

    print(user)


@UserCommand.command
def list():
    """Listuser
    """
    all_users = User.query.all()

    print(all_users)


@UserCommand.command
def delete(uuid):
    """Delete user
    """
    user = User.query.filter(User.uuid == uuid).one()
    user.delete()
