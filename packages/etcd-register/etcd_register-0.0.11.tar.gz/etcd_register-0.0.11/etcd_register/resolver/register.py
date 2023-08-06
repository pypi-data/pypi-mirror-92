import asyncio
import signal
import socket

import grpc
import yaml
from concurrent import futures

from etcd_register.etcd.client import EtcdClient
from etcd_register.util.config import Config


class Rpc(object):
    etcd = None

    def register(self, filepath, function, instance, message_size=205109840):
        """

        :param filepath: 配置文件
        :param function: 注册函数
        :param instance: 注册实例
        :param message_size: 单次请求数据大小
        :return:
        """
        config = Config.get_config(filepath)
        addr = config.get("etcd")
        scheme = config.get("scheme", "unknown")
        if not addr:
            raise Exception("etcd地址: {} 不规范".format(addr))
        port = ":{}".format(config.get("port"), 12306)
        service = config.get("service")
        self.etcd = EtcdClient(addr, scheme)

        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGTERM, self.term_sig_handler, loop)
        loop.add_signal_handler(signal.SIGINT, self.term_sig_handler, loop)
        loop.run_until_complete(self.run(config, service, port, function, instance, message_size))

    async def run(self, cfg, service, port, function, instance, message_size):
        await asyncio.gather(
            Rpc.listen(function, instance, port, message_size),
            self.serve(cfg, service, instance, port),
        )

    def term_sig_handler(self, service, port, lp):
        self.etcd.unregister_service(service, Rpc.get_ip_address() + port).send(None)
        lp.stop()

    @staticmethod
    async def listen(function, instance, port, message_size):
        MAX_MESSAGE_LENGTH = message_size
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                             options=[
                                 ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                                 ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
                             ]
                             )
        function(instance, server)
        server.add_insecure_port('[::]{}'.format(port))
        print("服务启动成功, 端口: ", port)
        server.start()
        await Rpc.wait(60)

    @staticmethod
    async def wait(timeout):
        while True:
            await asyncio.sleep(timeout)

    async def serve(self, cfg, service, instance, port):
        await self.etcd.register_api(service, instance, cfg)
        await self.etcd.register_service(service, Rpc.get_ip_address() + port, 10)

    @staticmethod
    def get_ip_address():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


reg = Rpc()
