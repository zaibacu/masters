import logging
import requests
logger = logging.getLogger(__name__)


class Engine(object):
    def read(self, url, headers=None, cookies=None):
        pass


class StaticEngine(Engine):
    def read(self, url, headers=None, cookies=None):
        try:
            return requests.get(url, headers=headers, cookies=cookies)
        except Exception as e:
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

    def read(self, url, headers=None, cookies=None):
        self.driver.add_cookie(cookies)
        self.driver.get(url)
        raw = self.driver.page_source
        return raw
