import json

import grpc

from etcd_register.proto import invoke_pb2, invoke_pb2_grpc
from etcd_register.util.config import Config


class RpcClient(object):
    conf = None

    def __init__(self, config):
        self.conf = Config.get_config(config)

    @staticmethod
    def encode(data):
        return json.dumps(data).encode('utf-8')

    @staticmethod
    def decode(data):
        return data.decode('utf-8')

    def invoke(self, service, method, args=None, version='v1', origin=False):
        try:
            addr = self.conf.get('rpc')
            channel = grpc.insecure_channel(addr)
            stub = invoke_pb2_grpc.RpcServiceStub(channel)
            request = invoke_pb2.Args()
            request.version = version
            request.service = service
            request.method = method
            if isinstance(args, bytes):
                request.args = args
            else:
                request.args = json.dumps(args, ensure_ascii=False).encode('utf-8')
            response = stub.Invoke(request)
            if origin:
                return Response(response.code, response.resultJson, response.msg)
            data = response.resultJson.decode('utf-8')
            return Response(response.code, data, response.msg)
        except Exception as e:
            return Response(101, None, str(e))


class Response(object):
    code = None
    data = None
    msg = None

    def __init__(self, code, data, msg):
        self.code = code
        self.data = data
        self.msg = msg

    def marshal(self):
        return {"code": self.code, "data": self.data, "msg": self.msg}

    def __str__(self):
        return "code: {}\nmsg: {}\ndata: {}".format(self.code, self.msg, self.data)


if __name__ == "__main__":
    client = RpcClient("/Users/wuranxu/PycharmProjects/AppMailService/service.yaml")
    print(client.invoke('user', 'insertUserLog', {"school_id": 3}))
