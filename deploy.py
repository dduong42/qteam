#!/usr/bin/env python3
"""
Upload index.html to using the FTP server.
"""
from concurrent.futures import ThreadPoolExecutor
from ftplib import FTP

import os
import os.path

os.chdir("src")
with open(os.path.join(os.environ["HOME"], ".qteam")) as f1:
    host = f1.readline()[:-1]
    user = f1.readline()[:-1]
    password = f1.readline()[:-1]

    def deploy(path: str):
        with FTP(host, user, password) as ftp, open(path, "rb") as f2:
            ftp.cwd("www")
            ftp.storbinary(f"STOR {path}", f2)

    with ThreadPoolExecutor() as executor:
        executor.submit(deploy, "index.html")
        executor.submit(deploy, "en.html")
        executor.submit(deploy, "styles.css")
