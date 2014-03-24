#!/usr/bin/env python3

import argparse
import getpass
import os
import subprocess
import syncfile
import sys
import target

def parse_args():
    descr = "Sync stuff - a frontend for unison and rsync."
    p = argparse.ArgumentParser(description = descr)
    p.add_argument("syncfile", type = argparse.FileType("r"))
    p.add_argument("target", type = str)

    tofrom = p.add_mutually_exclusive_group(required = False)
    tofrom.add_argument("--oneway", "-o", action = "store_true")

    return p.parse_args()

# Print a command (array of strings) out in such a way that
# it can be copied-and-pasted back into the shell.
def printCommand(cmd, fp = sys.stdout):
    i = 0
    while i < len(cmd):
        s = cmd[i]
        if " " in s or "\t" in s:
            s = "'" + s + "'"
        fp.write(s)
        if i < len(cmd) - 1:
            fp.write(" ")
        i += 1
    fp.write("\n")

def unison(t1, t2, sf):
    cmd = ["unison", t1.unison(), t2.unison()]
    cmd += ["-dumbtty"]
    cmd += ["-times=false"]
    cmd += ["-auto"]
    cmd += ["-perms=0"]
    cmd += ["-fastcheck=true"]
    for i in sf.glob(t1.unison()):
        cmd += ["-path", i]
    for i in sf.ignore_paths:
        cmd += ["-ignore", "Path " + i]
    for i in sf.ignore_names:
        cmd += ["-ignore", "Name " + i]

    printCommand(cmd)
    print()
    try:
        #subprocess.call(cmd)
        pass
    except KeyboardInterrupt:
        sys.exit(1)

def rsync(src, dst, sf):
    cmd = ["rsync", "-avuR", "--delete"]
    for i in sf.glob(src.rsync()):
        print(i)
        cmd += [i]
    for i in sf.ignore_paths:
        cmd += ["--exclude", i]
    for i in sf.ignore_names:
        cmd += ["--exclude", i]
    cmd += [dst.rsync()]
    printCommand(cmd)
    try:
        subprocess.call(cmd)
    except KeyboardInterrupt:
        sys.exit(1)

def main():
    args = parse_args()

    sf = syncfile.SyncFile(args.syncfile)
    t2 = target.parse(args.target)

    sf.display()
    print()
    print("Target:", t2)
    print()

    first_root = os.path.join("/home", getpass.getuser())
    t1 = target.parse(first_root)

    if not args.oneway:
        unison(t1, t2, sf)
    else: # args.oneway
        rsync(t1, t2, sf)

if __name__ == "__main__":
    main()
