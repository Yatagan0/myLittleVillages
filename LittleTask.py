import utils, random

from LittlePlace import *

class LittleTask:
    def __init__(self, village):
        self.state = "to do"
        self.status = "to start"
        self.village=village
        self.name ="defaultTaskName"
        self.villager = None
	
    def execute(self):
        print "executing default"
        


class LittleBuildTask(LittleTask):
    def __init__(self, village, name):
        LittleTask.__init__(self, village)
        self.name = name
        self.materials = {}
        self.building = None
        
        if name == "warehouse":
            self.remainingTime = 10
            self.materials["wood"] = 10
            self.materials["stone"] = 10
        elif name == "house":
            self.remainingTime = 10
            self.materials["wood"] = 8
            self.materials["stone"] = 8
            
    def execute(self):
        #~ print self.name, " executing"
        toReturn = {}
        if self.status == "to start":
            #select position
            #add bring items
            self.building= LittleBuilding()
            self.building.name = self.name
            posX = 0
            posY = 0
            size = 0
            while( not self.village.positionFree(posX, posY)):
                print "r"
                size +=1
                posX = random.randint(-size, size)
                posY= random.randint(-size, size)
               
            self.building.position = [posX, posY]
            print "end pos for ", self.name, " ", self.building.position 
        
            for m in self.materials:
                for i in range(self.materials[m]):
                    lct = LittleCarryTask(self.village)
                    lct.material = m
                    lct.destination = self.building.position 
                    lct.dependantTask = self
                    self.village.toDoList.append(lct)
               
            self.status = "waiting for materials"
        elif self.status == "waiting for materials":
            #check if remaining materials
            canContinue = True
            for m in self.materials:
                if self.materials[m] > 0:
                    canContinue = False
            if canContinue:
                self.status = "building"
        elif self.status == "building":
            #check if remaining time
            self.village.buildings.append(self.building)
            self.status = "done"
        return toReturn
            

class LittleCarryTask(LittleTask):
    def __init__(self, village):
        LittleTask.__init__(self, village)
        self.name = "carryTask"
        self.dependantTask = None
        self.material = ""
        self.destination = [0, 0]
        
    def execute(self):
        #~ print self.name, " executing"
        if self.status == "to start":
            self.goalBuilding = self.getClosestBuilding("warehouse", self.destination, 1)
            self.goalBuilding = self.goalBuilding[0]
            print "goal position ",self.goalBuilding.position
            self.status = "getting material"
        elif self.status == "getting material":
            if self.villager.goto(self.goalBuilding.position):
                self.status = "carrying material"
        elif self.status == "carrying material":
            if self.villager.goto(self.destination):
                self.status = "carrying material"
            self.dependantTask.materials[self.material] -= 1
            self.status = "done"
            
    def getClosestBuilding(self, buildingName, destination, nb):
        listToSort = []
        for b in self.village.buildings:
            if b.name == buildingName:
                listToSort.append([b, 1*utils.distance(self.villager.position, b.position) + 1*utils.distance(destination, b.position) ])
        #~ print "non sorted list ",listToSort
        sortedList = sorted(listToSort,  key=lambda tup: tup[1])
        #~ print "sorted list ",sortedList 
        result = []
        for i in range(min(nb, len(sortedList))):
            result.append(sortedList[i][0])

        return result
        
class LittleWorkTask(LittleTask):
    def __init__(self, village):
        LittleTask.__init__(self, village)
        
if __name__ == '__main__':
    lbt = LittleBuildTask()
