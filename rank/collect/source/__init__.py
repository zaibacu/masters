from collections import namedtuple
Result = namedtuple("Result", ["text"])


class Base(object):
    def auth(self, user, pwd) -> bool:
        pass

    def search(self, key) -> list:
        pass
