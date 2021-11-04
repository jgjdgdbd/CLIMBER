#coding:utf-8
import random
import numpy as np
import defenselayer_ideal_climber as dl
import sys
tracepath = 'whb_trace.dat'
endstatpath = 'endstat.dat'
logpath = 'log.dat'
endlifepath = 'endlife.dat'
initlifepath = 'initlife.dat'
areashift = 0 
maxpagenums = (4194304>>2) >> areashift 
isbreak = 0#
attacktype = 0
attackpp = 1
endnums = 1000001000
#climbershift = 17
##########################################################
class AcListGenerator:
    def __init__(self, type1, areasize, attackpp,climberenable, randomenable,climbershift,climberthreshold, stallenable):
        self.type = type1
        self.areasize = maxpagenums
        self.flag = 0
        self.index = 0
        self.round = 0
        self.count = 0
        self.hot = 100000
        pageshift = 12
        self.filelength = 0
        self.tracepoint = 0
        self.visitcountnow = 0
        with open(tracepath) as tracefile:
            for line in tracefile:
                temp = int(line)
                self.filelength = self.filelength + 1
        self.d1 = dl.DefenseLayer(self.areasize, self.type, climberenable, randomenable, stallenable,climberthreshold,climbershift)
        self.visitlist = [0 for i in range(self.filelength)]
        self.filelength = 0
        with open(tracepath) as tracefile:
            for line in tracefile:
                temp = int(line)
                self.visitlist[self.filelength] = temp
                self.filelength = self.filelength + 1
    def getindex(self):
        if self.tracepoint >= self.filelength:
            #return -1
            self.tracepoint = 0
        self.visitcountnow = self.visitcountnow + 1
        if self.visitcountnow == endnums:
            return -1
        ans = self.visitlist[self.tracepoint] % (self.areasize<<12)
        self.tracepoint = self.tracepoint + 1
        return ans

if len(sys.argv) == 1:
    g1 = AcListGenerator(attacktype,maxpagenums,attackpp,0,0,10,10,0)
elif len(sys.argv) == 2:
    g1 = AcListGenerator(attacktype,maxpagenums,attackpp,int(sys.argv[1]),0,10,10,0)
elif len(sys.argv) == 3:
    g1 = AcListGenerator(attacktype,maxpagenums,attackpp,int(sys.argv[1]),int(sys.argv[2]),10,10,0)
elif len(sys.argv) == 4:
    g1 = AcListGenerator(attacktype,maxpagenums,attackpp,int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),10,0)
elif len(sys.argv) == 5:
    g1 = AcListGenerator(attacktype,maxpagenums,attackpp,int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),0)
elif len(sys.argv) == 6:
    g1 = AcListGenerator(attacktype,maxpagenums,attackpp,int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]))
while isbreak == 0:
    addr = g1.getindex()
    print(addr)
    if addr == -1:
        g1.d1.m1.printstat()
        isbreak = 1
        break
    memorystat = g1.d1.access(addr)
    if memorystat[0] == -1:
        m1.printstat()
        isbreak = 1
print("end");
