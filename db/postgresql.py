import logging
import psycopg2

from .base import Database

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('db.postgresql')
logger.setLevel(logging.DEBUG)


class PostgreSQL(Database):
    conn = None

    @classmethod
    def set_conf(cls, conf):
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
            cls.conn = psycopg2.connect(**params)
            logger.info("<Database> connect success")
        except Exception as e:
            logger.warning("<Database> connect failed")
            cls.conn.close()
            print(e)

    # todo: 实现抽象类Database的相应方法
