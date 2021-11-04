import random
import numpy as np
class L_PAD:
    def __init__(self,type1):
        self.lrup = 0
        self.hitcounter = 0
        self.writecounter = 0
        self.countnums = 16
        self.hitcountermax = 10
        self.writecountermax = 20
        self.insertp = 1.0/256.0
        self.logname = "type"+str(type1)+"_L_PAD.log"
        self.logfile = open(self.logname,"w")
        self.count = [0 for i in range(self.countnums)]
        self.index = [0 for i in range(self.countnums)]
        self.enable = [0 for i in range(self.countnums)]
        for i in range(self.countnums):
            self.enable[i] = 0
            self.index[i] = 0
            self.count[i] = 0
        #srand((int)(time(NULL)));
    def __del__(self):
        self.logfile.close()
    def getrandom(self):
        return random.random()
        #lru
    def getevictp(self):
        maxp = 0
        for i in range(self.countnums):
            if self.count[i] > self.count[maxp]:
                maxp = i
        return maxp
    def access(self, addr_temp):
        self.writecounter = self.writecounter + 1
        if self.writecounter == (1<<self.writecountermax):
            self.logfile.write("L_PAD hitrate1 = %.10f\n"%(float(self.hitcounter) / float(self.writecounter)))
            self.writecounter = self.writecounter / 2
            self.hitcounter = self.hitcounter / 2
        for i in range(self.countnums):
            if((self.index[i] == addr_temp) and (self.enable[i] == 1)):
                #lru counter
                self.count[i] = 0
                for j in range(self.countnums):
                    if(i!=j):
                        self.count[j] = self.count[j] + 1
                self.hitcounter = self.hitcounter + 1
                if(self.hitcounter == 1<<self.hitcountermax):
                    self.logfile.write("L_PAD hitrate2 = %.10f\n"%(float(self.hitcounter) / float(self.writecounter)))
                    self.writecounter = self.writecounter / 2
                    self.hitcounter = self.hitcounter / 2
                return 1
        if(self.getrandom() < self.insertp):
            self.lrup = self.getevictp()
            self.index[self.lrup] = addr_temp
            self.count[self.lrup] = 0
            self.enable[self.lrup] = 1
            for j in range(self.countnums):
                if(self.lrup!=j):
                    self.count[j] = self.count[j] + 1
        return 0
class F_PAD:
    def __init__(self,type1):
        self.lrup = 0
        self.hitcounter = 0
        self.writecounter = 0
        self.countnums = 16
        self.hitcountermax = 10
        self.writecountermax = 20
        self.countmax = 32
        self.insertp = 1.0/256.0
        self.count = [0 for i in range(self.countnums)]
        self.index = [0 for i in range(self.countnums)]
        self.enable = [0 for i in range(self.countnums)]
        self.logname = "type"+str(type1)+"_F_PAD.log"
        self.logfile = open(self.logname,"w")
        for i in range(self.countnums):
            self.enable[i] = 0
            self.index[i] = 0
            self.count[i] = 0
    def __del__(self):
        self.logfile.close()
    def getrandom(self):
        return random.random()
    #lru
    def getevictp(self):
        minp = self.lrup
        for i in range(self.countnums):
            lruindex = (self.lrup+i) % self.countnums
            if(self.count[lruindex] == 0):
                return lruindex
            if(self.count[lruindex] < self.count[minp]):
                minp = lruindex
        for i in range(self.countnums):
            if(i!=minp):
                self.count[i] = self.count[i] - self.count[minp]
        self.count[minp] = 0
        self.lrup = (minp + 1) % self.countnums
        return minp
    def access(self, addr_temp):
        self.writecounter = self.writecounter + 1
        if(self.writecounter == 1<<self.writecountermax):
            self.logfile.write("F_PAD hitrate1 = %.10f hitcounter = %d writecounter = %d\n"%(float(self.hitcounter) / float(self.writecounter),self.hitcounter,self.writecounter))
            self.writecounter = self.writecounter / 2
            self.hitcounter = self.hitcounter / 2
        for i in range(self.countnums):
            if((self.index[i] == addr_temp) and (self.enable[i] == 1)):
                if self.count[i]+1 != (1 << self.countmax):
                    self.count[i] = self.count[i] + 1
                #///////////////
                self.hitcounter = self.hitcounter + 1
                if(self.hitcounter == 1<<self.hitcountermax):
                    self.logfile.write("F_PAD hitrate2 = %.10f hitcounter = %d writecounter = %d\n"%(float(self.hitcounter) / float(self.writecounter),self.hitcounter,self.writecounter))
                    self.writecounter = self.writecounter / 2
                    self.hitcounter = self.hitcounter / 2
                return 1
        randomv = self.getrandom()
        #print(randomv)
        if(randomv < self.insertp):
            evindex = 0
            evindex = self.getevictp()
            self.index[evindex] = addr_temp
            #//self.count[evindex] = 0
            self.enable[evindex] = 1
        return 0
