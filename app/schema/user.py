import marshmallow as ma


class UserSchema(ma.Schema):
    uuid = ma.fields.UUID(required=True, description='사용자 오브젝트 UUID')
    email = ma.fields.Email(required=True, description='사용자 이메일 주소')
