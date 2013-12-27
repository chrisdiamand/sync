#!/usr/bin/env python3

import glob
import os
import subprocess
from syncfile import SyncFile
import sys

# Return the IP address if it can be turned into one,
# otherwise return None.
def is_ip_addr(dst):
    assert type(dst) == str

    if len(dst) <= 3 and dst.isdigit(): # It's a single number
        return "192.168.245." + dst

    if dst.count(".") != 3:
        return None

    for i in dst:
        if not (i.isdigit() or i == "."):
            return None
    return dst # It's a valid entire IP address

def is_mounted(ip):
    procmounts = open("/proc/mounts", "r")
    for i in procmounts:
        i = i.strip()
        fields = i.split()
        mount_src = "root@" + ip + ":/"
        if mount_src == fields[0]:
            procmounts.close()
            return fields[1]
    procmounts.close()
    return None

def create_mountpoint():
    n = 0
    while True:
        mp = os.path.expanduser("~/mp" + str(n))
        if os.path.exists(mp):
            if os.path.isdir(mp) and not os.path.ismount(mp):
                if not os.listdir(mp): # Check it's empty
                    return mp
        else:
            print("Does not exist:", mp)
            try:
                os.makedirs(mp)
            except FileExistsError:
                subprocess.call(["fusermount", "-u", mp])
            return mp

# See if the mountpoint has been mounted but then
# expired. When this happens there is a "Transport
# endpoint is not connected" error.
def endpoint_not_connected(mp):
    out = subprocess.check_output(["ls", mp])
    errmsg = "ls: cannot access " + mp + ": Transport endpoint is not connected"
    if out.strip() == errmsg:
        return True
    return False

def mount(ip):
    mp = is_mounted(ip)
    if mp != None: # It's already mounted
        print("%s already mounted at %s" % (ip, mp))
        if endpoint_not_connected(mp):
            print("But endpoint not connected: Unmounting.")
            subprocess.call(["fusermount", "-u", mp])
        else:
            return mp

    mp = create_mountpoint()

    mnt = ["sshfs", "root@" + ip + ":/", mp]
    mnt += ["-o", "ConnectTimeout=20"]
    print("Mounting", ip, "on", mp)
    retcode = subprocess.call(mnt)
    print("Done.")
    if retcode != 0:
        print("Error: Could not mount", ip, "on", mp)
        os.removedirs(mp)
        sys.exit(retcode)
    return mp

# Check that dst exists and is a directory, or is an
# IP address, in which case mount it using sshfs
def check_exists_or_ip(dst):
    if not os.path.exists(dst):
        ip = is_ip_addr(dst)
        if ip != None:
            mp = mount(ip)
            dst = os.path.join(mp, "storage/emulated/legacy")
        else:
            print("Error: " + dst + " does not exist.")
            sys.exit(1)

    else: # The path exists - check it's a directory
        if not os.path.isdir(dst):
            print("Error: " + dst + " exists but is not a directory")
            sys.exit(1)

    return dst

###################################################

SYNCFILE = os.path.expanduser("~/.phonesync.txt")

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " MOUNTPOINT/IP")
    sys.exit(1)

mountpoint = None
dst = check_exists_or_ip(sys.argv[1])

home = os.path.expanduser("~")
cmd = ["unison", "-fat", "-fastcheck", "true", "-dumbtty", "-root", home, "-root", dst, "-auto"]

sf = SyncFile(SYNCFILE)
filenames = sf.glob(home)
for f in filenames:
    cmd += ["-path", f]

print("Starting unison...")
try:
    subprocess.call(cmd)
except KeyboardInterrupt:
    print("Interrupted, exiting.")
    sys.exit(1)
print("Done.");
