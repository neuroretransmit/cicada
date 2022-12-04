#!/usr/bin/env python3

import json

from datetime import datetime
from time import mktime
from time import gmtime, strptime

def delta(t1, t2):
    t1 = t1.replace("T","-").replace(".000Z", "")
    t2 = t2.replace("T","-").replace(".000Z", "")
    t1 = datetime.strptime(t1, "%Y-%m-%d-%H:%M:%S")
    t2 = datetime.strptime(t2, "%Y-%m-%d-%H:%M:%S")
    return abs(int((t1-t2).total_seconds()))

tweets = []
with open("./tweets/0.json") as zero:
    with open("./tweets/1.json") as one:#cool
        zero_json = json.load(zero)
        one_json = json.load(one)
        for _json in [zero_json, one_json]:
            for tweet in _json["data"]:
                tweets.append(tweet)

last = None
for tweet in sorted(tweets, key=lambda t: t["created_at"]):
    if last:
        now = tweet["created_at"]
        print(f"{delta(now, last) / 60} seconds")
        last = now
    else:
        last = tweet["created_at"]
print(f"num tweets: {len(tweets)-3}")
