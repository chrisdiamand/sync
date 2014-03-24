#!/usr/bin/env python3

import ipparse
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

    def rsync(self):
        return self.localdir

    def unison(self):
        return self.localdir

    def __repr__(self):
        return self.localdir

class RemoteTarget(Target):
    def __init__(self, tgt):
        Target.__init__(self, tgt)
        self.parse()

    def parse(self):
        [self.user, self.ip] = ipparse.parse_dest(self.target)

    def rsync(self):
        ret = self.user + "@" + self.ip
        ret += os.path.join(":", "home", self.user)
        return ret

    def unison(self):
        ret = "ssh://" + self.user + "@" + self.ip
        ret += "/" + os.path.join("/home", self.user)
        return ret

    def __repr__(self):
        return self.user + "@" + self.ip
