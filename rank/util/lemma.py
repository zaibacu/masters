from urllib.parse import urlencode
from functools import lru_cache
import re
import requests


class Lemmator(object):
    def __init__(self):
        self.domain = "donelaitis.vdu.lt"
        self.pattern = re.compile(r"lemma=&quot;(?P<lemma>(\w|[ąčęėįšųūž])+)([(].*[)])?&quot;.*?type=&quot;(?P<type>((\w|[ąčęėįšųūž.,\s])*))&quot;")

    @lru_cache()
    def get_lemma(self, word):
        data = urlencode({"tekstas": word, "tipas": "anotuoti", "pateikti": "LM", "veiksmas": "Rezultatas puslapyje"})
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Referer": "http://donelaitis.vdu.lt/main_helper.php?id=4&nr=7_2",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Origin": "http://donelaitis.vdu.lt"
                   }
        resp = requests.post(url="{0}/main_helper.php?id=4&nr=7_2".format(self.domain), body=data, headers=headers)
        raw = resp.read().decode("UTF-8")
        result = self.pattern.search(raw)
        if result:
            return result.group("lemma"), result.group("type")
        else:
            return word, None
