from Levenshtein import distance
import logging
logger = logging.getLogger(__name__)


def levenshtein(w1: str, w2: str) -> int:
    result = distance(w1, w2)
    logger.debug("Distance between {0} and {1} is {2}".format(w1, w2, result))
    return result
