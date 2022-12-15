#!/usr/bin/env python3

import os
import cgi
import cgitb

form = cgi.FieldStorage()
file = form['filename']

if file.filename:
    # block directory traversal and strip path
    filename = os.path.basename(file.filename).replace("\\", "/")
    open(f"/sandox/{filename}", "wb").write(file.file.read())
    message = "File received successfully"
else:
    message = "No file was uploaded"

print(f"""\
Content-Type: text/html\n
<html>
<body>
  <p>%s</p>
</body>
</html>
""" % message)
