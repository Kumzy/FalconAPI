import falcon
import json
from sqlalchemy.ext.declarative import declarative_base
try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict
from app.models import User
from app.database import engine

Base = declarative_base()


class Collection():
    """
    Handle for endpoint: /v1/users
    """

    def to_json(self, body_dict):
        return json.dumps(body_dict)


    def on_error(self, resp, error=None):
        resp.status = error['status']
        meta = OrderedDict()
        meta['code'] = error['code']
        meta['message'] = error['message']

        obj = OrderedDict()
        obj['meta'] = meta
        resp.body = self.to_json(obj)

    def on_success(self, resp, data=None):
        resp.status = falcon.HTTP_200
        meta = OrderedDict()
        meta['code'] = 200
        meta['message'] = 'OK'

        obj = OrderedDict()
        obj['meta'] = meta
        obj['data'] = data
        resp.body = self.to_json(obj)

    #@falcon.before(auth_required)
    def on_get(self, req, resp):
        session = req.context['session']
        print(session.is_active)
        #Bugging here
        user_dbs = session.query(User).all()

        if user_dbs:
            obj = [User.to_dict() for user in user_dbs]
            self.on_success(resp, obj)
       # else:
         #   raise AppError()

    #@falcon.before(auth_required)
    #def on_put(self, req, res):
   #     pass