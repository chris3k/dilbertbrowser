import requests
from HTMLParser import HTMLParser
from Strip import Strip
import json
from StringIO import StringIO


class DilbertParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.properties = dict()

    @property
    def strip(self):
        s = Strip()
        s.title = self.properties.get("og:title", "")
        s.url = self.properties.get("og:url", "")
        s.img_url = self.properties.get("og:image", "")
        try:
            r = requests.get(s.img_url)
            s.comic = StringIO(r.content)
        except Exception as e:
            s.comic = None
        # s.local_img_path = self.properties.get("", "") "dt170206.gif"
        s.prev_strip = self.properties.get("prev_strip", "")
        s.next_strip = self.properties.get("next_strip", "")
        return s

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            m = dict((k, v) for k, v in attrs)
            k = m.get("property", None)
            if k:
                self.properties[k] = m.get("content", "")

        if tag == "a":
            m = dict((k, v) for k, v in attrs)
            if m.get("title") == "Older Strip":
                self.properties["prev_strip"] = m.get("href")
            if m.get("title") == "Next Strip":
                self.properties["next_strip"] = m.get("href")


if __name__ == "__main__":
    parser = DilbertParser()
    r = requests.get("http://dilbert.com/strip/2017-02-05")
    parser.feed(r.text)
    print json.dumps(parser.properties, indent=2)
