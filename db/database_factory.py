import logging

from db.postgresql import PostgreSQL
from db.json import JSON


logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('db.database_factory')
logger.setLevel(logging.DEBUG)


class DatabaseFactory:
    """
    提供访问数据库的统一接口，测试时强制使用json
    """
    @staticmethod
    def get_database(**kwargs):
        conf = kwargs["conf"]
        # todo: 为测试方便，强制使用json
        conf["db_type"] = "json"
        logger.info(f'Use {conf["db_type"]} as Database')

        if conf["db_type"] == "postgresql":
            PostgreSQL.set_conf(conf)
            return PostgreSQL
        elif conf["db_type"] == "json":
            JSON.set_conf(conf)
            return JSON
