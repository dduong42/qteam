#!/usr/bin/env python3
"""
Deploy using the FTP server.
"""
import ftplib
import os
import os.path

os.chdir("src")
with open(os.path.join(os.environ["HOME"], ".qteam")) as f1:
    host = f1.readline()[:-1]
    user = f1.readline()[:-1]
    password = f1.readline()[:-1]

    with ftplib.FTP(host, user, password) as ftp:
        ftp.set_debuglevel(1)
        ftp.cwd("www")

        def deploy():
            for entry in os.scandir("."):
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
