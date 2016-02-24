# coding=utf8

import logging

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

import handler


settings = {
    "debug": True,
    "port": 24300
}


urls = [
    (u"/", handler.IndexHandler),
]


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application(urls, **settings)
    server = tornado.httpserver.HTTPServer(application)
    logging.info("start on 127.0.0.1:{}".format(settings["port"]))
    server.listen(settings["port"])
    server.start()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    logging.basicConfig(
        filename="server.log",
        level=logging.DEBUG,
        format="[%(name)s][%(levelname)s][%(asctime)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    main()
