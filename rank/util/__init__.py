from Levenshtein import distance
import logging
logger = logging.getLogger(__name__)


def levenshtein(w1: str, w2: str) -> int:
    logger.debug("Distance between {0} and {1}".format(w1, w2))
    return distance(w1, w2)
