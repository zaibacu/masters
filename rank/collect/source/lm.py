from rank.util.scrape.reader import SiteReader
from rank.util.scrape.engine import StaticEngine
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
        self.reader = LMSiteReader(StaticEngine())
        self.session_id = get_session_id()
        self.reader.add_headers(**headers())
        self.reader.add_cookies(**cookies(self.session_id))

    def auth(self, user, passw):
        import sys
        debug = {"verbose": sys.stderr}
        login_url = "https://www.linkomanija.net/takelogin.php"
        return requests.post(login_url, data=payload(user, passw), headers=headers(), cookies=cookies(self.session_id))

    def search(self, key) -> list:
        keywords = key.lower().split(" ")
        query = "c29=1&c52=1&c53=1&c61=1&c25=1&c26=1&incldead=0&search={0}".format("+".join(keywords))
        self.reader.add_link("https://www.linkomanija.net/browse.php?{0}".format(query))
        for bs, url in self.reader.scrape():
            if "details" in url:  # Comments parsing
                root = bs.find("div", {"id": "comments"})
                comments = root.findAll("div", {"class": "comment-text"})
                for comment in comments:
                    yield comment.text.strip()
            else:  # Getting movies
                root = bs.findAll("table")[3]
                rows = root.findAll("tr")
                for row in rows[1:]:
                    cols = row.findAll("td")
                    info = cols[1].findAll("a")[0]
                    title = info.text.lower()
                    if all([True if key in title else False for key in keywords]):
                        self.reader.add_link("https://www.linkomanija.net/{0}".format(info["href"]))
