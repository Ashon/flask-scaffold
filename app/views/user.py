from flask_smorest import Blueprint

from models.user import User
from schema.user import UserSchema


blueprint = Blueprint(
    'User API', 'user', url_prefix='/users',
    description='사용자 정보 API'
)


@blueprint.route('')
@blueprint.response(UserSchema(many=True))
def get_users():
    """사용자 리스트 조회

    모든 사용자 리스트를 조회한다.
    """

    users = User.query.all()
    return users
