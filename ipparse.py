#!/usr/bin/env python3

import getpass
import os
import subprocess
import sys

class InvalidRootError(Exception):
    pass

def get_best_interface():
    import getip
    ifs = getip.get_interfaces(ign_loopback = True, ign_public = True)
    if len(ifs) > 0:
        return ifs[0]
    ifs = getip.get_interfaces(ign_loopback = True)
    if len(ifs) > 0:
        return ifs[0]
    print("Error: Cannot complete IP address: No network interfaces")
    sys.exit(1)

# Return a complete IP address based on the last part
def complete_IP(partial):
    ip = get_best_interface().ip
    ip.parts[3] = int(partial)
    return str(ip)

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
    print("Run sync.py instead.")
    sys.exit(1)

if __name__ == "__main__":
    main()
