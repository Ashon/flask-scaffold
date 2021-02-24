from core.app import create_app
import settings

from views.user import blueprint as user_blp


routes = [user_blp, ]

app = create_app(__name__, settings, routes)
