import snscrape.modules.twitter as sntwitter
import os
import logging
import xml.etree.ElementTree as ET
import re
import sys
import datetime
import random

# Basic logging configuration
logging.basicConfig(format='%(asctime)s %(message)s')
logging.getLogger().setLevel(logging.WARN)

# List of tweets used in annotation guidelines
unused_tweet_ids = [1571501207822155777,
                    948614822324826112,
                    1566367589789569024,
                    1574117107134087170,
                    1574073508736425988,
                    1575046379621449728,
                    1574735036003352577,
                    1573970692697198592]


def extract_tweets(filename, n, prev=None):
    """ Extracts tweets containing expression in _expressions_ _n_ times """
    # Create list of expressions
    with open(filename, 'r') as f:
        expressions = [x.rstrip() for x in f]

    # Create list of unwanted tweets in dataset
    if prev is not None:
        with open(prev, 'r') as f:
            prev = [x.rstrip() for x in f]
            print(prev)
            prev = [int(re.search(r"[0-9]+", i).group(0)) for i in prev]
            prev += unused_tweet_ids
    else:
        prev = unused_tweet_ids

    # Create dataset folders
    if not os.path.exists("dataset"): os.mkdir("dataset")
    dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    assert not os.path.exists(f"dataset/{dt}")
    os.mkdir(f"dataset/{dt}")
    os.mkdir(f"dataset/{dt}/training")

    # Search for tweets; extract them if certain conditions aren't met
    for word in expressions:
        logging.warning(f"Searching tweets for {word}")
        i = 1
        for tweet in sntwitter.TwitterSearchScraper(word).get_items():
            if i > n:
                break
            # Because snscrape includes user as part of matching result, one
            # also needs to explicitely search the tweet content so that the
            # query match.
            elif re.search(word, tweet.renderedContent):
                # NOTE: This language check is performed automatically on
                #       Twitter's side, which could lead to false negatives.
                if tweet.lang == "sv":
                    # if current tweet is in list of unwanted tweets, skip
                    if tweet.id in prev: continue
                    print(tweet.renderedContent)
                    root = ET.Element("tweet")
                    root.set("id", str(tweet.id))
                    root.set("word", word)
                    root.set("date", str(tweet.date))
                    root.set("url", str(tweet.url))
                    root.set("annotation", "NULL")
                    content = ET.SubElement(root, "content")
                    content.text = str(tweet.renderedContent)
                    tree = ET.ElementTree(root)
                    filename = f"dataset/{dt}/training/{tweet.id}.xml"
                    with open(filename, 'wb') as export:
                        logging.info(f"Writing XML for {filename}")
                        tree.write(export)
                    i += 1


def search_tweets(word, n=10):
    """ Searches tweets using word and prints n results """
    i = 1
    for tweet in sntwitter.TwitterSearchScraper(word).get_items():
        if i > n:
            break
        if re.search(word, tweet.renderedContent):
            if tweet.lang == "sv":
                print(f"{tweet.url}: {tweet.renderedContent}")
                print()
                i += 1


if __name__ == "__main__":
    if len(sys.argv) not in [3, 4]:
        print("ERROR: must have only one/two arguments")
        sys.exit(1)
    try:
        extract_tweets(sys.argv[1], n=int(sys.argv[2]), prev=sys.argv[3])
    except IndexError:
        extract_tweets(sys.argv[1], n=int(sys.argv[2]))
