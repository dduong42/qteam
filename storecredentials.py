#!/usr/bin/env python3
"""
Store the credentials in ~/.qteam
"""
import getpass
import os
import os.path

os.umask(0o77)
with open(os.path.join(os.environ["HOME"], ".qteam"), "w") as f:
    f.write(input("Host: "))
    f.write("\n")
    f.write(input("User: "))
    f.write("\n")
    f.write(getpass.getpass())
    f.write("\n")
