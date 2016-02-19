import logging
logger = logging.getLogger(__name__)


class Engine(object):
    def read(self, url, cookies=None):
        pass


class StaticEngine(Engine):
    def read(self, url, cookies=None):
        from urllib.request import urlopen
        from urllib.error import HTTPError
        try:
            return urlopen(url).read().decode("UTF-8")
        except HTTPError as e:
            logger.error(e, "scrapping \"{0}\" failed".format(url))
            return None


class PhantomEngine(Engine):
    def __init__(self, use_tor=False):
        from selenium import webdriver
        from . import pimp_my_selenium
        if use_tor:
            path = "/usr/local/bin/phantomjs"
            args = ["--proxy=localhost:9030", "--proxy-type=socks5"]
            self.driver = webdriver.PhantomJS(path, service_args=args)
            pimp_my_selenium(self.driver)
        else:
            self.driver = webdriver.PhantomJS()

    def read(self, url, cookies=None):
        self.driver.get(url)
        raw = self.driver.page_source
        return raw
