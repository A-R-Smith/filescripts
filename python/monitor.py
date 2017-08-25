#!/usr/bin/env python
import time
import sys
import os
import ntpath
import logging as log
import hashlib
from shutil import copyfile
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# filename="/home/ford/WeeklyReports/UBIWeeklyReports_2017-07-05.txt"
# fname="/home/nwadmin/test/DailyReports/dailyReport.txt"

testFileShare = "/mnt/fileshare/test/"
prodFileShare = "/mnt/fileshare/prod/"
log_file = "/var/log/monitor/monitor.log"
testLanding = "/home/ford/"
prodLanding = "/home/fordprod/"

weeklyReports = "WeeklyReports/"
weeklyMetrics = "WeeklyMetrics/"
dailyReports = "DailyReports/"

log.basicConfig(filename=log_file,
                level=log.INFO,
                format='%(asctime)s %(message)s')


# strips the file name from the end of the full file path
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


# calculates the sha256 checksum from the file and compares to the sha256 file provided by ford
def verifyWithSHA256(fname):
    try:
        cfile = open(fname, 'rb')
        checksum = hash_bytestr_iter(file_as_blockiter(cfile), hashlib.sha256())
    except Exception:
        log.error("failed to create checksum from file: " + fname)
        return False
    else:
        cfile.close()

    try:
        sfile = open(fname + ".sha256", 'r')
        sha256 = sfile.read().rstrip('\r\n')
    except Exception:
        log.error("failed to read ford's .sha256 file: " + fname + ".sha256")
        return False
    else:
        sfile.close()

    return checksum == sha256


# creates sha256 checksum
def hash_bytestr_iter(bytesiter, hasher, ashexstr=True):
    for block in bytesiter:
        hasher.update(block)
    return (hasher.hexdigest() if ashexstr else hasher.digest())


# creates an iterator of file blocks
def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.txt"]

    def __init__(self, toPath):
        self.toPath = toPath
        super(MyHandler, self).__init__()

    def process(self, event):
        time.sleep(5)

        # print event.src_path, event.event_type, event.is_directory  # print now only for degu
        if event.event_type == 'created' and event.is_directory == False:

            verified = verifyWithSHA256(event.src_path)
            if (verified):
                filename = path_leaf(event.src_path)
                log.info("moving file: " + event.src_path)
                try:
                    copyfile(event.src_path, self.toPath + filename)
                except Exception:
                    log.error("failed to copy file to file share: " + filename)
                else:
                    os.remove(event.src_path)
                    os.remove(event.src_path + ".sha256")
            else:
                log.error("file failed checksum: " + event.src_path)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


if __name__ == '__main__':
    log.info("file monitor starting up....")
    observer = Observer()
    observer.schedule(MyHandler(testFileShare + weeklyReports), path=testLanding + weeklyReports)
    observer.schedule(MyHandler(testFileShare + weeklyMetrics), path=testLanding + weeklyMetrics)
    observer.schedule(MyHandler(testFileShare + dailyReports), path=testLanding + dailyReports)
    observer.schedule(MyHandler(prodFileShare + weeklyReports), path=prodLanding + weeklyReports)
    observer.schedule(MyHandler(prodFileShare + weeklyMetrics), path=prodLanding + weeklyMetrics)
    observer.schedule(MyHandler(prodFileShare + dailyReports), path=prodLanding + dailyReports)
    observer.start()
    #    print args
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
