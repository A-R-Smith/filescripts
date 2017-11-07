#!/usr/bin/env python
from os import listdir
from os.path import isfile, join, isdir

prod_dir = '/mnt/fileshare/prod/'
backup_dir = '/mnt/backup/'

dirs = [f for f in listdir(prod_dir) if isdir(join(prod_dir, f))]

for dir in dirs:
    onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
    for file in onlyfiles:
        print(dir+file)