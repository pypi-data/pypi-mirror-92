import yaml


class Config(object):
    @staticmethod
    def get_config(cfg):
        """
        获取配置文件内容
        :param cfg:
        :return:
        """
        try:
            with open(cfg, 'r', encoding='UTF-8') as f:
                data = yaml.load(f)
            return data
        except Exception as e:
            raise Exception("读取服务配置文件失败, error: {}".format(str(e)))
