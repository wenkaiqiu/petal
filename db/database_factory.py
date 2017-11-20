import logging

from db.json import JSON
from db.restful import RESTFul

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('db.database_factory')
logger.setLevel(logging.DEBUG)


class DatabaseFactory:
    """
    提供访问数据库的统一接口，测试时强制使用json
    """
    @staticmethod
    def get_database(**kwargs):
        conf = kwargs["conf"]
        logger.info(f'Use {conf["db_type"]} as Database')

        if conf["db_type"] == "json":
            JSON.set_conf(conf)
            return JSON
        elif conf['db_type'] == 'RESTFul':
            RESTFul.set_conf(conf)
            return RESTFul
