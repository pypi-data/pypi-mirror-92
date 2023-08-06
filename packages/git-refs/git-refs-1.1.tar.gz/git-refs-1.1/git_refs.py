#!/usr/bin/env python3
# Author    : weaming
# Mail      : garden.yuen@gmail.com
# Created   : 2021-01-21 18:37:09

import sys, os
from git import Repo

CSV = bool(os.getenv("CSV"))


def myprint(*args):
    if CSV:
        print(",".join(str(x) for x in (list(args)+['']*(5-len(args)))))
    else:
        print(*args)


def main():
    path = (sys.argv + ["."])[1]
    if not os.path.isdir(os.path.join(path, ".git")):
        print(f"{path} is not git repo root directory")
        sys.exit(1)

    r = Repo(path)
    if CSV:
        print("where,type,name,sha,remote")

    for x in r.tags:
        myprint("local", "tag", x.name, x.commit.hexsha)
    for x in r.branches:
        tb = x.tracking_branch()
        if tb:
            if CSV:
                myprint("local", "branch", x.name, x.commit.hexsha, tb.name)
            else:
                myprint("local", "branch", x.name, x.commit.hexsha, "->", tb.name)
        else:
            myprint("local", "branch", x.name, x.commit.hexsha, "", "")

    for remote in r.remotes:
        for ref in remote.refs:
            remote_hexsha = ""
            try:
                ref.ref
            except TypeError as e:
                remote_hexsha = str(e).rsplit("to", 1)[1].strip(" '")
            myprint("remote", "reference", ref.remote_head, remote_hexsha, remote.name)


if __name__ == "__main__":
    main()
