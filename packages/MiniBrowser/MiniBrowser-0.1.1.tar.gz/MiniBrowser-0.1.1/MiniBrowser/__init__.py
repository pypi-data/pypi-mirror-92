import pygame
from PygameUILib import *
from PythonEventSystem import *
from PygameAnimationLib import *
from html.parser import HTMLParser
from html.entities import *
import urllib.request

class Parser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

class Browser:
    def __init__(self, x=0, y=0, w=1920, h=1080, custom = False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.events = {
            "p": Event(),
            "div": Event(),
            "style": Event()
        }
        if not custom:
            pass

    def parseURL(self, url):
        fp = urllib.request.urlopen(url)
        bytes = fp.read()
        output = bytes.decode("utf8")
        fp.close()
        return output

    def visit(self, url):
        parser = Parser()
        parser.feed(self.parseURL(url))
        parser.close()

    def update(self, surface):
        pass
