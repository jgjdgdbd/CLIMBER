#coding:utf-8
import random
import numpy as np
import math
##############################
##############################

mu = 0.3
sigma = mu*0.11 #
remapthreshold = 2000000
cyclethreshold = 20000000

lineshift = 6
groupshift = 12
counternums = 256
hashnums = 2
hotthreshold = 1000
list1size = 64
list2size  = 64
list3size =128
hotlistsize =list1size + list2size + list3size


halfinterval = cyclethreshold

isbreak = 0
listsize = [list1size,list2size,list3size]
#climbethreshold = 10

class bloomfilter :
    def __init__(self, groupshift, areasize, hashnums, counternums,list1size, list2size, list3size,halfinterval):
        self.halfinterval = halfinterval
        self.groupshift = groupshift
        self.areasize = areasize
        self.hashnums = hashnums
        self.groupnums = int( areasize >> groupshift) + 1
        print(self.groupnums)
        self.counter = [[0 for m in range(256)] for y in range(self.groupnums)]
        self.counternums = counternums
        self.hotlist = [[[-1 for m in range(list1size)],[-1 for n in range(list2size)],[-1 for p in range(list3size)]] for k in range(self.groupnums)]
        self.voidlist = [[[1],[1],[1]]]
        self.list1point = [0 for x in range(self.groupnums)]
        self.list2point = [0 for x in range(self.groupnums)]
        self.list3point = [0 for x in range(self.groupnums)]
        self.addr2hot = [-1 for y in range(self.areasize)]
    def clear(self):
        for i in range(self.groupnums):
            self.list3point[i] = 0
            for j in range(counternums):
                self.counter[i][j] = 0
            for j in range(len(self.hotlist[i])):
                for k in range(len(self.hotlist[i][j])):
                    self.hotlist[i][j][k] = -1
        for i in range(len(self.addr2hot)):
            self.addr2hot[i] = -1
    def rank(self):
        return self.hotlist
    def getcount(self,addr_temp):
        hashvalue = [0 for x in range(hashnums)]
        groupindex = int(addr_temp >> groupshift)
        isclimb = cyclethreshold
        for i in range(hashnums):
            hashvalue[i] = (addr_temp%(1<<groupshift)+i) % counternums
            if isclimb > self.counter[groupindex][hashvalue[i]]:
                isclimb = self.counter[groupindex][hashvalue[i]]
        return isclimb
    def count(self,addr_temp):
        hashvalue = [0 for x in range(hashnums)]
        groupindex = int(addr_temp >> groupshift)
        isclimb = cyclethreshold
        for i in range(hashnums):
            hashvalue[i] = (addr_temp%(1<<groupshift)+i) % counternums
            self.counter[groupindex][hashvalue[i]] =  self.counter[groupindex][hashvalue[i]] + 1
            if isclimb > self.counter[groupindex][hashvalue[i]]:
                isclimb = self.counter[groupindex][hashvalue[i]]
        return isclimb
    def access(self,addr,hotthreshold,totaltime):
        hashvalue = [0 for x in range(hashnums)]
        groupindex = int(addr >> groupshift)
        ishot = 0
        isclimb = cyclethreshold
        inhot = 0
        addr_temp = addr
        if self.addr2hot[addr_temp] != -1:
            inhot = 1
            if self.addr2hot[addr_temp] < list3size:
                if self.hotlist[groupindex][1][0] != -1:#######
                    self.addr2hot[self.hotlist[groupindex][1][0]] = self.addr2hot[addr_temp]
                self.hotlist[groupindex][2][self.addr2hot[addr_temp]] = self.hotlist[groupindex][1][0]
                self.addr2hot[addr_temp] = list3size
                self.hotlist[groupindex][1][0] = addr_temp
            elif self.addr2hot[addr_temp] < list3size + list2size - 1:##
                if self.hotlist[groupindex][1][self.addr2hot[addr_temp] - list3size +1] != -1:
                    self.addr2hot[self.hotlist[groupindex][1][self.addr2hot[addr_temp] - list3size+1]] = self.addr2hot[addr_temp]
                self.hotlist[groupindex][1][self.addr2hot[addr_temp] - list3size] = self.hotlist[groupindex][1][self.addr2hot[addr_temp] - list3size+1]
                self.hotlist[groupindex][1][self.addr2hot[addr_temp] - list3size+1] = addr_temp
                self.addr2hot[addr_temp] = self.addr2hot[addr_temp] + 1
            elif self.addr2hot[addr_temp] == list3size + list2size - 1:
                if self.hotlist[groupindex][0][0] != -1:
                    self.addr2hot[self.hotlist[groupindex][0][0]] = self.addr2hot[addr_temp]
                self.hotlist[groupindex][1][self.addr2hot[addr_temp] - list3size] = self.hotlist[groupindex][0][0]
                self.hotlist[groupindex][0][0] = addr_temp
                self.addr2hot[addr_temp] = list3size + list2size
            elif self.addr2hot[addr_temp] < hotlistsize - 1:
                if self.hotlist[groupindex][0][self.addr2hot[addr_temp]-list3size-list2size +1] != -1:
                    self.addr2hot[self.hotlist[groupindex][0][self.addr2hot[addr_temp]-list3size-list2size+1]] = self.addr2hot[addr_temp]
                self.hotlist[groupindex][0][self.addr2hot[addr_temp]-list3size-list2size] = self.hotlist[groupindex][0][self.addr2hot[addr_temp]-list3size-list2size+1]
                self.hotlist[groupindex][0][self.addr2hot[addr_temp]-list3size-list2size+1] = addr_temp
                self.addr2hot[addr_temp] = self.addr2hot[addr_temp] + 1
        for i in range(hashnums):
            hashvalue[i] = (addr%(1<<groupshift)+i) % counternums
            self.counter[groupindex][hashvalue[i]] =  self.counter[groupindex][hashvalue[i]] + 1
            if self.counter[groupindex][hashvalue[i]] >= hotthreshold:
                ishot = ishot + 1
            if isclimb > self.counter[groupindex][hashvalue[i]]:
                isclimb = self.counter[groupindex][hashvalue[i]]
        if ishot >= hashnums:
            if inhot == 0:
                if self.hotlist[groupindex][2][self.list3point[groupindex]] != -1:
                    self.addr2hot[self.hotlist[groupindex][2][self.list3point[groupindex]]] = -1
                self.hotlist[groupindex][2][self.list3point[groupindex]] = addr
                self.addr2hot[addr] = self.list3point[groupindex]
                self.list3point[groupindex] = (self.list3point[groupindex] + 1) % list3size
        return isclimb


class memorymodel:
    def __init__(self, areasize, attacktype, no, areashift, climberenable, randomenable,randomshift, reverseenable,stallenable,climberthreshold,climbershift):
        self.maxpagenums = areasize
        self.climbershift = climbershift
        self.climberenable = climberenable
        areanums = self.maxpagenums >> 10
        print('self.maxpagenums' + str(self.maxpagenums))
        self.attacktype = attacktype
        np.random.seed(0)
        print("gen life distribution begin")
        p = np.random.normal(loc = mu, scale = sigma, size = 2*areanums)
        p.sort()
        
        x = [0 for i in range(self.maxpagenums)]
        for i in range(self.maxpagenums):
            x[i] = math.pow(p[areanums+(i>>10) -1 ],-12)*90.345
        print("gen life distribution end")
        self.minlifetime = 10000000000
        self.maxlifetime = 0.0
        self.no = no 
        self.randomkey = 0  ###randmap
        self.randomenable = randomenable
        self.randomshift = randomshift
        self.reverseenable = reverseenable
        self.stallenable = stallenable
        self.climberthreshold = climberthreshold
        self.randompath = ['', 'random_']
        self.climberpath = ['', 'climber_','oclimber']
        self.stallpath = ['', 'stall_']
        self.endlifepath = 'type' + str(self.attacktype)+'_bwlmm_'+str(climbershift)+'_'+self.climberpath[self.climberenable]+self.randompath[self.randomenable] + \
                            self.stallpath[self.stallenable]+str(self.climberthreshold)+'_'+'endlife.dat'
        self.endlogpath = 'type' + str(self.attacktype)+'_bwlmm_'+str(climbershift)+'_'+self.climberpath[self.climberenable]+self.randompath[self.randomenable] + \
                            self.stallpath[self.stallenable]+str(self.climberthreshold)+'_'+'wearrate.log'
        self.lifelist = [[0,0] for y in range(len(x))]
        self.lifelist2 = [[0,0] for y in range(len(x))]
        self.sortednow = [0 for  y in range(len(x))]
        self.climbla2hot = [0 for  y in range(len(x))]####climber
        self.start = 0
        for i in range(len(x)) :
            if(self.minlifetime > x[i]):
                self.minlifetime = x[i]
            if(self.maxlifetime < x[i]):
                self.maxlifetime = x[i]
            self.lifelist[i][0] = i
            self.lifelist[i][1] = x[i]#
            self.lifelist2[i][0] = i
            self.lifelist2[i][1] = x[i]#
        x = []
        print("minlifetime =%d,maxlifetime =%d"%(int(self.minlifetime),int(self.maxlifetime)))
        self.maplist = [0 for x in range(self.maxpagenums)]
        self.reverselist = [0 for x in range(self.maxpagenums)]
        self.countlist = [[0,0] for x in range(self.maxpagenums)]#
        self.climberlocthre= [0 for  y in range(self.maxpagenums)]
        self.voidreturn = [[0,0]]
        print("sort pages begin")
        self.sortedlist = sorted(self.lifelist2, key = lambda x:x[1])##
        print("sort pages end")
        for i in range(len(self.sortedlist)):
            self.climbla2hot[self.sortedlist[i][0]] = i
            self.sortednow[i] = self.sortedlist[i][0]
            self.climberlocthre[i] = int(self.climberthreshold*(self.lifelist2[i][1]/self.minlifetime))
        print("map begin")
        for i in range(len(self.maplist)):
            self.maplist[i] = i
            self.reverselist[i] = i
            self.countlist[i][0] = i
        print("map end")
        self.visitcount = [[0 for x in range(2)] for y in range(self.maxpagenums)]##
        for i in range(len(self.visitcount)):
            self.visitcount[i][0] = i
        self.totalcount = 0
        self.remaptimes = 0
        self.totaltime = 0###
        print("bloomfilter begin")
        self.bloomfilter1 = bloomfilter(groupshift, self.maxpagenums, hashnums, counternums,list1size, list2size, list3size,halfinterval)
        print("bloomfilter1 end")
        self.bloomfilter2 = bloomfilter(groupshift, (self.maxpagenums >> groupshift), hashnums, counternums,list1size, list2size, list3size,halfinterval)
        print("bloomfilter2 end")
        self.climberpoint = (self.maxpagenums - 1) >> self.climbershift
        self.climbtime = 0
        self.disclimbtime =0
        self.rank2addrp = 0
        self.rank2addr = [0 for  y in range(self.maxpagenums)]
        self.climberstart = [1 for  y in range(self.maxpagenums)]
        self.maxSL = 0
        self.isvisited = [0 for  y in range(self.maxpagenums)]
        self.visitedback = [0 for  y in range(self.maxpagenums)]
        self.map2weakaddr = self.maxpagenums - 1 
    def getrank2addr(self):
        return self.rank2addr
    def climber(self,addr_temp,counterv):
        addr= self.maplist[addr_temp]
        localclimbethreshold = self.climberlocthre[addr]
        maxup = 0
        if (counterv % (localclimbethreshold) == 0) and (self.climberenable >= 1):
            randommax = 1<<self.climbershift
            climberareaindex = self.climbla2hot[addr_temp] >> self.climbershift
            targetindex = climberareaindex
            if self.climberpoint == (self.maxpagenums - 1) >> self.climbershift:
                maxup = self.maxpagenums
            else:
                maxup = (self.climberpoint + 1) <<  self.climbershift
            if climberareaindex == self.climberpoint: ##
                hotrandomaddr = random.randint(1, (1<<self.climbershift) - 1)
                targetaddr = self.sortednow[(self.climbla2hot[addr_temp] + hotrandomaddr) % (1<<self.climbershift) + (maxup - (1<<self.climbershift))]
            else:
                ####new begin
                if climberareaindex > self.climberpoint:
                    targetindex = self.climberpoint
                else:
                    targetindex = random.randint(climberareaindex + 1, self.climberpoint)
                if targetindex == self.climberpoint:
                    randommax = maxup - (targetindex << self.climbershift)
                ###new end
                randomaddr = random.randint(0,(randommax)-1)
                targetaddr = self.sortednow[(targetindex<< self.climbershift) + randomaddr]
            tarla = self.reverselist[targetaddr]
            targetcount = self.bloomfilter1.getcount(tarla)
            #if targetcount <= counterv:
            wearratecompare = self.lifelist[targetaddr][1] / self.lifelist2[targetaddr][1] - self.lifelist[addr][1] / self.lifelist2[addr][1]
            countercompare = targetcount - counterv
            if (wearratecompare > 0 and countercompare <= 0) or(wearratecompare < 0 and countercompare > 0):

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
    def access(self,addr_temp):
        self.isvisited[addr_temp] = self.isvisited[addr_temp] + 1
        self.totaltime = self.totaltime + 1
        addr = self.maplist[addr_temp]
        if self.totalcount < remapthreshold:
            self.visitcount[addr_temp][1] = self.visitcount[addr_temp][1] + 1
        self.totalcount = self.totalcount + 1
        isclimb = self.bloomfilter1.access(addr_temp, hotthreshold,self.totalcount)
        self.bloomfilter2.access((addr_temp >> groupshift), hotthreshold,self.totalcount)
        if self.climber(addr_temp,isclimb) == -1:
            return (-1,[self.bloomfilter1.voidlist,self.bloomfilter2.voidlist],self.voidreturn)
        self.lifelist[addr][1] = self.lifelist[addr][1] - 1
        if self.lifelist[addr][1] < 0:
            return (-1,[self.bloomfilter1.voidlist,self.bloomfilter2.voidlist],self.voidreturn)
        if self.totalcount == cyclethreshold:
            self.totalcount = 0
        if self.totalcount == remapthreshold:
            self.start = 1
            #self.totalcount = 0
            for i in range(len(self.maplist)):
                self.countlist[i][1] = self.bloomfilter1.getcount(i)
            return (1, [self.bloomfilter1.hotlist,self.bloomfilter2.hotlist], sorted(self.countlist, key = lambda x:x[1]))
        elif self.totalcount % remapthreshold == 0:
            return (2, [self.bloomfilter1.voidlist,self.bloomfilter2.voidlist], self.voidreturn)
        else:
            return (0, [self.bloomfilter1.voidlist,self.bloomfilter2.voidlist], self.voidreturn)
    def doswap(self, addr_temp, isswap):
        self.climberpoint = self.climberpoint - 1
        self.maxSL = 0
        self.rank2addrp = 0
        if self.climberpoint < (int(((self.maxpagenums / 2) ))>>self.climbershift):
            self.climberpoint = (self.maxpagenums - 1) >> self.climbershift
        if isswap != 0 and self.climberenable < 2:
            addr = self.maplist[addr_temp]
            if self.randomenable == 1:
                self.randomkey = random.randint(0,(1<<self.randomshift)-1)
            mapindex = 0#
            rank1 = self.bloomfilter1.rank()
            rank2 = self.bloomfilter2.rank()
            lifenowlist = sorted(self.lifelist, key = lambda x:x[1])
            for i in range(len(lifenowlist)):
                self.visitedback[i] = self.isvisited[i]
                self.isvisited[i] = 0
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
            print('maxwearrate:'+str(maxwearrate))
            for listindex1 in range (len(rank2[0])):
                for gpindex2 in range(len(rank2)):
                    for listindex2 in range (len(rank2[gpindex2])):
                        for index2 in range(len(rank2[gpindex2][listindex2])):
                            if rank2[gpindex2][listindex2][listsize[listindex2] - 1 - index2] != -1:
                                gpindex1 = rank2[gpindex2][listindex2][listsize[listindex2] - 1 - index2]
                            #for listindex1 in range (len(rank2[gpindex2])):
                                for index1 in range(len(rank1[gpindex1][listindex1])):
                                    if rank1[gpindex1][listindex1][listsize[listindex1] - 1 - index1] != -1:
                                        bemapaddr = rank1[gpindex1][listindex1][listsize[listindex1] - 1 - index1]
                                        if isswap == 1:
                                            index = len(lifenowlist) - 1 - mapindex
                                        else:
                                            index = mapindex
                                        if index < (1<<self.randomshift):
                                            self.climberstart[lifenowlist[index][0]] = 0
                                        else:
                                            self.climberstart[lifenowlist[index][0]] = 1
                                        self.rank2addr[bemapaddr] = len(lifenowlist) - 1 - mapindex
                                        #if self.randomenable == 1 and index < (1<<self.randomshift):
                                        if self.randomenable == 1 and index < (((int(self.maxpagenums/2))>>self.randomshift)<<self.randomshift):
                                        #if self.randomenable == 1 and index < (self.maxpagenums/2):
                                            index = index ^ self.randomkey
                                        if self.maplist[bemapaddr] != lifenowlist[(index)][0] or self.maplist[bemapaddr] == addr:
                                            #不要交换开销
                                            self.lifelist[self.maplist[bemapaddr]][1] = self.lifelist[self.maplist[bemapaddr]][1] - 1
                                            if self.lifelist[self.maplist[bemapaddr]][1] < 0:
                                                return (-1, [self.bloomfilter1.voidlist,self.bloomfilter2.voidlist], self.maplist)
                                        self.maplist[bemapaddr] = lifenowlist[(index)][0]
                                        self.reverselist[lifenowlist[(index)][0]] = bemapaddr
                                        self.climbla2hot[bemapaddr] = (index)
                                        #self.life2sorted[bemapaddr] = len(self.sortedlist) - 1 - mapindex
                                        mapindex = mapindex + 1 
            #print(mapindex)
            for noindex2  in range (len(self.bloomfilter2.addr2hot)):
                #print('noindex2：%d'%(noindex2))
                if self.bloomfilter2.addr2hot[noindex2] == -1:
                    for listindex1 in range (len(rank2[0])):##
                        #print('-1noindex2：%d'%(noindex2))
                        for noinde1 in range(len(rank1[noindex2][listindex1])):
                            if rank1[noindex2][listindex1][noinde1] != -1:
                                #print('noinde1：%d'%(noinde1))
                                bemapaddr = rank1[noindex2][listindex1][listsize[listindex1] - 1 - noinde1]
                                if isswap == 1:
                                    index = len(lifenowlist) - 1 - mapindex
                                else:
                                    index = mapindex
                                if index < (1<<self.randomshift):
                                    self.climberstart[lifenowlist[index][0]] = 0
                                else:
                                    self.climberstart[lifenowlist[index][0]] = 1
                                self.rank2addr[bemapaddr] = len(lifenowlist) - 1 - mapindex
                                #if self.randomenable == 1 and index < (1<<self.randomshift):
                                if self.randomenable == 1 and index < (((int(self.maxpagenums/2))>>self.randomshift)<<self.randomshift):
                                #if self.randomenable == 1 and index < (self.maxpagenums/2):
                                    index = index ^ self.randomkey
                                if self.maplist[bemapaddr] != lifenowlist[(index)][0] or self.maplist[bemapaddr] == addr:
                                    #不要交换开销
                                    self.lifelist[self.maplist[bemapaddr]][1] = self.lifelist[self.maplist[bemapaddr]][1] - 1
                                    if self.lifelist[self.maplist[bemapaddr]][1] < 0:
                                        return (-1, [self.bloomfilter1.voidlist,self.bloomfilter2.voidlist], self.maplist)
                                self.maplist[bemapaddr] = lifenowlist[(index)][0]
                                self.reverselist[lifenowlist[(index)][0]] = bemapaddr
                                self.climbla2hot[bemapaddr] = (index)
                                #self.life2sorted[bemapaddr] = len(self.sortedlist) - 1 - mapindex
                                mapindex = mapindex + 1 
            #print(mapindex)
            for index3 in range(len(self.bloomfilter1.addr2hot)):#
                if self.bloomfilter1.addr2hot[index3] == -1:
                    bemapaddr = index3
                    if isswap == 1:
                        index = len(lifenowlist) - 1 - mapindex
                    else:
                        index = mapindex
                    if index < (1<<self.randomshift):
                        self.climberstart[lifenowlist[index][0]] = 0
                    else:
                        self.climberstart[lifenowlist[index][0]] = 1
                    if len(lifenowlist) - 1 - mapindex == 0:
                        self.map2wearaddr = bemapaddr
                        #print('map2weakaddr:%d'%(bemapaddr))
                    self.rank2addr[bemapaddr] = len(lifenowlist) - 1 - mapindex
                    if self.randomenable == 1 and index < (((int(self.maxpagenums/2))>>self.randomshift)<<self.randomshift):
                        index = index ^ self.randomkey
                    if self.maplist[bemapaddr] != lifenowlist[(index)][0] or self.maplist[bemapaddr] == addr:
                        #不要交换开销
                        self.lifelist[self.maplist[bemapaddr]][1] = self.lifelist[self.maplist[bemapaddr]][1] - 1
                        if self.lifelist[self.maplist[bemapaddr]][1] < 0:
                            return (-1, [self.bloomfilter1.voidlist,self.bloomfilter2.voidlist], self.maplist)
                    #print(bemapaddr)
                    self.maplist[bemapaddr] = lifenowlist[(index)][0]
                    self.reverselist[lifenowlist[(index)][0]] = bemapaddr
                    self.climbla2hot[bemapaddr] = (index)
                    #self.life2sorted[bemapaddr] = len(self.sortedlist) - 1 - mapindex
                    mapindex = mapindex + 1 
            self.remaptimes = self.remaptimes + 1
            #print('lifenowlist:%d'%lifenowlist[(len(lifenowlist) - 1 - mapindex)][0])
            self.bloomfilter1.clear()
            self.bloomfilter2.clear()
            return (1, [self.bloomfilter1.hotlist,self.bloomfilter2.hotlist], self.maplist)
        self.bloomfilter1.clear()
        self.bloomfilter2.clear()
        return (0, [self.bloomfilter1.voidlist,self.bloomfilter2.voidlist], self.maplist)
    def printstat(self):
        print("write endstat start")
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
