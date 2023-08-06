import MySQLdb

from .resolve import resolve


class Mysql:

  def __init__(self, config):
    self.config = config

    args = {
      "host":   resolve(self.config["host"]),
      "user":   resolve(self.config["username"]),
      "passwd": resolve(self.config["password"]),
    }

    if self.config.get("database") is not None:
      args["db"] = resolve(self.config["database"])

    self.connection = MySQLdb.connect(**args)


  def query(self, sql, params={}):
    cursor = self.connection.cursor()
    cursor.execute(sql, params)
    cols = [col[0] for col in cursor.description]
    rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
    cursor.close()

    return rows
