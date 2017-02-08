import os


class Strip(object):
    def __init__(self):
        self.url = None
        self.title = ""
        self.date = None
        self.next_strip = None
        self.prev_strip = None
        self.img_url = None
        self._local_img_path = None
        self._comic = None

    @property
    def local_img_path(self):
        if self._local_img_path:
            return os.path.join("strips", self._local_img_path)

    @local_img_path.setter
    def local_img_path(self, url):
        self._local_img_path = url

    @property
    def comic(self):
        if self.local_img_path and os.path.exists(self.local_img_path):
            return self.local_img_path
        return self._comic

    @comic.setter
    def comic(self, x):
        self._comic = x

    def parse(self):
        pass

    def download(self):
        pass

    def __str__(self):
        return "<url={}, local_path={}>".format(self.url, self._local_img_path)

    def __repr__(self):
        return self.__str__()
