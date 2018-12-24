#!/usr/bin/env python3

from sys import maxsize
import subprocess

# There is similar code in ./debian/postinst. If you are changing this
# you probably want to change that too.
def download_xflux():
    # Determines which is the appropriate executable for 32-bit
    if maxsize == 2**31 - 1:
        print("Downloading 32-bit xflux ...")
        urls = ["https://justgetflux.com/linux/xflux-pre.tgz"]
    elif maxsize == 2**63 - 1:
        print("Downloading 64-bit xflux ...")
        urls = ["https://justgetflux.com/linux/xflux64.tgz",
                "https://justgetflux.com/linux/xflux11.tgz",
                "https://justgetflux.com/linux/xflux12.tgz"]
    else:
        raise Exception("Unexpected maxsize = %i!" % maxsize)
    for url in urls:
        tarchive = "/tmp/xflux.tgz"
        subprocess.call(['wget', url, '-O', tarchive])
        subprocess.call(['tar', '-xvf', tarchive])

if __name__ == '__main__':
    download_xflux()
