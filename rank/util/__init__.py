from Levenshtein import distance
import logging
logger = logging.getLogger(__name__)


def levenshtein(w1: tuple, w2: tuple) -> int:
    logger.debug("Distance between {0} and {1}".format(w1, w2))
    return min([
        distance(d1, d2)
        for d1, d2 in zip(w1, w2)
    ])
