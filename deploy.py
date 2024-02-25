#!/usr/bin/env python3
"""
Deploy using the FTP server.
"""
import getpass
import ftplib
import os
import os.path

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

os.chdir("src")
with ftplib.FTP(host, user, password) as ftp:
    ftp.set_debuglevel(1)
    ftp.cwd("www")

    def deploy():
        with os.scandir(".") as it:
            for entry in it:
                if entry.is_dir():
                    try:
                        ftp.cwd(entry.name)
                    except ftplib.error_perm as reason:
                        if str(reason)[:3] == '550':
                            ftp.mkd(entry.name)
                            ftp.cwd(entry.name)
                        else:
                            raise
                    os.chdir(entry.name)
                    deploy()
                    os.chdir("..")
                    ftp.cwd("..")
                else:
                    with open(entry.name, "rb") as f2:
                        ftp.storbinary(f"STOR {entry.name}", f2)
    deploy()
