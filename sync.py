#!/usr/bin/env python3

import argparse
from syncfile import SyncFile
import target
import sys

def parse_args():
    descr = "Sync stuff - a frontend for unison and rsync."
    p = argparse.ArgumentParser(description = descr)
    p.add_argument("syncfile", type = argparse.FileType("r"))
    p.add_argument("target", type = str)
    return p.parse_args()

def main():
    args = parse_args()

    sf = SyncFile(args.syncfile)
    print("Parsing '" + args.target + "'")
    t = target.parse(args.target)

    print("Includes:")
    for i in sf.includes:
        print("  " + i)
    print("Target:", t)


if __name__ == "__main__":
    main()
