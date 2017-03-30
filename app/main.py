import falcon
from app.api.v1 import users
from app.middleware import DatabaseSessionManager
from app.database import db_session, init_session
from app.api.common import base

class App(falcon.API):

    def __init__(self,*args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.add_route('/',base.BaseResource())
        self.add_route('/v1/users',users.Collection())


init_session()
mdlw = [DatabaseSessionManager(db_session)]
application = App(middleware=mdlw)