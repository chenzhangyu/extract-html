# coding=utf8

import logging

# set logger handler
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-6s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)

fh = logging.FileHandler("server.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger = logging.getLogger("")
logger.addHandler(fh)
logger.addHandler(console)

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import options

import settings as config  # noqa
import handler


settings = {
    "debug": options.debug,
    "port": options.port
}


urls = [
    (u"/", handler.IndexHandler),
]


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application(urls, **settings)
    server = tornado.httpserver.HTTPServer(application)
    logging.info("start on 127.0.0.1:{}".format(options.port))
    server.listen(options.port)
    server.start()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
