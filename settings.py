# coding=utf8

import os

from tornado.options import parse_config_file, define


root_path = os.path.dirname(__file__)

define("debug", True)
define("port", 24300)
define("log_file", None)

parse_config_file(os.path.join(root_path, "etc", "config.conf"))

print os.path.join(root_path, "etc", "config.conf")
