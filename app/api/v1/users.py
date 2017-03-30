import falcon
import json
from sqlalchemy.ext.declarative import declarative_base
from app.api.common import BaseResource
try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict
from app.models import User

from sqlalchemy.ext.declarative import DeclarativeMeta
from app.database import engine

Base = declarative_base()

class AlchemyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, tuple):
            data = {}
            for obj in o:
                data.update(self.parse_sqlalchemy_object(obj))
            return data
        if isinstance(o.__class__, DeclarativeMeta):
            return self.parse_sqlalchemy_object(o)
        return json.JSONEncoder.default(self, o)

    def parse_sqlalchemy_object(self, o):
        data = {}
        fields = o.__json__() if hasattr(o, '__json__') else dir(o)
        for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class']]:
            value = o.__getattribute__(field)
            try:
                json.dumps(value)
                data[field] = value
            except TypeError:
                data[field] = None
        return data


class Collection(   ):
    """
    Handle for endpoint: /v1/users
    """

    def to_json(self, body_dict):
        return json.dumps(body_dict, cls=AlchemyEncoder)


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
        print(req.context['session'].session_factory)
        #Bugging here
        users = session.query(User).all()
        print(users)
        if users:
            self.on_success(resp, users)
       # else:
         #   raise AppError()

    #@falcon.before(auth_required)
    #def on_put(self, req, res):
   #     pass