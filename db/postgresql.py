import logging
import psycopg2

from .base import Database

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('db.postgresql')
logger.setLevel(logging.DEBUG)


class PostgreSQL(Database):
    """
    用于访问PostgreSQL的数据库类，实现抽象父类Database定义的接口
    """
    _conn = None  # sql连接

    @classmethod
    def set_conf(cls, conf):
        """
        读取数据库配置信息，创建与数据库的连接
        :param conf:
        :return:
        """
        logger.info("<PostgreSQL> set_conf")
        params = {
            "database": conf["db_name"],
            "user": conf["db_user"],
            "password": conf["db_pass"],
            "host": conf["db_host"],
            "port": conf["db_port"],
        }
        logger.info("<PostgreSQL> try to connect PostgreSQL")
        try:
            cls._conn = psycopg2.connect(**params)
            logger.info("<Database> connect success")
        except Exception as e:
            logger.warning("<Database> connect failed")
            cls._conn.close()
            print(e)
