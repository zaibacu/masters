from rank.util.scrape.reader import SiteReader
from rank.util.scrape.engine import StaticEngine
from . import Base


def payload(user, passw):
    return {"username": user, "password": passw}


class TorrentLtSiteReader(SiteReader):
    pass


class TorrentLtSource(Base):
    def __init__(self):
        self.reader = TorrentLtSiteReader(StaticEngine())

    def auth(self, user, passw):
        login_url = "http://torrent.ai/lt/account-login.php"
        session = self.reader.engine.session
        session.post(login_url, data=payload(user, passw))
        return session

    def search(self, key) -> list:
        keywords = key.lower().replace(" ", "+")
        query = "search={0}&cats%5B%5D=33&cats%5B%5D=43&cats%5B%5D=34&cats%5B%5D=32".format(keywords)
        self.reader.add_link("http://torrent.ai/lt/torrents?{0}".format(query))
        for bs, url in self.reader.scrape():
            if "torrents" in url:  # Torrents list
                root = bs.find("table", {"class": "torrents_table"})
                movies = root.findAll("tr")
                movie_links = [tag.find("a")["href"]
                               for movie in movies
                               for tag in movie.findAll("td", {"class": "torrent_name"})
                               if movie and tag]
                for link in movie_links:
                    self.reader.add_link("http://torrent.ai/lt/{0}".format(link))
            else:  # Movie
                root = bs.find("div", {"class": "torrent_comments"})
                comments = root.findAll("div", {"class": "comment_wrap_parent"})
                for comment in comments:
                    body = comment.find("div", {"class": "comment_body"})
                    body.find("div", {"class": "comment_actions"}).decompose()
                    body.find("div", {"class": "comment_reply"}).decompose()
                    yield body.text.strip()

