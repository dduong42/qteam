#!/usr/bin/env python3
"""
Upload index.html to using the FTP server.
"""
from ftplib import FTP

import os
import os.path


with open(os.path.join(os.environ["HOME"], ".qteam")) as f1:
    host = f1.readline()[:-1]
    user = f1.readline()[:-1]
    password = f1.readline()[:-1]

    with FTP(host, user, password) as ftp, open("src/index.html", "rb") as f2:
        ftp.cwd("www")
        ftp.storbinary("STOR index.html", f2)
