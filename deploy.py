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


def cd(ftp: ftplib.FTP, path: str):
    dirs = path.split(os.sep)
    for d in dirs:
        try:
            ftp.cwd(d)
        except ftplib.error_perm as reason:
            if str(reason)[:3] == '550':
                ftp.mkd(d)
                ftp.cwd(d)
            else:
                raise


def mkdir(path: str):
    with ftplib.FTP(host, user, password) as ftp:
        ftp.set_debuglevel(1)
        head, tail = os.path.split(path)
        cd(ftp, head)
        try:
            ftp.mkd(tail)
        except ftplib.error_perm as reason:
            if str(reason)[:3] != '550':
                raise


def put(path: str):
    with ftplib.FTP(host, user, password) as ftp:
        ftp.set_debuglevel(1)
        head, tail = os.path.split(path)
        cd(ftp, head)
        with open(path, "rb") as f:
            ftp.storbinary(f"STOR {tail}", f)


with ThreadPoolExecutor() as executor:
    def deploy(path: str):
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_dir():
                    executor.submit(mkdir, entry.path)
                    deploy(entry.path)
                else:
                    executor.submit(put, entry.path)
    deploy("www")
