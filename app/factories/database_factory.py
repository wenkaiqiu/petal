from db import PostgreSQL, JSON
from .base import Factory


class DatabaseFactory(Factory):
    """
    提供访问数据库的统一接口，测试时强制使用json
    """
    def generate(self, **kwargs):
        conf = kwargs["conf"]
        # todo: 为测试方便，强制使用json
        conf["db_type"] = "json"

        if conf["db_type"] == "postgresql":
            PostgreSQL.set_conf(conf)
            return PostgreSQL
        elif conf["db_type"] == "json":
            JSON.set_conf(conf)
            return JSON
