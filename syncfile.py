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

def syncfile_level(sf, lines, pos, parentpath):
    assert type(sf) == SyncFile
    assert type(lines) == list
    assert type(pos) == int
    assert type(parentpath) == str

    if pos >= len(lines):
        return pos

    while pos < len(lines):
        cur_line = lines[pos]
        if cur_line.isspace() or cur_line == "":
            pos += 1
            continue

        cur_il = count_leading_whitespace(cur_line)
        path = os.path.join(parentpath, cur_line.strip())

        if pos < len(lines) - 1:
            next_line = lines[pos + 1]
            next_il = count_leading_whitespace(next_line)

            if next_il > cur_il:
                pos = syncfile_level(sf, lines, pos + 1, path)
            else:
                sf.add(path)

            if cur_il > next_il:
                break
        else: # We are at the last entry
            sf.add(path)

        pos += 1

    return pos

def remove_comments(lines):
    i = 0
    while i < len(lines):
        # Remove the '\n' from every line
        line = lines[i].rstrip()
        pos = line.find("#")
        if pos != -1:
            line = line[0:pos] # Remove the comment
        lines[i] = line
        i += 1

class SyncFile:
    def __init__(self, sync_fname):
        self.includes = []
        self.ignore_paths = []
        self.ignore_names = []
        self.fname = None
        self.read(sync_fname)

    # Add an entry from a syncfile
    def add(self, path):
        assert type(path) == str
        print("Adding", path)
        if path.startswith("IGNORE_PATH:/"):
            self.ignore_paths.append(path[13:])
        elif path.startswith("IGNORE_NAME:/"):
            self.ignore_names.append(path[13:])
        else:
            print("INCLUDE:", path)
            self.includes.append(path)

    def read(self, fp):
        syncfile = None
        if type(fp) == str:
            syncfile = open(self.fname, "r")
            self.fname = fp
        else:
            syncfile = fp
            self.fname = fp.name
        lines = syncfile.readlines()
        remove_comments(lines)
        syncfile.close()

        self.includes = []
        syncfile_level(self, lines, 0, "")

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
