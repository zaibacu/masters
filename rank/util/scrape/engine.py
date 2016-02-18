import logging
logger = logging.getLogger(__name__)


class Engine(object):
    def read(self, url):
        pass


class StaticEngine(Engine):
    def read(self, url):
        from urllib.request import urlopen
        from urllib.error import HTTPError
        try:
            return urlopen(url).read().decode("UTF-8")
        except HTTPError as e:
            logger.error(e, "scrapping \"{0}\" failed".format(url))
            return None


class PhantomEngine(Engine):
    def __init__(self, use_tor=False):
        self.use_tor = use_tor

    def read(self, url):
        from selenium import webdriver
        from . import pimp_my_selenium
        if self.use_tor:
            path = "/usr/local/bin/phantomjs"
            args = ["--proxy=localhost:9030", "--proxy-type=socks5"]
            driver = webdriver.PhantomJS(path, service_args=args)
            pimp_my_selenium(driver)

        else:
            driver = webdriver.PhantomJS()
        driver.get(url)
        raw = driver.page_source
        driver.close()
        return raw
