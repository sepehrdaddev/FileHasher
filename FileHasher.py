#!/usr/bin/python
##############################################################################
#                                                                            #
#                               By Sepehrdad Sh                              #
#                                                                            #
##############################################################################

import sys
import os
import hashlib
import base64
import time
import argparse
from colorama import *


def Handler(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            func(*args, **kwargs)
        except Exception as error:
            print(Fore.RED + '\n[-] Error : %s' % error)
        elapsed_time = time.time() - start_time
        print(Fore.GREEN + '[+] Elapsed time: %s' % elapsed_time)
    return wrapper


def Getsize(infile):
    units = {0: 'bytes', 1: 'Kbytes', \
    2: 'Mbytes', 3: 'Gbytes', 4: 'Tbytes'}
    size = os.path.getsize(infile)
    i = 0
    while size > 1000:
        size = size / 1000
        i += 1
    return '%s %s' % (size, units[i])


def Base32(text):
    encoded = base64.b32encode(text)
    return encoded.decode('utf-8')


def Base64(text):
    encoded = base64.b64encode(text)
    return encoded.decode('utf-8')


def Base85(text):
    encoded = base64.b85encode(text)
    return encoded.decode('utf-8')


def handledirectory(path):
    for (dirpath, _, filenames) in os.walk(path):
        for filename in filenames:
            yield os.path.join(dirpath, filename)


def Checksum(infile, method, type):
    BUF_SIZE = 65536
    hasher = None
    hashed = None
    if method == 'SHA1':
        hasher = hashlib.sha1()
    elif method == 'SHA256':
        hasher = hashlib.sha256()
    elif method == 'SHA512':
        hasher = hashlib.sha512()
    elif method == 'MD5':
        hasher = hashlib.md5()
    with open(infile, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            hasher.update(data)
    if type == 'HEX':
        hashed = hasher.hexdigest()
    elif type == 'Base32':
        hashed = Base32(hasher.digest())
    elif type == 'Base64':
        hashed = Base64(hasher.digest())
    elif type == 'Base85':
        hashed = Base85(hasher.digest())

    return (os.path.realpath(infile), Getsize(infile), method,
            hashed, '_' * 59)


@Handler
def main():
    files = 0
    print(Fore.LIGHTYELLOW_EX + '[Info] FileHasher by Sepehrdad Sh')
    parser = argparse.ArgumentParser()
    parser.add_argument('method', type=str, choices=['SHA1', 'SHA256', 'SHA512', 'MD5'], help='Hashing method to use')
    parser.add_argument('format', type=str, choices=['HEX', 'Base32', 'Base64', 'Base85'], help='Output format')
    parser.add_argument('files', nargs='+', help='File/s to hash')
    args = parser.parse_args()
    for i in args.files:
        if os.path.exists(i):
            if os.access(i, os.R_OK):
                if os.path.isfile(i):
                    try:
                        print(Fore.GREEN + '\n   %s %s %s' % ('_' * 20, '[New File Hashed]', '_' * 20) + Fore.YELLOW
                              + '\n\n   File Name: %s\n   File Size: %s\n   %s: %s\n   %s'
                              % (Checksum(i, args.method, args.format)))
                        files += 1
                    except:
                        continue
                elif os.path.isdir(i):
                    filelist = handledirectory(i)
                    try:
                        for x in filelist:
                            if os.access(x, os.R_OK):
                                print(Fore.GREEN + '\n   %s %s %s' % ('_' * 20, '[New File Hashed]', '_' * 20)
                                      + Fore.YELLOW + '\n\n   File Name: %s\n   File Size: %s\n   %s: %s\n   %s'
                                      % (Checksum(x, args.method, args.format)))
                                files += 1
                            else:
                                print(Fore.RED + '[-] Unable to access: %s' % os.path.realpath(x))
                    except:
                        continue
            else:
                print(Fore.RED + '[-] Unable to access: %s' % os.path.realpath(i))
        else:
            print(Fore.RED + '[-] Unable to find: %s' % i)
    print(Fore.GREEN + '\n[+] Files: %s' % files)
if __name__ == '__main__':
    init(autoreset=True)
    main()
