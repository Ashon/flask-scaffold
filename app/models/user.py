import uuid
from datetime import datetime
from functools import cached_property

from flask import current_app
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from core.context import db


def generate_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    uuid = db.Column(db.String(36), default=generate_uuid, primary_key=True)

    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=datetime.utcnow)

    @cached_property
    def _salt(self):
        return current_app.config.get('SALT')

    def check_password(self, password):
        return check_password_hash(self.password, self._salt + password)

    def save(self):
        self.password = generate_password_hash(self._salt + self.password)

        db.session.add(self)
        db.session.commit()

        return self

    def delete(self):
        db.session.begin(subtransactions=True)

        try:
            db.session.delete(self)
            db.session.commit()

        except Exception:
            db.session.rollback()

        db.session.commit()
