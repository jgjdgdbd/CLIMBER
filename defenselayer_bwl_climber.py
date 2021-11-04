#coding:utf-8
import random
import numpy as np
import bwlmm_climber as mm
enable = 1
normalp = 0
attackp = 0
gapp = [normalp, attackp]
###############stall par begin
stalllimits = 5
#stallenable = 0
par1threshold = 0
par2threshold = 0
#################### end
#######################random begin
randomshift = 17
#randomenable = 0
######################random end
class DefenseLayer:
    def __init__(self, areasize, attacktype,climberenable, randomenable, stallenable,climberthreshold,climbershift):
        self.areashift = 10##
        self.maxpagenums = areasize
        self.attacktype = attacktype
        self.stallnums = 0
        self.attacknums = 0
        self.stat = 0 #
        self.start = 0
        self.randomenable = randomenable
        self.reverseenable = 0
        self.stallenable = stallenable
        no = 0
        self.m1 = mm.memorymodel(self.maxpagenums, self.attacktype,no, self.areashift, climberenable, randomenable, randomshift,self.reverseenable,stallenable,climberthreshold,climbershift)
        #self.life2sorted = self.m1.getlife2sorted()
        self.life2sorted = [0 for i in range(self.maxpagenums)]####climber
        self.logpath = "type"+str(self.attacktype)+"_defense_bwlmm_threshold.dat"
        #self.life2sorted = self.m1.getlife2sorted()
        self.logfile = open(self.logpath, "w")
    def __del__(self):
        self.logfile.close()
    def hotdistribute(self, sortedcountlist):
        areasize = 1000
        total = 0.0
        #for i in range(len(sortedcountlist)):
        for i in range(areasize):
            total = total + sortedcountlist[len(sortedcountlist) - 1 - i][1]
        #average = float(total) / float(areasize)
        maxcount = sortedcountlist[len(sortedcountlist) - 1][1]
        level = float(float(maxcount) / float(total))
        self.logfile.write(U"level:%f\n"%level)
        return level
    def hotmonitor(self, sortedcountlist):
        dismatch = 0
        #areasize = min(self.maxpagenums/2,1<<randomshift)
        areasize = min(self.maxpagenums/2,1024)
        #areasize = self.maxpagenums
        address2life = self.m1.getrank2addr()
        addrsource = 0
        maxdismatch = 0
        minvalue = 100000000000
        maxindex = 0###
        dis = 0
        index = 0
        if self.start > 2:
            for i in range(self.maxpagenums):
                if self.life2sorted[i] < areasize:
                    if self.life2sorted[i] < address2life[i]:
                        dis = address2life[i] - self.life2sorted[i]
                    else:
                        #dis = self.life2sorted[i] - address2life[i]
                        dis = 0
                    dismatch = dismatch + dis
                    if maxdismatch < dis:
                        maxdismatch = dis
                self.life2sorted[i] = address2life[i]
            self.logfile.write(U"dismatch:%d\n"%dismatch)
            self.logfile.write(U"max:%d\n"%maxdismatch)
            print(U"max:%d\n"%maxdismatch)
        else:
            for i in range(self.maxpagenums):
                self.life2sorted[i] = address2life[i]
        return (dismatch, maxdismatch)
    def attdetector(self, addr_temp, sortedlist):
        isswap = 1
        par1 = self.hotdistribute(sortedlist)
        par2 = self.hotmonitor(sortedlist)
        if self.stallenable == 1:
            if par1 >= par1threshold or par2[1] >= par2threshold:
                self.stallnums = self.stallnums + 1
                if self.stallnums >= stalllimits:
                    return -1 
        return isswap
    def access(self, addr_temp):
        memorystat1 = self.m1.access(addr_temp)
        if memorystat1[0] == 1:
            if enable == 0:
                isswap = self.attdetector(addr_temp,memorystat1[1])
                self.start = self.start + 1
                memorystat2 = self.m1.doswap(addr_temp, 1)
                if memorystat2[0] == -1:
                    return (memorystat2[0], memorystat1[1])
            #return (isswap, memorystat1[1])
                return (memorystat1[0],memorystat1[1])
            isswap = self.attdetector(addr_temp,memorystat1[2])
            if isswap == -1:
                return (-1, memorystat1[1])
            self.start = self.start + 1
            memorystat2 = self.m1.doswap(addr_temp, isswap)
            if memorystat2[0] == -1:
                return (memorystat2[0], memorystat1[1])
            #return (isswap, memorystat1[1])
            return (memorystat1[0], memorystat1[1])
        return (memorystat1[0],memorystat1[1])
