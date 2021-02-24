#!/usr/bin/env python
from flask_script import Manager
from flask_migrate import MigrateCommand

from wsgi import app
from commands.user import UserCommand


manager = Manager(app)

# flask-migration 관련 관리 커맨드들이 db 커맨드 컬렉션으로 등록된다.
manager.add_command('db', MigrateCommand)
manager.add_command('user', UserCommand)

if __name__ == '__main__':
    manager.run()
