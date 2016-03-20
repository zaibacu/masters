from rank.util.scrape.reader import SiteReader
from rank.util.scrape.engine import StaticEngine
from . import Base


class FilmaiInSiteReader(SiteReader):
    pass


class FilmaiInSource(Base):
    def __init__(self):
        self.reader = FilmaiInSiteReader(StaticEngine())

    def search(self, key) -> list:
        import re
        import requests
        import xml.etree.ElementTree as ET
        sitemap = requests.get("http://www.filmai.in/sitemap.xml")
        root = ET.fromstring(sitemap.content)
        links = [url[0].text
                 for url in root]
        keys = key.lower().split(" ")
        patt = re.compile(r"/(?P<movie_id>\d+)")
        ids = map(lambda x: patt.search(x).group("movie_id"), filter(lambda x: all([key in x for key in keys]), links))
        for link in map(lambda x: "http://filmai.in/komentarai/{0}/".format(x), ids):
            self.reader.add_link(link)

        for bs, url in self.reader.scrape():
            # comment_blocks = bs.findAll("div", {"class": "notes-light"})
            for comment in bs.findAll("div", id=lambda x: x and x.startswith("comm-id-")):
                yield comment.text.strip()


