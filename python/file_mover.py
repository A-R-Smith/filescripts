#!/usr/bin/env python
import time
import json
import os
import sys
import ntpath
import logging as log
import hashlib
import configparser
from shutil import copyfile


# strips the file name from the end of the full file path
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


# calculates the sha256 checksum from the file and compares to the sha256 file provided
def verify_sha256(filename):
    try:
        check_file = open(filename, 'rb')
        checksum = hash_bytestr_iter(file_as_blockiter(check_file), hashlib.sha256())
    except Exception:
        log.error("failed to create checksum from input file: " + filename)
        return False
    else:
        check_file.close()

    try:
        sha_file = open(filename + ".sha256", 'r')
        sha256 = sha_file.read().rstrip('\r\n')
    except Exception:
        log.error("failed to read checksum file: " + filename + ".sha256")
        return False
    else:
        sha_file.close()

    return checksum == sha256


# creates sha256 checksum
def hash_bytestr_iter(bytesiter, hasher, ashexstr=True):
    for block in bytesiter:
        hasher.update(block)
    return hasher.hexdigest() if ashexstr else hasher.digest()


# creates an iterator of file blocks
def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)


def process_file(filename):
    if has_sha25_file is True:
        verified = verify_sha256(filename)
    else:
        verified = True

    if verified:
        #to_file = destination_dir + path_leaf(filename)
        to_file = destination_dir + filename.replace(input_dir, "")

        log.info("moving file, from: " + filename + "   to: " + to_file)
        try:
            # os.makedirs(os.path.dirname(to_file), exist_ok=True)
            copyfile(filename, to_file)
        except Exception:
            log.error("failed to copy file to file share: " + filename)
            log.error(sys.exc_info()[0])

        if do_delete is True:
            log.info("deleting file: "+filename)
            os.remove(filename)
            if has_sha25_file:
                log.info("deleting sha file: " + filename+ ".sha256")
                os.remove(filename + ".sha256")
    else:
        log.error("file failed checksum: " + filename)


def process_dir(path):
    for file in os.listdir(path):
        if os.path.isdir(path+'/'+file):
            if is_recursive:
                process_dir(path+'/'+file)
        else:
            for file_type in file_pattern:
                if file.endswith(file_type):
                    process_file(path+'/'+file)
                    break


if __name__ == '__main__':
    configs = configparser.ConfigParser()

    # read config file
    args = sys.argv[1:]
    if args:
        configs.read(args[0])
    else:
        configs.read("/etc/monitor/monitor.ini")

    # load configs from file
    input_dir = configs.get("Directories", "input_dir")
    destination_dir = configs.get("Directories", "desitnation_dir")

    is_recursive = eval(configs.get("Options", "is_recursive"))
    has_sha25_file = eval(configs.get("Options", "has_sha256_file"))
    file_pattern = json.loads(configs.get("Options", "file_pattern"))
    do_delete = eval(configs.get("Options","delete_files"))

    log_file = configs.get("Logging", "log_file")

    # initialize logger
    log.basicConfig(filename=log_file,
                    level=log.INFO,
                    format='%(asctime)s %(message)s')

    log.info("file monitor starting up....")
    log.info("input dir:  "+input_dir)
    log.info("output dir: "+destination_dir)

    process_dir(input_dir)






