import json


class BaseResponseEntity(object):
    def __init__(self):
        self.ResponseCode = 500
        self.Data = {}

    def toJSONData(self):
        return dict(ResponseCode=self.ResponseCode, Data=self.Data)

    def toJSONCode(self):
        return dict(ResponseCode=self.ResponseCode)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'toJSON'):
            return obj.toJSON()
        else:
            return json.JSONEncoder.default(self, obj)