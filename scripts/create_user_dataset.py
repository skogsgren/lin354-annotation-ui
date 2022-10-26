import sys
import os
import random


def main(username, n):
    """randomly chooses 'n' amount of tweets from "training pool" for user
       'username' and moves those to folder training/'username' """
    i = 0
    tweets = [x for x in os.listdir("training")]
    random.shuffle(tweets)
    assert not os.path.exists("training/%s" % username)
    os.mkdir("training/%s" % username)
    while i < n:
        twt = tweets.pop()
        os.rename("training/%s" % twt, "training/%s/%s" % (username, twt))
        i += 1


if __name__ == "__main__":
    main(sys.argv[1], 225)
