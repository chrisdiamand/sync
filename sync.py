#!/usr/bin/env python3

import argparse
import getpass
import os
import syncfile
import target
import sys

def parse_args():
    descr = "Sync stuff - a frontend for unison and rsync."
    p = argparse.ArgumentParser(description = descr)
    p.add_argument("syncfile", type = argparse.FileType("r"))
    p.add_argument("target", type = str)
    return p.parse_args()

def unison(t1, t2, sf):
    cmd = ["unison", "-root", t1.unison(), "-root", t2.unison()]
    cmd += ["-times", "false"]
    cmd += ["-auto"]
    cmd += ["-perms", "0"]
    cmd += ["-fastcheck", "true"]
    for i in sf.glob(t1.unison()):
        cmd += ["-path", i]
    for i in sf.ignore_paths:
        cmd += ["-ignore", "Path " + i]
    for i in sf.ignore_names:
        cmd += ["-ignore", "Name " + i]
    print(" ".join(cmd))

def main():
    args = parse_args()

    sf = syncfile.SyncFile(args.syncfile)
    t2 = target.parse(args.target)

    sf.display()
    print("Target:", t2)
    print()

    first_root = os.path.join("/home", getpass.getuser())
    t1 = target.parse(first_root)

    unison(t1, t2, sf)

if __name__ == "__main__":
    main()
