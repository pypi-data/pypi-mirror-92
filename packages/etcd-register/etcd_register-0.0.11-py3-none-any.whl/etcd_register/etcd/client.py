import asyncio
import json

from aioetcd3.client import client


class EtcdClient(object):
    client = None
    scheme = None

    def __init__(self, host, scheme):
        """
        :param host: ip:port,ip:port
        """
        self.client = client(host)
        self.scheme = scheme

    async def unregister_service(self, name, addr):
        print("unregister service: ", "/{}/{}/{}".format(self.scheme, name, addr))
        await self.client.delete("/{}/{}/{}".format(self.scheme, name, addr))

    async def register_service(self, name, addr, ttl):
        while True:
            value, meta = await self.client.get("/{}/{}/{}".format(self.scheme, name, addr))
            if value is None:
                await self.with_alive(name, addr, ttl)
            await asyncio.sleep(ttl)

    @staticmethod
    def lower_first(s):
        if len(s) == 0:
            return ""
        if s[0].islower():
            if len(s) == 1:
                return s[0].lower()
            return s[0].lower() + s[1:]
        return ""

    async def register_api(self, name, instance, cfg):
        version = cfg.get("version")
        methods = cfg.get("method", {})
        for d in dir(instance):
            if d.startswith("_") or d.endswith("_"):
                continue
            if d not in methods.keys():
                print("方法: {}注册失败, 请在service.yml中配置".format(d))
                continue
            info = methods.get(d)
            await self.register_single(version, name, d, info)

    async def register_single(self, version, service, method_name, no_auth=None):
        key = "{}.{}.{}".format(version, EtcdClient.lower_first(service), EtcdClient.lower_first(method_name))
        info = {"no_auth": False if no_auth is None else no_auth.get("no_auth"),
                "path": "/{}/{}".format(service, method_name)}
        await self.client.put(key, json.dumps(info, ensure_ascii=False))

    async def with_alive(self, name, addr, ttl):
        lease = await self.client.grant_lease(ttl)
        key = "/{}/{}/{}".format(self.scheme, name, addr)
        print("service alive: {}".format(key))
        await self.client.put(key, addr, lease=lease)
        await self.refresh_lease(lease, ttl)

    async def refresh_lease(self, lease, ttl):
        try:
            while True:
                await self.client.refresh_lease(lease)
                await asyncio.sleep(ttl - 5)
        except Exception as err:
            print("服务续租失败, error: ", err)
