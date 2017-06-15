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


class FileHasher:

    def __init__(self):
        pass

    @staticmethod
    def Getsize(infile):
        try:
            units = {0: 'bytes', 1: 'Kbytes', \
            2: 'Mbytes', 3: 'Gbytes', 4: 'Tbytes'}
            size = os.path.getsize(infile)
            i = 0
            while size > 1000:
                size = size / 1000
                i += 1
            return '%s %s' % (size, units[i])
        except:
            pass

    @staticmethod
    def Base32(text):
        encoded = base64.b32encode(text)
        return encoded.decode('utf-8')

    @staticmethod
    def Base64(text):
        encoded = base64.b64encode(text)
        return encoded.decode('utf-8')

    @staticmethod
    def Base85(text):
        encoded = base64.b85encode(text)
        return encoded.decode('utf-8')

    @staticmethod
    def handledirectory(path):
        for (dirpath, _, filenames) in os.walk(path):
            for filename in filenames:
                yield os.path.join(dirpath, filename)

    @staticmethod
    def Checksum(infile, method, format):
        try:
            BUF_SIZE = 65536
            hasher = None
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
            if format == 'HEX':
                return (os.path.realpath(infile), FileHasher.Getsize(infile), method,
                        hasher.hexdigest(), '_' * 58)
            elif format == 'Base32':
                return (os.path.realpath(infile), FileHasher.Getsize(infile), method,
                        FileHasher.Base32(hasher.digest()), '_' * 58)
            elif format == 'Base64':
                return (os.path.realpath(infile), FileHasher.Getsize(infile), method,
                        FileHasher.Base64(hasher.digest()), '_' * 58)
            elif format == 'Base85':
                return (os.path.realpath(infile), FileHasher.Getsize(infile), method,
                        FileHasher.Base85(hasher.digest()), '_' * 58)
        except:
            pass

if __name__ == '__main__':
    init(autoreset=True)
    files = 0
    print(Fore.LIGHTYELLOW_EX + '[Info] FileHasher by sepehrdad sh')
    parser = argparse.ArgumentParser()
    parser.add_argument('method', type=str, choices=['SHA1', 'SHA256', 'SHA512', 'MD5'], help='Hashing method to use')
    parser.add_argument('format', type=str, choices=['HEX', 'Base32', 'Base64', 'Base85'], help='Output format')
    parser.add_argument('files', nargs='+', help='File/s to hash')
    args = parser.parse_args()
    start_time = time.time()
    for i in args.files:
        if os.path.isfile(i):
            try:
                print(Fore.GREEN + '\n   %s %s %s' % ('_' * 20, '[New File Hashed]', '_' * 20) + Fore.YELLOW
                      + '\n\n   File Name: %s\n   File Size: %s\n   %s: %s\n   %s'
                      % (FileHasher.Checksum(i, args.method, args.format)))
                files += 1
            except:
                continue
        elif os.path.isdir(i):
            filelist = FileHasher.handledirectory(i)
            try:
                for x in filelist:
                    print(Fore.GREEN + '\n   %s %s %s' % ('_' * 20, '[New File Hashed]', '_' * 20) + Fore.YELLOW
                          + '\n\n   File Name: %s\n   File Size: %s\n   %s: %s\n   %s'
                          % (FileHasher.Checksum(x, args.method, args.format)))
                    files += 1
            except:
                continue
        else:
            pass
    elapsed_time = time.time() - start_time
    print(Fore.GREEN + '\n[+] Files: %s' % files)
    print(Fore.GREEN + '[+] Elapsed time: %s' % elapsed_time)
