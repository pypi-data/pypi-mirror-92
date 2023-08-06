from etcd_register.util.config import Config
import requests


class HttpClient(object):
    conf = None

    def __init__(self, config):
        self.conf = Config.get_config(config)

    def invoke(self, service, method, json=None, version='v1'):
        try:
            url = self.conf.get('gateway')
            r = requests.post('{}/{}/{}/{}'.format(url, version, service, method), json=json)
            if r.status_code != 200:
                raise Exception("status code != 200")
            return r.json()
        except Exception as e:
            return dict(code=101, msg=str(e))
