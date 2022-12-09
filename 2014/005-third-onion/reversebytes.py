#!/usr/bin/env python3

with open("server-status.jpg", "rb") as s1, open("server-status-reversed.jpg", "wb") as r:
    data = s1.read()
    for b in data[::-1]:
        r.write(b.to_bytes(1, 'big'))
