#! /bin/bash
pid=$(ps aux | grep file_monitor.py | awk'{print $2}')
kill -9 $pid
