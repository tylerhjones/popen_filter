#!/usr/local/bin/python2.6

import sys

from commands import getoutput
from time     import sleep
from re       import compile

user  = "root"

tobig_single = 30720  # 30MB
tobig_total  = 102400 # 100MB

memory = {
    "total": 0,
    "largest": 0,
}

check = "ps -u %s -o rss,etime,pid,command" % (user)

regex = compile("^\s*(?P<memory>\d+)\s+(?P<time>[\d:-]+)\s+(?P<pid>\d+)\s+(?P<process>.*)")
for line in getoutput(check).split("\n"):
    m = regex.search(line)
    if m:
        mem = int(m.group("memory"))
        memory["total"] += mem
        if mem > memory["largest"]:
            memory["largest"] = mem
        if "-d" in sys.argv:
            print " %5.2fM %s" % (float(mem)/1024, m.group("process")[:100])

if memory["largest"] > tobig_single:
    print "A single process exceeds %sM (%5.2fM)" % (tobig_single / 1024, float(memory["largest"]) / 1024)

if memory["total"] > tobig_total:
    print "Collectively, all processes exceed %sM (%5.2fM)" % (tobig_total / 1024, float(memory["total"]) / 1024)