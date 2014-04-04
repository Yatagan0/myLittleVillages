import random, utils

from LittleVillager import *
from LittlePlace import *
from LittleTask import *

class LittleVillage:
    def __init__(self):
        self.toDoList = []
        self.villagers = []
        self.places=[]
        self.buildings=[]
        self.globalPosition = [0.,0.]
        self.name = "defaultVillageName"
        
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
            
        entrepot = LittleBuilding()
        entrepot.name = "Warehouse"
        self.buildings.append(entrepot)
        
    def __str__(self):
        s = "This is the village of "+self.name
        s += "\ninhabitants :"
        for v in self.villagers:
            s += "\n"+v.name+ " "+ str(v.gender)
        for b in self.buildings:
            s += "\n"+b.name
        return s
        
    def positionFree(self, x, y):
        for b in self.buildings:
            if b.position[0] == x and b.position[1] == y :
                return False
        return True
        
    def iterate(self):
        for p in self.villagers:
            if not p.busy:
                #~ print "test"
                p.selectTask(self.toDoList)
            else:
                toDoNow = p.performTask()
               
                
        
        inds = range(len(self.toDoList))
        inds.reverse()
        for i in inds:
            if self.toDoList[i].status == "done":
                print self.toDoList[i].name, " finished"
                self.toDoList.pop(i)
            

if __name__ == '__main__':
    lv = LittleVillage()
    lv.createRandomVillage(10)
    
    lbt = LittleBuildTask(lv, "warehouse")
    lv.toDoList.append(lbt)
    lbt = LittleBuildTask(lv, "house")
    lv.toDoList.append(lbt)
    lbt = LittleBuildTask(lv, "house")
    lv.toDoList.append(lbt)
    for i in range(25):
        lv.iterate()
        
    print lv
