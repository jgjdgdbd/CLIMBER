#coding:utf-8
import random
import numpy as np
import idealmm_climber as mm
import AD as AD
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
        self.stat = 0 ##
        self.randomenable = randomenable
        self.reverseenable = 0
        self.stallenable = stallenable
        if self.stallenable > 0:
            self.L_PAD = AD.L_PAD(attacktype)
            self.F_PAD = AD.F_PAD(attacktype)
        self.start = 0
        no = 0
        self.m1 = mm.memorymodel(self.maxpagenums, self.attacktype,no, self.areashift, climberenable, randomenable, randomshift,self.reverseenable,stallenable,climberthreshold,climbershift)
        self.life2sorted = [0 for i in range(self.maxpagenums)]####climber
        self.logpath = "type"+str(self.attacktype)+"_defense_idealmm_threshold.dat"
        #self.life2sorted = self.m1.getlife2sorted()
        self.logfile = open(self.logpath, "w")
    def __del__(self):
        self.logfile.close()
    def attdetector(self, addr_temp, sortedlist):
        isswap = 1
        return isswap
    def access(self, addr_temp):
        if self.stallenable > 0:
            self.L_PAD.access(addr_temp>>6)
            self.F_PAD.access(addr_temp>>6)
        memorystat1 = self.m1.access(addr_temp>>12)
        isswap = 1
        if memorystat1[0] == 1:
            self.start = self.start + 1
            memorystat2 = self.m1.doswap(addr_temp>>12, isswap, memorystat1[1])
            if memorystat2[0] == -1:
                return (memorystat2[0], memorystat1[1])
            return (memorystat1[0], memorystat1[1])
        return (memorystat1[0],memorystat1[1])
