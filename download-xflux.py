from sys import maxsize, version_info

if version_info[0] == 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve

import tarfile

# There is similar code in ./debian/postinst. If you are changing this
# you probably want to change that too.
def download_xflux():
    # Determines which is the appropriate executable for 32-bit
    if maxsize == 2147483647:
        print("Downloading 32-bit xflux ...")
        url = "https://justgetflux.com/linux/xflux-pre.tgz"
    elif maxsize == 9223372036854775807:
        print("Downloading 64-bit xflux ...")
        url = "https://justgetflux.com/linux/xflux64.tgz"
    tarchive = "/tmp/xflux.tgz"
    
    # use python's builtins methods to eliminate external program
    # dependencies for manual install
    # in case internet connection isn't available to download wget
    # & not every linux system (minimal) has wget (nor curl) preinstalled.
    urlretrieve(url, tarchive)

    print("Extracting {} ...".format(tarchive))
    tar = tarfile.open(tarchive)
    tar.extractall()
    tar.close()

if __name__ == '__main__':
    download_xflux()
