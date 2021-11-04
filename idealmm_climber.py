#coding:utf-8
import random
import numpy as np
import math
##############################
##############################
mu = 0.3 
sigma = mu*0.11 #
remapthreshold = 2000000###prediction phase
cyclethreshold = 20000000
#climbethreshold = 10

##################################

##################################
class memorymodel:
    def __init__(self, areasize, attacktype, no, areashift, climberenable, randomenable, randomshift,reverseenable,stallenable,climberthreshold,climbershift):
        self.maxpagenums = areasize
        self.climbershift = climbershift
        self.climberenable = climberenable
        areanums = self.maxpagenums >> 10
        self.attacktype = attacktype
        print('maxpagenums:' + str(self.maxpagenums))
        self.no = no
        self.randomkey = 0
        self.randomshift = randomshift
        self.randomenable = randomenable
        self.reverseenable = reverseenable
        self.climberthreshold = climberthreshold
        self.stallenable = stallenable
        self.life2sorted = [0 for x in range(self.maxpagenums)]
        self.randompath = ['', 'random_']
        self.climberpath = ['', 'climber_', 'oclimber_']
        self.stallpath = ['', 'stall_']
        self.endlifepath = 'type' + str(self.attacktype)+'_idealmm_'+str(climbershift)+'_'+self.climberpath[self.climberenable]+self.randompath[self.randomenable] + \
                            self.stallpath[self.stallenable]+str(self.climberthreshold)+"_"+'endlife.dat'
        self.endlogpath = 'type' + str(self.attacktype)+'_idealmm_'+str(climbershift)+'_'+self.climberpath[self.climberenable]+self.randompath[self.randomenable] + \
                            self.stallpath[self.stallenable]+str(self.climberthreshold)+'_'+'wearrate.log'
        np.random.seed(0)
        print("gen life distribution begin")
        p = np.random.normal(loc = mu, scale = sigma, size = 2*areanums)
        p.sort()

        x = [0 for i in range(self.maxpagenums)]
        for i in range(self.maxpagenums):
            x[i] = math.pow(p[areanums+(i>>10) - 1],-12)*90.345
        print("gen life distribution end")
        self.minlifetime = 10000000000
        self.maxlifetime = 0.0
        self.lifelist = [[0,0] for y in range(len(x))]
        self.lifelist2 = [[0,0] for y in range(len(x))]
        for i in range(len(x)) :
            if(self.minlifetime > x[i]):
                self.minlifetime = x[i]
            if(self.maxlifetime < x[i]):
                self.maxlifetime = x[i]
            self.lifelist[i][0] = i
            self.lifelist[i][1] = x[i]#
            self.lifelist2[i][0] = i
            self.lifelist2[i][1] = x[i]#
            self.life2sorted[i] = i
        x = []
        print("minlifetime =%d,maxlifetime =%d"%(int(self.minlifetime),int(self.maxlifetime)))
        self.maplist = [0 for x in range(self.maxpagenums)]
        self.reverselist = [0 for x in range(self.maxpagenums)]####climber
        self.sortednow = [0 for  y in range(self.maxpagenums)]
        self.climbla2hot = [0 for  y in range(self.maxpagenums)]###climber
        self.climberlocthre= [0 for  y in range(self.maxpagenums)]
        self.climberstart = [1 for  y in range(self.maxpagenums)]
        self.maxSL = 0
        self.start = 0 #climber start flag
        print("sort pages begin")
        self.sortedlist = sorted(self.lifelist2, key = lambda x:x[1])##
        for i in range(len(self.sortedlist)):
            self.life2sorted[self.sortedlist[i][0]] = i
            self.sortednow[i] = self.sortedlist[i][0]
            self.climbla2hot[self.sortedlist[i][0]] = i
            self.climberlocthre[i] = int(self.climberthreshold*(self.lifelist2[i][1]/self.minlifetime))
            #self.climberlocthre[i] = climbethreshold
        print("sort pages end")
        print("map begin")
        for i in range(len(self.sortedlist)):
            self.maplist[i] = i
            self.reverselist[i] = i####climber
        print("map end")
        self.visitcount = [[0 for x in range(2)] for y in range(self.maxpagenums)]##
        for i in range(len(self.visitcount)):
            self.visitcount[i][0] = i
        self.totalcount = 0
        self.remaptimes = 0
        self.totaltime = 0##
        self.climberpoint = (self.maxpagenums - 1) >> self.climbershift
        self.climbtime = 0
        self.disclimbtime =0
        self.rank2addrp = 0
        self.rank2addr = [0 for  y in range(self.maxpagenums)]
        self.visitedback = [0 for  y in range(self.maxpagenums)]
        self.map2weakaddr = self.maxpagenums - 1
    def getlife2sorted(self):
        return self.life2sorted
    def getrank2addr(self):
        return self.rank2addr
    def climber(self,addr_temp,counterv):
        #if counterv % climbethreshold == 0 and self.start == 1:
        addr= self.maplist[addr_temp]
        localclimbethreshold = self.climberlocthre[addr]
        maxup = 0
        if (counterv % (localclimbethreshold) == 0) and (self.climberenable >= 1):
            #step = int(counterv / localclimbethreshold)
            randommax = 1<<self.climbershift
            climberareaindex = self.climbla2hot[addr_temp] >> self.climbershift
            targetindex = climberareaindex
            if self.climberpoint == (self.maxpagenums - 1) >> self.climbershift:
                maxup = self.maxpagenums
            else:
                maxup = (self.climberpoint + 1) <<  self.climbershift
            if climberareaindex == self.climberpoint: #
                hotrandomaddr = random.randint(1, (1<<self.climbershift) - 1)
                targetaddr = self.sortednow[(self.climbla2hot[addr_temp] + hotrandomaddr) % (1<<self.climbershift) + (maxup - (1<<self.climbershift))]
            else:
                if climberareaindex > self.climberpoint:
                    targetindex = self.climberpoint
                else:
                    targetindex = random.randint(climberareaindex + 1, self.climberpoint)
                if targetindex == self.climberpoint:
                    randommax = maxup - (targetindex << self.climbershift)

                ###new end
                randomaddr = random.randint(0,(randommax)-1)
                #print(((targetindex<< climbershift)+randomaddr))
                targetaddr = self.sortednow[(targetindex<< self.climbershift) + randomaddr]
            tarla = self.reverselist[targetaddr]
            targetcount = self.visitcount[tarla][1]
            #if targetcount < counterv:
            wearratecompare = self.lifelist[targetaddr][1] / self.lifelist2[targetaddr][1] - self.lifelist[addr][1] / self.lifelist2[addr][1]
            countercompare = targetcount - counterv
            #if (self.lifelist[targetaddr][1] / self.lifelist2[targetaddr][1]) > (self.lifelist[addr][1] / self.lifelist2[addr][1]):
            if (wearratecompare > 0 and countercompare <= 0) or(wearratecompare <= 0 and countercompare > 0):
                #self.lifelist[targetaddr][1] = self.lifelist[targetaddr][1] - 1
                #if self.lifelist[targetaddr][1] < 0:
                self.lifelist[addr][1] = self.lifelist[addr][1] - 1
                if self.lifelist[addr][1] < 0:
                    return -1
                ###climber sl
                if self.climberstart[addr] == 0 and self.maxSL < (self.climbla2hot[tarla] >> self.climbershift):
                    self.maxSL = (self.climbla2hot[tarla] >> self.climbershift)
                #####
                self.reverselist[targetaddr] = addr_temp
                self.reverselist[addr] = tarla
                self.maplist[addr_temp] = targetaddr
                self.maplist[tarla] = addr
                swaptemp = self.climbla2hot[addr_temp]
                self.climbla2hot[addr_temp] = self.climbla2hot[tarla]
                self.climbla2hot[tarla] = swaptemp
                self.climbtime = self.climbtime + 1
                return 1
            self.disclimbtime = self.disclimbtime + 1
        return 0
    def clear(self):
        for i in range(len(self.visitcount)):
            self.visitedback[self.visitcount[i][0]] = self.visitcount[i][1]
            self.visitcount[i][1] = 0
    def access(self,addr_temp2):

        addr_temp =addr_temp2
        self.totaltime = self.totaltime + 1
        addr = self.maplist[addr_temp]
        #if self.totalcount < remapthreshold:
        self.visitcount[addr_temp][1] = self.visitcount[addr_temp][1] + 1
        #if self.visitcount[addr_temp][1] % climbethreshold == 0:
        if self.climber(addr_temp,self.visitcount[addr_temp][1]) == -1:
            return (-1, self.visitcount, self.maplist)
        self.totalcount = self.totalcount + 1
        self.lifelist[addr][1] = self.lifelist[addr][1] - 1
        if self.lifelist[addr][1] < 0:
            return (-1, self.visitcount, self.maplist)
        if self.totalcount == cyclethreshold:
            self.totalcount = 0
        if self.totalcount == remapthreshold:
            self.start = 1
            #print("remap begin")
            #self.totalcount = 0
            visitsortedlist = sorted(self.visitcount, key = lambda x:x[1])
            return (1, visitsortedlist, self.maplist)
            #print("remap end")
        elif self.totalcount % remapthreshold == 0:
            return (2, self.visitcount, self.maplist)
        else:
            return (0, self.visitcount, self.maplist)
    def doswap(self, addr_temp2, isswap, visitsortedlist):
        addr_temp = addr_temp2
        self.rank2addrp = 0
        self.maxSL = 0
        self.climberpoint = self.climberpoint - 1
        #if self.climberpoint <= (int(((self.maxpagenums / 4) * 3))>>climbershift):
        if self.climberpoint < (int(((self.maxpagenums / 2) ))>>self.climbershift):
            self.climberpoint = (self.maxpagenums - 1) >> self.climbershift
        if isswap != 0 and self.climberenable < 2:
            if self.randomenable == 1:
                self.randomkey = random.randint(0,(1<<self.randomshift)-1)
            addr = self.maplist[addr_temp]
            lifenowlist = sorted(self.lifelist, key = lambda x:x[1])
            for i in range(len(lifenowlist)):
                self.sortednow[i] = lifenowlist[i][0]
            maxwearrate = 0.0
            wearrate = 0.0
            maxlife = 0
            maxlife2 = 0
            maxi = 0
            for i in range(len(self.lifelist)):
                wearrate = 1.0- (self.lifelist[i][1]/self.lifelist2[i][1])
                if maxwearrate < wearrate:
                    maxwearrate = wearrate
                    maxlife = self.lifelist[i][1]
                    maxlife2 = self.lifelist2[i][1]
                    maxi = i
            print('maxwearrate='+str(maxwearrate))
            zeropoint = 0
            for i in range(len(visitsortedlist)):
                if visitsortedlist[len(visitsortedlist) - 1 - i][1] == 0 and zeropoint < len(visitsortedlist) - 1 - i:
                    zeropoint = len(visitsortedlist) - 1 - i
                #block1 start
                if isswap == 1:
                    #index = i
                    index = len(visitsortedlist) - 1 - i
                    #if self.randomenable == 1 and index < (1<<self.randomshift):
                    #    index = index ^ self.randomkey
                else:
                    #index = len(visitsortedlist) - 1 - i
                    index = i
                if len(visitsortedlist) - 1 - i > zeropoint:
                    vindex = len(visitsortedlist) - 1 - i
                else:
                    vindex = zeropoint - (len(visitsortedlist) - 1 - i)
                if len(visitsortedlist) - 1 - i == 0:
                    self.map2wearaddr = visitsortedlist[vindex][0]
                self.rank2addr[visitsortedlist[vindex][0]] = len(visitsortedlist) - 1 - i
                if self.randomenable == 1 and index < (((int(self.maxpagenums/2))>>self.randomshift)<<self.randomshift):
                    index = index ^ self.randomkey
                if index < (1<<self.randomshift):
                    self.climberstart[lifenowlist[index][0]] = 0
                else:
                    self.climberstart[lifenowlist[index][0]] = 1
                if self.maplist[visitsortedlist[vindex][0]] != lifenowlist[index][0] and self.maplist[visitsortedlist[vindex][0]] != addr:
                    self.lifelist[self.maplist[visitsortedlist[vindex][0]]][1] = self.lifelist[self.maplist[visitsortedlist[vindex][0]]][1] - 1
                    if self.lifelist[self.maplist[visitsortedlist[vindex][0]]][1] < 0:
                        return (-1, visitsortedlist, self.maplist)
                ###block1 end
                self.visitedback[visitsortedlist[vindex][0]] = self.visitcount[visitsortedlist[vindex][0]][1]
                self.visitcount[visitsortedlist[vindex][0]][1] = 0
                self.maplist[visitsortedlist[vindex][0]] = lifenowlist[index][0]
                self.reverselist[lifenowlist[index][0]] = visitsortedlist[vindex][0]
                self.climbla2hot[visitsortedlist[vindex][0]] = index
                self.life2sorted[visitsortedlist[vindex][0]] = vindex
            self.remaptimes = self.remaptimes + 1
            return (1, visitsortedlist, self.maplist)
        self.clear()
        return (0, visitsortedlist, self.maplist)
    def printstat(self):
        print("write endstat start")      #
        print('climbtime:%d'%(self.climbtime))
        print('disclimbtime:%d'%(self.disclimbtime))
        with open(self.endlifepath,'w') as f2:
            for i in range(len(self.lifelist)):
                f2.write(U"%d,%d,%d\n"%(self.lifelist[i][0],int(self.lifelist[i][1]),int(self.lifelist2[i][1])))
        with open(self.endlogpath,'w') as f2:
            #for i in range(len(self.lifelist)):
            f2.write(U"overhead:%d,%d,%d\n"%(self.climbtime,int(0),int(self.disclimbtime)))
        print("write endstat end")
        print("totaltime:")
        print(self.totaltime)        
        print("print end");
