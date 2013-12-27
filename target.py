#!/usr/bin/env python3

import os

def parse(tgt):
    if os.path.isdir(tgt):
        return LocalTarget(tgt)
    else:
        return RemoteTarget(tgt)

class Target:
    def __init__(self, tgt):
        self.target = tgt
    def unison(self):
        return None
    def rsync(self):
        return None
    def __repr__(self):
        return "<?>"

class LocalTarget(Target):
    def __init__(self, tgt):
        Target.__init__(self, tgt)
        assert os.path.isdir(tgt)
        self.localdir = os.path.realpath(tgt)

    def __repr__(self):
        return self.localdir

class RemoteTarget(Target):
    def __init__(self, tgt):
        Target.__init__(self, tgt)
        self.parse()

    def parse(self):
        pass

    def __repr__(self):
        return "IP"
