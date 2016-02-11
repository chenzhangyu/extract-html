# coding=utf8

import logging

from bs4 import BeautifulSoup
from bs4.element import Tag, Comment


def priority_get(d, fields, default=None):
    result = None
    for key in fields:
        key_list = key.split(".")
        iter_result = d
        counter = 0
        for k in key_list:
            counter += 1
            if counter < len(key_list):
                iter_result = iter_result.get(k, {})
                if not iter_result:
                    break
            else:
                iter_result = iter_result.get(k)
        if iter_result:
            result = iter_result
            break
    return result if result else default


class ExtractResponse(object):

    def __init__(self):
        self._counter = 0
        self._r = []

    def _decode_string(self, raw):
        return raw.decode("string_escape")

    def _strip_img_src(self, raw):
        raw = self._decode_string(raw)
        if raw:
            if raw[0] in ("'", '"'):
                raw = raw[1:]
            if raw[-1] in ("'", '"'):
                raw = raw[:-1]
        return raw

    @property
    def type_allowed(self):
        return ("text", "image")

    def push(self, data, _type="text"):
        assert _type in self.type_allowed
        if _type == "image":
            data = self._strip_img_src(data)
        self._r.append({
            "seq": self._counter,
            "type": _type,
            "data": data
        })
        self._counter += 1

    def get_result(self):
        return self._r


class Extraxt(object):

    def __init__(self, raw, url="url"):
        self.raw = raw
        self.result = ExtractResponse()
        self.soup = BeautifulSoup(raw, "lxml")

    def parse(self):
        for child in self.soup.body.descendants:
            if isinstance(child, Tag):
                if child.name == "img":
                    img_src = priority_get(child, ["src", "data-src"])
                    if img_src:
                        self.result.push(img_src, "image")
                    else:
                        logging.info("no img src, {}, <url: {}>".format(child, "url"))
            elif isinstance(child, Comment):
                continue
            else:
                if child.string != "\n" and child.string.strip():
                    # print repr(child.string)
                    self.result.push(child.string)

    def get_result(self):
        return self.result.get_result()


def extract(raw):
    result = ExtractResponse()
    soup = BeautifulSoup(raw, "lxml")
    for child in soup.body.descendants:
        if isinstance(child, Tag):
            if child.name == "img":
                img_src = priority_get(child, ["src", "data-src"])
                if img_src:
                    result.push(img_src, "image")
                else:
                    logging.info("no img src, {}, <url: {}>".format(child, "url"))
        elif isinstance(child, Comment):
            continue
        else:
            if child.string != "\n" and child.string.strip():
                # print repr(child.string)
                result.push(child.string)
    return result.get_result()


if __name__ == "__main__":
    s = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title></title>
        </head>
        <body>
            <p> test text </p>
            <img src="a.jpeg" width="100px"> <br />
            <img src='a.jpeg' width="100px"> <br>
            <p> new text </p>
            <div>
                haha
                <!-- <p> hehe </p> -->
            </div>
        </body>
        </html>
        """
    with open("./raw.html", "r") as f:
        s = f.read()
    task = Extraxt(s)
    task.parse()
    print task.get_result()
