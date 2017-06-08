#!/usr/bin/python
##############################################################################
#                                                                            #
#                               By Sepehrdad Sh                              #
#                                                                            #
##############################################################################

import sys
import os
import hashlib
import time
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
    def Checksum(infile):
        try:
            BUF_SIZE = 65536
            md5 = hashlib.md5()
            sha1 = hashlib.sha1()
            sha256 = hashlib.sha256()
            with open(infile, 'rb') as f:
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    md5.update(data)
                    sha1.update(data)
                    sha256.update(data)
            return os.path.realpath(infile), \
            FileHasher.Getsize(infile),\
             md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest(), '_' * 58
        except:
            pass

if __name__ == '__main__':
    init(autoreset=True)
    files = 0
    print(Fore.LIGHTYELLOW_EX + '[Info] FileHasher by sepehrdad sh')
    start_time = time.time()
    if len(sys.argv[1:]) < 1:
        print(Fore.RED + '[-] No input selected')
        print(Fore.LIGHTYELLOW_EX + 'Usage: FileHasher <filename/s>')
    else:
        for i in sys.argv[1:]:
            if os.path.isfile(i):
                try:
                    print(Fore.GREEN + '\n   %s %s %s' % ('_' * 20, '[New File Hashed]', '_' * 20) + Fore.YELLOW
                          + '\n   |File Name: %s\n   |File Size: %s\n   |MD5: %s\n   |SHA1: %s\n   |SHA256: %s\n   |%s'
                          % (FileHasher.Checksum(i)))
                    files += 1
                except:
                    continue
            else:
                pass
    elapsed_time = time.time() - start_time
    print(Fore.GREEN + '\n[+] Files: %s' % files)
    print(Fore.GREEN + '[+] Elapsed time: %s' % elapsed_time)
