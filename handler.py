# coding=utf8

import json
import logging
import traceback

import tornado.web
from tornado.httpclient import AsyncHTTPClient
from readability.readability import Document
from bs4 import BeautifulSoup

from extract import Extraxt


class IndexHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def post(self):
        logging.info(self.request)
        url = self.get_body_argument("url")
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        }
        http_client = AsyncHTTPClient()
        try:
            http_client.fetch(url, callback=self.extract_data, headers=headers)
        except:
            logging.error(traceback.format_exc())
            self.write(json.dumps({'message': 'failure'}))
            self.finish()

    def extract_data(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        if soup.title:
            title = soup.title.string.strip()
        else:
            title = ''

        document = Document(response.body).summary()
        task = Extraxt(document)
        task.parse()
        self.write(json.dumps({
            "title": title,
            "items": task.get_result()
        }))
        self.finish()
