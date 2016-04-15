import redis
import pickle
import sys


def select_rand(lst, n):
    import random
    return random.sample(lst, n)


def get_positive(comments, limit):
    return select_rand([comment for comment in comments if comment.rating == "1"], limit)


def get_negative(comments, limit):
    return select_rand([comment for comment in comments if comment.rating == "-1"], limit)


def get_group(comments, train_limit, test_limit):
    from random import shuffle
    positives = get_positive(comments, train_limit + test_limit)
    negatives = get_negative(comments, train_limit + test_limit)

    training = positives[:train_limit] + negatives[:train_limit]
    testing = positives[train_limit:] + negatives[train_limit:]

    shuffle(training)
    shuffle(testing)
    return training, testing


def main(args):
    r = redis.StrictRedis(host='localhost', port=6379, db=1)
    comments = [pickle.loads(r.get(key)) for key in r.keys("comment:*")]

    train_data, test_data = get_group(comments, args.train, args.test)

    with open(args.o1, "w") as f:
        for comment in train_data:
            text = comment.text
            f.write("{1}|{0}\n".format(text.replace("\n", " "), comment.rating))

    with open(args.o2, "w") as f:
        for comment in test_data:
            text = comment.text
            f.write("?|{0}\n".format(text.replace("\n", " ")))

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--train", type=int, default=200, help="count of items for train")
    parser.add_argument("--test", type=int, default=50, help="count of items for test")
    parser.add_argument("-o1", help="train output file")
    parser.add_argument("-o2", help="test output file")
    main(parser.parse_args())
