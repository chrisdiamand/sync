#!/usr/bin/env python3

import getpass
import os
import subprocess
import sys

class InvalidRootError(Exception):
    pass

# Return a complete IP address based on the last part
def complete_IP(partial):
    import getip
    ifaces = getip.get_interfaces()
    complete = ifaces[0].ip
    parts = complete.split(".")
    parts[3] = partial
    return ".".join(parts)

# Parse a specification for the other root to be synced.
# Allow: 190 (infers username@123.456.789.190)
#        username@190
#        username@123.456.789.190
#        hostname
#        username@hostname
def parse_dest(dst):
    assert type(dst) == str
    user = host = ip = None

    # Extract the username if one was given
    parts = dst.split("@")
    if len(parts) == 2: # A username was provided
        user = parts[0]
        host = parts[1]
    elif len(parts) == 1: # Just a host was specified
        user = getpass.getuser()
        host = dst
    else: # Too many '@' symbols
        raise InvalidRootError()

    # Parse the rest of it
    if host.isalpha(): # It's a hostname
        ip = host
    else:
        parts = host.split(".")
        if len(parts) == 1: # Just the last part of the IP address
            ip = complete_IP(host)
        elif len(parts) == 4: # A whole IP address
            ip = host
        else: # Invalid IP address
            raise InvalidRootError()

    return user, ip

def main():
    user = ip = None
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " [USER@][IP_SUBNET].IP_HOST")
        sys.exit(1)

    root_spec = sys.argv[1]

    try:
        user, ip = parse_dest(root_spec)
    except InvalidRootError:
        print("Error: Invalid root '" + root_spec + "'")
        sys.exit(1)

    root1 = os.path.join("/home", getpass.getuser())
    root2 = "ssh://" + user + "@" + ip + "/" + os.path.join("/home", user)

    cmd = ["unison", "homesync", "-root", root1, "-root", root2]

    print(" ".join(cmd))
    subprocess.call(cmd)

if __name__ == "__main__":
    main()
