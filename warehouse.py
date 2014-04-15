import random

class material:
    def __init__(self, name):
        self.name = name
        self.minStock = 0
        self.maxStock = -1
        self.production = 0

class warehouse:
    def __init__(self, wlist):
        self.allWharehouse = wlist
        self.allWharehouse.append(self)
        
        self.productions = []
        self.content = {}
        self.demand = []
        
        self.capacity = 100
        self.satisfactionRate = 1.
        
    def addProduction(self, name, prod=0):
        mat = material(name)
        mat.production = prod
        self.productions.append(mat)
        
    def randomDemand(self, demand):
        for d in demand:
            i = random.randint(d[1], d[2])
            self.demand.append([d[0], i, None])
            #~ if d[0] in self.demand.keys():
                #~ self.demand[d[0]] += i
            #~ else:
                #~ self.demand[d[0]] = i
        
    def isFull(self):
        all = 0
        for k in self.content:
            print k
            all += self.content[k]
            
        if all>= self.capacity:
            return True
        return False
        
    def iterate(self):
        self.produce()
        self.examineDemands()
        self.answerDemands()
        pass
        
    def produce(self):
        for p in self.productions:
            if p.production > 0:
                r = random.random()
                if r < p.production and not self.isFull():
                    print "produced ",p.name
                    if p.name in self.content.keys():
                        self.content[p.name] += 1
                    else:
                        self.content[p.name] = 1
        
    def examineDemands(self):
        pass
        
    def answerDemands(self):
        nbok = 0
        nbnok = 0
        for d in self.demand:
            toDeliver = 0
            if d[0] not in self.content.keys():
                toDeliver = 0
                nbnok = d[1]
            elif  self.content[d[0]] >= d[1]:
                toDeliver = d[1]
                nbok += d[1]
            else:
                toDeliver = self.content[d[0]] 
                nbok += self.content[d[0]] 
                nbnok += d[1] - self.content[d[0]] 
                
            if toDeliver > 0:
                self.content[d[0]] -= toDeliver
                if d[2] is not None:
                    d[2].content[d[0]] += toDeliver
                    
        print "nbok ",nbok
        print "nbnok ", nbnok
        if nbok + nbnok >0:
            sat = nbok/(nbok + nbnok)
            self.satisfactionRate = 0.9*self.satisfactionRate + 0.1*sat
        print "satisfaction rate ",self.satisfactionRate
        self.demand = []
        
        
if __name__=='__main__':
    wlist = []
    w1 = warehouse(wlist)
    w2 = warehouse(wlist)

    w1.addProduction("wood", 0.5)
    w2.addProduction("stone", 0.5)
    
    for i in range(5):
        print "---------------------"
        w1.randomDemand([["wood", 0, 1],["stone", 0, 1]])
        w2.randomDemand([["wood", 0, 1],["stone", 0, 1]])
        for w in wlist:
            w.iterate()
            
            
            