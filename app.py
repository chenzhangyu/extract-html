# coding=utf8

import logging

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
    logging.basicConfig(
        filename=options.log_file,
        level=logging.DEBUG,
        format="[%(name)s][%(levelname)s][%(asctime)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    main()
