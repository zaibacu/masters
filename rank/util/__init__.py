from Levenshtein import distance
import logging
logger = logging.getLogger(__name__)


def levenshtein(w1: str, w2: str) -> int:
    result = distance(w1, w2)
    logger.debug("Distance between {0} and {1} is {2}".format(w1, w2, result))
    return result


def stem(w1: str, w2: str) -> int:
    from stemmer import stemmer
    st = stemmer.Stemmer()
    return chars(st.stem(w1), st.stem(w2))


def chars(w1: str, w2: str) -> int:
    from itertools import zip_longest
    return sum([1
                for c1, c2 in zip_longest(w1, w2)
                if c1 != c2
                ])
