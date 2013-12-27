#!/usr/bin/env python3

import glob as glob_module
import os
import sys

def count_leading_whitespace(text):
    c = 0
    for i in text:
        if i == " ":
            c += 1
        elif i == "\t":
            print("Error: Tabs used to indent syncfile")
            sys.exit(1)
        else:
            break
    return c

def syncfile_level(ret_list, lines, pos, parentpath):
    assert type(ret_list) == list
    assert type(lines) == list
    assert type(pos) == int
    assert type(parentpath) == str

    if pos >= len(lines):
        return pos

    while pos < len(lines):
        cur_line = lines[pos]
        cur_il = count_leading_whitespace(cur_line)
        path = os.path.join(parentpath, cur_line.strip())

        if pos < len(lines) - 1:
            next_line = lines[pos + 1]
            next_il = count_leading_whitespace(next_line)

            if next_il > cur_il:
                pos = syncfile_level(ret_list, lines, pos + 1, path)
            else:
                ret_list.append(path)

            if cur_il > next_il:
                break
        else: # We are at the last entry
            ret_list.append(path)

        pos += 1

    return pos

class SyncFile:
    def __init__(self, sync_fname):
        self.includes = []
        self.excludes = []
        self.fname = None
        self.read(sync_fname)

    def read(self, fp):
        syncfile = None
        if type(fp) == str:
            syncfile = open(self.fname, "r")
            self.fname = fp
        else:
            syncfile = fp
            self.fname = fp.name
        lines = syncfile.readlines()
        syncfile.close()

        self.includes = []
        syncfile_level(self.includes, lines, 0, "")

    # Expand all wildcards
    def glob(self, root):
        filenames = []
        for p in self.includes:
            searchpath = os.path.join(root, p)
            matches = glob_module.glob(searchpath)
            for match in matches:
                filenames.append(os.path.relpath(match, start = root))
        return filenames

def main():
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "SYNC_FILE")
        sys.exit(1)

    sync = SyncFile(sys.argv[1])
    for i in sync.includes:
        print(i)

if __name__ == "__main__":
    main()
