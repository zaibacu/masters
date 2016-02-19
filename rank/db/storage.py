import pickle
from collections import namedtuple
Comment = namedtuple("Comment", ["text", "rating"])


class Storage(object):
    comments = []

    @staticmethod
    def load(f):
        return pickle.load(f)

    @classmethod
    def dump(cls, f):
        pickle.dump(cls, f)

    def add_comment(self, text, rating=0):
        self.comments = Comment(text, rating)

