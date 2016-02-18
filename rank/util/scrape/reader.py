from bs4 import BeautifulSoup
from queue import Queue
from .engine import StaticEngine
import logging

logger = logging.getLogger(__name__)


class SiteReader(object):
    def __init__(self, engine=None):
        self.queue = Queue()
        if not engine:
            self.engine = StaticEngine()
        else:
            self.engine = engine

    def add_link(self, url):
        logger.debug("Adding URL: {0}".format(url))
        self.queue.put(url)

    def scrape(self):
        while not self.queue.empty():
            url = self.queue.get()
            logger.debug("Scrapping URL: {0}".format(url))
            raw = self.engine.read(url)
            if raw:
                yield self._process(raw), url

    @staticmethod
    def _process(raw):
        return BeautifulSoup(raw, "lxml")
