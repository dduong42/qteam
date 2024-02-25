#!/usr/bin/env python3
"""
Deploy using the FTP server.
"""
import getpass
import ftplib
import os
import os.path

from concurrent.futures import ThreadPoolExecutor

credentials_path = os.path.join(os.environ["HOME"], ".qteam")

# Try to create ~/.qteam
os.umask(0o77)
try:
    with open(credentials_path, "x") as f:
        host = input("Host: ")
        user = input("User: ")
        password = getpass.getpass()
        f.write(f"{host}\n{user}\n{password}\n")
except FileExistsError:
    with open(credentials_path) as f:
        host = f.readline()[:-1]
        user = f.readline()[:-1]
        password = f.readline()[:-1]


def put(path: str):
    with ftplib.FTP(host, user, password) as ftp:
        ftp.set_debuglevel(1)
        with open(path, "rb") as f:
            ftp.storbinary(f"STOR {path}", f)


with ThreadPoolExecutor() as executor, ftplib.FTP(host, user, password) as ftp:
    ftp.set_debuglevel(1)

    def deploy(path: str):
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_dir():
                    try:
                        ftp.mkd(entry.path)
                    except ftplib.error_perm as reason:
                        if str(reason)[:3] != '550':
                            raise
                    deploy(entry.path)
                else:
                    executor.submit(put, entry.path)
    deploy("www")
