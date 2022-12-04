#!/usr/bin/env python3

import json
import datetime as dt

SUBREDDIT_JSON = "./a2e7j6ic78h0j-posts.json"
BOOK_CODE = "../001-final.jpg/outguess.txt"
TITLES = "./plaintext.txt"

authors = dict()
posts_with_comments = list()
titles = list()
anomalies = list()
images = list()

with open(SUBREDDIT_JSON, 'r') as f:
    posts = json.load(f)
    posts["data"] = sorted(posts["data"], key=lambda x: x["created_utc"])

    for post in posts["data"]:
        author = post["author"]
        url = post["url"]
        created = post["created_utc"]
        title = post["title"]
        num_comments = post["num_comments"]

        if author not in authors:
            authors[author] = list()
            authors[author].append(post)
            if "deleted" in author:
                anomalies.append((author, url, created, title))
                continue
        if url.endswith(".jpg") or url.endswith(".png"):
            images.append((author, title, url, created))
            dup = False
            for image in images:
                if image[1] == title and image[0] != author:
                    dup = True
                    break
            if dup:
                anomalies.append((author, url, created, title))
            titles.append((title, url, False, created))
            continue
        if num_comments > 0:
            posts_with_comments.append(url)
        show = True
        # not fast search for existing title
        for t in titles:
            if t[0] == title:
                show = False
                break
        if not show:
            anomalies.append((author, url, created, title))
        titles.append((title, url, show, created))

with open("ciphertext.txt", "w") as of:
    for title in titles:
        if title[2]:
            of.write(title[0].strip() + "\n")

print("\nIMAGES")
for image in images:
    print("\t" + image[0], image[1], image[2], dt.datetime.fromtimestamp(image[3]))

print("\nANOMALIES (Posts created after original with same title)")
for anomaly in anomalies:
    orig = next(p for p in posts["data"] if p["title"] == anomaly[3])
    #print("\t" + anomaly[0], anomaly[3], anomaly[1], 'created: {}'.format(dt.datetime.fromtimestamp(anomaly[2])))
    print('\tupdated:\n\t\t{}\n\t\t{}\n\t\t{}\n\t\t{}'.format(anomaly[0], dt.datetime.fromtimestamp(anomaly[2]), anomaly[3], anomaly[1]))
    print('\toriginal:\n\t\t{}\n\t\t{}\n\t\t{}\n\t\t{}\n'.format(orig["author"], dt.datetime.fromtimestamp(orig["created_utc"]), orig["title"], orig["url"]))

print("\nPOSTS WITH COMMENTS")
for post in posts_with_comments:
    print("\t" + post)

print("\nAUTHORS")
for author in authors.keys():
    print("\t" + author)

with open("./ciphertext.txt", "r") as file:
	post_titles = file.read().upper()
	# TODO: Merge in key creation program
	vignere_key = [10, 2, 14, 7, 19, 6, 18, 12, 7, 8, 17, 0, 19, 7, 14, 18, 14, 19, 13, 0, 1, 2, 0] # the key
	plaintext = ''
	i = 0
	
	for char in post_titles:
	    # Reset key on New Line or wrap
	    if i >= len(vignere_key) or ord(char) == 10:
	        i = 0
	    # if character is out of bounds, Num, punctuation etc... add it to the finalString and skip translation
	    if char > 'Z' or char < 'A':
	        plaintext += char
	        continue
	    # get the character in ASCII
	    ascii_code = ord(char)
	    # Shift it by the key
	    new_char = ascii_code - vignere_key[i]
	    # if it's too big subtract the number of letters in the alphabet (Wrap)
	    if new_char > ord('Z'):
	        new_char = new_char - 26
	    # if it's too small add the number of letters in the alphabet (Wrap)
	    if new_char < ord('A'):
	        new_char = new_char + 26
	    # Add the character to the finalString
	    plaintext += chr(new_char)
	    # next value in key
	    i += 1

with open(TITLES, "w") as of:
    of.write(plaintext)

with open(BOOK_CODE, "r") as book_code:
    bc = [c for c in book_code.read().split("\n") if not "http" in c and ":" in c ]
    message = ''
    with open(TITLES, "r") as titles:
        t = [t for t in titles.read().split("\n")]
        for l in bc:
            ref = l.split(":")
            line = int(ref[0]) - 1
            col = int(ref[1]) - 1
            message += t[line][col]
