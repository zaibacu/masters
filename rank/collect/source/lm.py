from rank.util.scrape.reader import SiteReader
from rank.util.scrape.engine import PhantomEngine
from . import Base
import requests


def get_session_id():
    resp = requests.get("https://www.linkomanija.net/login.php")
    return resp.cookies["PHPSESSID"]


def headers():
    return {
        "Connection": "keep-alive",
        "Referer": "https://www.linkomanija.net/login.php",
        "User-agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "www.linkomanija.net",
        "Origin": "https://www.linkomanija.net",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "lt,en-US;q=0.8,en;q=0.6,ru;q=0.4,pl;q=0.2",
        "Upgrade-Insecure-Requests": "1"
    }


def cookies(session_id):
    return {
        "PHPSESSID": session_id
    }


def payload(username, password):
    return {"username": username, "password": password, "commit": "Prisijungti"}


class LMSiteReader(SiteReader):
    pass


class LMSource(Base):
    def __init__(self):
        # self.engine = PhantomEngine()
        self.reader = LMSiteReader()
        self.session_id = get_session_id()

    def auth(self, user, passw):
        import sys
        debug = {"verbose": sys.stderr}
        login_url = "https://www.linkomanija.net/takelogin.php"
        return requests.post(login_url, data=payload(user, passw), headers=headers(), cookies=cookies(self.session_id))

    def search(self, key) -> list:
        return requests.get("http://www.linkomanija.net/browse.php?search={0}".format(key),
                            headers=headers(), cookies=cookies(self.session_id))

