import falcon
import json

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict


from app.database import engine


class BaseResource(object):
    HELLO_WORLD = {
        'server': 'test',
        'database': '%s' % (engine.name)
    }

    def to_json(self, body_dict):
        return json.dumps(body_dict)


    def on_success(self, res, data=None):
        res.status = falcon.HTTP_200
        meta = OrderedDict()
        meta['code'] = 200
        meta['message'] = 'OK'

        obj = OrderedDict()
        obj['meta'] = meta
        obj['data'] = data
        res.body = self.to_json(obj)

    def on_get(self, req, res):
        if req.path == '/':
            res.status = falcon.HTTP_200
            res.body = self.to_json(self.HELLO_WORLD)
