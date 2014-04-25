import random, utils

from LittleVillager import *
from LittleTask import *
from LittlePlace import *


class LittleVillage:
    def __init__(self):
        self.toDoList = []
        self.villagers = []
        self.places=[]
        self.buildings=[]
        self.globalPosition = [0.,0.]
        self.name = "defaultVillageName"
        self.carrying = ""
        
    def readVillage(self, file):
        print "bla"
        
    def writeVillage(self, file):
        print "bla"
        
    def createRandomVillage(self, num):
        startName = utils.allU 
        middleName = utils.allL 
        endName = ["touille", "mont", "vert", "gny", "leaux", "rrand", "lieu", "guen"]
        self.name= startName[random.randint(0, len(startName)-1)]+middleName[random.randint(0, len(middleName)-1)]+endName[random.randint(0, len(endName)-1)]

        for i in range(num):
            lv = LittleVillager()
            lv.generate()
            self.villagers.append(lv)
            
        newBuilding("storage", "warehouse", [0, -2], "ok", self)
        self.buildings[0].setMaterial("stone", 40)
        self.buildings[0].setMaterial("wood", 10)
        newBuilding("production", "woodcutter", [0, 4], "ok", self)
        self.buildings[1].startProducing("wood", 3, 1)
        newBuilding("storage", "warehouse", [0, 3], "ok", self)
        
    def __str__(self):
        s = "This is the village of "+self.name
        s += "\ninhabitants :"
        for v in self.villagers:
            s += "\n"+v.name+ " "+ str(v.position)+" "+str(v.money)
        for b in self.buildings:
            #~ s += "\n"+b.name+ " "+ str(b.position)
            s+= "\n"+str(b)
        return s
        
    def positionFree(self, x, y):
        for b in self.buildings:
            if b.position[0] == x and b.position[1] == y :
                #~ print "position ",x, " ",y, "not free : ",b.name
                return False
        return True

    def addProductionTask(self, workshop):
        lwt = LittleWorkTask(workshop)
        self.toDoList.append(lwt)
        
    def addCarryTask(self, fromB,toB, mat, mandatory = True):
        if fromB.id == toB.id:
            return
        lct = LittleCarryTask(self, fromB, toB, mat)
        lct.mandatory = mandatory
        self.toDoList.append(lct)


    def getClosestBuilding(self, buildingName, destination, villagerpos = None, nb=1):
        listToSort = []
        for b in self.buildings:
            if b.name == buildingName and b.state=="ok":
                if villagerpos is not None:
                    listToSort.append([b, 1*utils.distance(villagerpos, b.position) + 1*utils.distance(destination, b.position) ])
                else:
                    listToSort.append([b, utils.distance(destination, b.position) ])

        sortedList = sorted(listToSort,  key=lambda tup: tup[1])
        result = []
        for i in range(min(nb, len(sortedList))):
            result.append(sortedList[i][0])
        
        return result
        
    def iterate(self):
        print "--------------------"
        for p in self.villagers:
            if not p.busy:
                #~ print "select"
                p.selectTask(self.toDoList)
            else:
                #~ print "perform"
                toDoNow = p.performTask()
               
                
        
        inds = range(len(self.toDoList))
        inds.reverse()
        for i in inds:
            if self.toDoList[i].status == "done":
                #~ print self.toDoList[i].name, " finished"
                self.toDoList.pop(i)
            elif self.toDoList[i].status == "fail":
                if not self.toDoList[i].mandatory:
                    self.toDoList.pop(i)
                elif random.randint(0, 9) == 0:
                    t = self.toDoList.pop(i)
                    t.status = "to start"
                    self.toDoList.append(t)
                    print "postponning task ",t.id
                    
            

if __name__ == '__main__':
    lv = LittleVillage()
    lv.createRandomVillage(10)
    
    lbt = LittleBuildTask(lv, "warehouse")
    lv.toDoList.append(lbt)
    lbt = LittleBuildTask(lv, "house")
    lv.toDoList.append(lbt)
    lbt = LittleBuildTask(lv, "house")
    lv.toDoList.append(lbt)
    for i in range(50):
        #~ print "iterate"
        lv.iterate()
        
    print lv
