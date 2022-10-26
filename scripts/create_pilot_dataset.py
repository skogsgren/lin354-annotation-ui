import random
import os


tweets = [x for x in os.listdir("training")]
random.shuffle(tweets)
assert not os.path.exists("pilot_two")
os.mkdir("pilot_two")

i = 0
while i < 30:
    t = tweets.pop()
    os.rename("training/%s" %t, "pilot_two/%s" %t)
    i += 1
