"""Recieve POST requests on the database"""

from tornado.options import define, options
import datetime
import logging
import os
import torndb
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

# "X-X-X" in this file denotes keyword not intended to expose

define("port", default=8888, help="Run on the given port", type=int)
define("mysql_host", default="127.0.0.1", help="ping-me database host")
define("mysql_database", default="X-X-X", help="ping-me database name")
define("mysql_user", default="X-X-X", help="tornado_api database user")
define("mysql_password", default="X-X-X", help="password mysql")

logging.basicConfig(filename='X-X-X', level=logging.INFO,
                    format='%(asctime)s %(message)s', filemode='w')


class Application(tornado.web.Application):
    def __init__(self):
        project_dir = os.getcwd()
        handlers = [
            (r"/X-X-X", ConfigHandler),
        ]
        settings = dict(
            # autoescape = None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class ConfigHandler(BaseHandler):
    def post(self):
        try:
            X-X-X = self.get_argument("X-X-X")
            # Check if data already exists.
            # Do some further verification.
            self.db.execute("INSERT INTO X-X-X SET \
                            X-X-X = '{}';".format(X-X-X))
        except Exception as e:
            logging.WARNING(e)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
