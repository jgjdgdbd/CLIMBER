#coding:utf-8
import random
import numpy as np
import AD as AD
import twlmm_climber as mm
enable = 0
normalp = 0
attackp = 0
gapp = [normalp, attackp]
###############stall par begin
stalllimits = 5
stallenable = 0
par1threshold = 0
par2threshold = 0
#################### end
#######################random begin
randomshift = 17
randomenable = 0
######################random end
class DefenseLayer:
    def __init__(self, areasize, attacktype,climberenable, randomenable, stallenable,climbershift):
        self.areashift = 10#
        self.maxpagenums = areasize
        self.attacktype = attacktype
        self.climberenable = climberenable
        self.stallnums = 0
        self.attacknums = 0
        self.stat = 0 ##
        self.start = 0
        no = 0
        self.m1 = mm.memorymodel(self.maxpagenums, self.attacktype,no, self.areashift, randomenable, climbershift)
        #self.life2sorted = self.m1.getlife2sorted()
        self.life2sorted = [0 for i in range(self.maxpagenums)]####climber
        self.logpath = "type"+str(self.attacktype)+"_defense_idealmm.dat"
        #self.life2sorted = self.m1.getlife2sorted()
        self.logfile = open(self.logpath, "w")
    def __del__(self):
        self.logfile.close()
    def access(self, addr_temp):
        return self.m1.access(addr_temp)
