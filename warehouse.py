import random, math

class material:
    def __init__(self, name):
        self.name = name
        self.minStock = 0
        self.maxStock = -1
        self.production = 0
        
    def __str__(self):
        s = " "+self.name+":\n"
        s+= " min stock: "+str(self.minStock)+"\n"
        s+= " production: "+str(self.production)
        return s

class warehouse:
    def __init__(self, wlist):
        self.allWharehouse = wlist
        self.allWharehouse.append(self)
        
        self.productions = {}
        self.content = {}
        self.demand = []
        
        self.capacity = 100
        self.satisfactionRate = 1.
        
    def addProduction(self, name, prod=0):
        mat = material(name)
        mat.production = prod
        self.productions[name] = mat
        #~ self.productions.append(mat)
        
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
            #~ print k
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
        for mat in self.productions.keys():
            p = self.productions[mat]
            if p.production > 0:
                r = random.random()
                if r < p.production and not self.isFull():
                    #~ print "produced ",p.name
                    if p.name in self.content.keys():
                        self.content[p.name] += 1
                    else:
                        self.content[p.name] = 1
        
    def examineDemands(self):
        suppliers = [w for w in self.allWharehouse if w is not self]
        #~ print suppliers
        for p in self.productions:
            m = self.productions[p]
            if m.name not in self.content.keys():
                has = 0
            else:
                has = self.content[m.name]
            toCommand = math.ceil(m.minStock - has)
            toCommand = int(toCommand/max(0.2, self.satisfactionRate))
            m.minStock = 0.9*m.minStock
            #~ print "to command ", toCommand
            if toCommand > 0:
                for i in range(0, toCommand):
                    s = random.choice(suppliers)
                    s.demand.append([m.name, 1, self])

        
    def answerDemands(self):
        nbok = 0
        nbnok = 0
        for d in self.demand:
            toDeliver = 0
            if d[0] not in self.content.keys():
                self.addProduction(d[0])
                self.content[d[0]] = 0
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
                    print self.name, " delivers ",d[0]," to ",d[2].name
                    d[2].content[d[0]] += toDeliver
                    
            self.productions[d[0]].minStock += 0.1*d[1]
                    
        #~ print "nbok ",nbok
        #~ print "nbnok ", nbnok
        if nbok + nbnok >0:
            sat = nbok/(nbok + nbnok)
            self.satisfactionRate = 0.9*self.satisfactionRate + 0.1*sat
        #~ print "satisfaction rate ",self.satisfactionRate
        self.demand = []
        
        
    def __str__(self):
        s = "production :\n"
        for p in self.productions.keys():
            s+= str(self.productions[p])+"\n"
            
        s += "content :\n"
        for p in self.content.keys():
            s+= p + ": "+ str(self.content[p])+"\n"
            
        s+="satisfaction rate: "+str(self.satisfactionRate)
            
        return s
        
        
if __name__=='__main__':
    wlist = []
    w1 = warehouse(wlist)
    w1.name = "w1"
    w2 = warehouse(wlist)
    w2.name = "w2"
    w3 = warehouse(wlist)
    w3.name = "w3"
    w4 = warehouse(wlist)
    w4.name = "w4"
    w5 = warehouse(wlist)
    w5.name = "w5"
    w6 = warehouse(wlist)
    w6.name = "w6"

    w3.addProduction("wood", 0.5)
    w4.addProduction("stone", 0.5)
    w5.addProduction("wood", 0.5)
    w6.addProduction("stone", 0.5)
    
    for i in range(550):
        print "---------------------"
        w1.randomDemand([["wood", 0, 1],["stone", 0, 1]])
        w2.randomDemand([["wood", 0, 1],["stone", 0, 1]])
        for w in wlist:
            w.iterate()
           
    for w in wlist:
        print "%%%%%%%%%%%%"       
        print w

            