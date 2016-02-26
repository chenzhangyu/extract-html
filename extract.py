# coding=utf8

import logging
from collections import namedtuple

from bs4 import BeautifulSoup
from bs4.element import Tag, Comment


LinkItem = namedtuple("LinkItem", ["type_", "data", "href"])


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

    def push(self, data, type_="text", link=""):
        assert type_ in self.type_allowed
        if type_ == "image":
            data = self._strip_img_src(data)

        is_merged = False
        if self._counter:

            # TODO get by seq
            item = self._r.pop()

            if item["type"] == "text" and type_ == "text" and item["link"] == link:
                item["data"] += data
                self._r.append(item)
                is_merged = True
            else:
                self._r.append(item)

        if not is_merged:
            self._r.append({
                "seq": self._counter,
                "type": type_,
                "data": data,
                "link": link
            })
            self._counter += 1

    def get_result(self):
        return self._r


class Extraxt(object):

    def __init__(self, raw, url="url"):
        self.raw = raw
        self.result = ExtractResponse()
        self.soup = BeautifulSoup(raw, "lxml")
        self._href = None

    def parse(self):
        for child in self.soup.body.descendants:
            if isinstance(child, Tag):
                if child.name == "img":
                    img_src = priority_get(child, ["src", "data-src"])
                    if img_src:
                        self.result.push(img_src, "image")
                    else:
                        logging.info("no img src, {}, <url: {}>".format(child, "url"))
                elif child.name == "a":
                    self._parse_tag_a(child)
            elif isinstance(child, Comment):
                continue
            else:
                if child.string != "\n" and child.string.strip():
                    # print repr(child.string)
                    self.result.push(child.string)

    def _parse_tag_a(self, root):
        _r = []
        link = root.get("href", "")
        for child in root:
            if isinstance(child, Tag):
                if child.name == "img":
                    _r.append(LinkItem("image", priority_get(child, ["src", "data-src"]), link))

            elif isinstance(child, Comment):
                continue

            else:
                if child.string != "\n" and child.string.strip():
                    if len(_r):
                        last_item = LinkItem(*_r.pop())
                        if last_item.type_ == "text":
                            last_item.data += child.string
                            _r.append(last_item)
                        else:
                            _r.append(LinkItem("text", child.string, link))
                    _r.append(LinkItem("text", child.string, link))

        logging.info(_r)
        for item in _r:
            self.result.push(item.data, type_=item.type_, link=item.href)

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
