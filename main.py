import argparse
from Tkinter import Tk, Label, Button, StringVar
from collections import deque
from threading import Thread

import requests
from PIL import Image, ImageTk

from Strip import Strip
from parse import DilbertParser

strips = deque()
strips_lookup = set()
idx = 0


def append_strip(url, left=False):
    global idx
    if url not in strips_lookup:
        r = requests.get("http://dilbert.com{}".format(url))
        parser = DilbertParser()
        parser.feed(r.text)
        if left:
            strips.appendleft(parser.strip)
            idx += 1
        else:
            strips.append(parser.strip)
        strips_lookup.add(url)
        print "GET: {}".format(url)


parser = argparse.ArgumentParser(description='Dilbert browser')
parser.add_argument('date', nargs="?", default="2017-02-05", help='Start date')
args = parser.parse_args()
start_date = "/strip/{}".format(args.date)
append_strip(start_date)


class DilbertGUI:
    def __init__(self, master):
        self.master = master
        master.title("Dilbert browser")
        current = strips[0]  # type: Strip

        self.url_text = StringVar()
        self.url_text.set(current.url)
        self.url = Label(master, textvariable=self.url_text)
        self.url.pack()

        self.title_text = StringVar()
        self.title_text.set(current.title)
        self.title = Label(master, textvariable=self.title_text)
        self.title.pack()

        image = Image.open(current.comic)
        photo = ImageTk.PhotoImage(image)
        self.strip_img = Label(image=photo)
        self.strip_img.image = photo  # keep a reference!
        self.strip_img.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        Thread(target=append_strip, args=(current.next_strip,)).start()
        Thread(target=append_strip, args=(current.prev_strip, True)).start()

        self.master.bind("<Left>", lambda e, d=-1: self.change_strip(d))
        self.master.bind("<Right>", lambda e, d=1: self.change_strip(d))

    def change_strip(self, x):
        global idx
        """
        :type x: int
        """
        # idx += x
        # idx %= len(strips)
        nidx = max(min(idx + x, len(strips) - 1), 0)
        if nidx == idx:
            return

        idx = nidx
        self.render_strip(strips[idx])

        # preload
        current = strips[idx]
        Thread(target=append_strip, args=(current.next_strip,)).start()
        Thread(target=append_strip, args=(current.prev_strip, True)).start()

    def render_strip(self, s):
        """
        :type s: Strip
        """
        self.url_text.set(s.url)
        self.title_text.set(s.title)
        img = Image.open(s.comic)
        p = ImageTk.PhotoImage(img)
        self.strip_img.configure(image=p)
        self.strip_img.image = p
        self.strip_img.pack()


root = Tk()
my_gui = DilbertGUI(root)
root.mainloop()
