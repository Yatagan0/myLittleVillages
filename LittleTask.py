import utils, random

from LittlePlace import *

global taskID 
taskID = 0

class LittleTask:
    def __init__(self, village):
        self.state = "to do"
        self.status = "to start"
        self.village=village
        self.name ="defaultTaskName"
        self.villager = None
        self.salary = 0.0
        global taskID
        self.id = taskID
        taskID += 1
 
    def execute(self):
        print "executing default"

    def canPerform(self):
        #~ print "default perform"
	return self.status != "done" and self.state == "to do"
        #~ return True


class LittleBuildTask(LittleTask):
    def __init__(self, village, name):
        LittleTask.__init__(self, village)
        self.name = name
        self.materials = {}
        self.building = None
        self.isBuilding = True
        
        if name == "warehouse":
            self.remainingTime = 10
            self.materials["wood"] = 10
            self.materials["stone"] = 10
        elif name == "house":
            self.remainingTime = 10
            self.materials["wood"] = 8
            self.materials["stone"] = 8
        elif name == "field":
            self.remainingTime = 3
            self.isBuilding = False
            self.materials["wood"] = 1
        elif name == "forest":
            self.remainingTime = 1
            self.isBuilding = False
            
        
        self.salary = 1 + 1*self.materials["wood"]  + 1*self.materials["wood"]  + 1*self.remainingTime
            
    def execute(self):
        #~ print self.name, " executing"
        if self.status == "to start":
            #select position
            #add bring items
            if self.building == None:
                self.building= LittleBuilding()
                self.building.name = self.name+" - in construction"
                posX = 0
                posY = 0
                size = 0
                while( not self.village.positionFree(posX, posY)):
                    size +=1
                    posX = random.randint(-size, size)
                    posY= random.randint(-size, size)
                   
                self.building.position = [posX, posY]
                print "end pos for ", self.name, " ", self.building.position 
                if self.isBuilding:
                    self.village.buildings.append(self.building)
                else:
                    self.village.places.append(self.building)
            if self.villager.goto(self.building.position):

        
                for m in self.materials:
                    for i in range(self.materials[m]):
                        lct = LittleCarryTask(self.village)
                        lct.material = m
                        lct.destination = self.building.position 
                        lct.dependantTask = self
                        lct.salary = 1
                        self.village.toDoList.append(lct)
                   
                self.status = "waiting for materials"
                self.villager.money += 1
                return True
        elif self.status == "waiting for materials":
            #check if remaining materials
            canContinue = True
            for m in self.materials:
                if self.materials[m] > 0:
                    canContinue = False
            if canContinue:
                self.status = "building"
            return True
        elif self.status == "building":
            #check if remaining time
            self.remainingTime -=1
            self.villager.money += 1
            if self.remainingTime == 0:
                self.building.name = self.name
                
                print self.building.name, "finished in ", self.building.position
                self.status = "done"
                
                return True
            return True
                
        return False
        
    def canPerform(self):
        if self.status == "waiting for materials" and self.state == "to do":
            for m in self.materials:
                if self.materials[m] > 0:
                    #~ print "cannot perform"
                    return False
        #~ print "can perform"
        return self.status != "done" and self.state == "to do"

            

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
            #~ print "goal position ",self.goalBuilding.name ," ",self.goalBuilding.position
            self.status = "getting material"
            
        elif self.status == "getting material":
            #~ print "before goto1 ",self.goalBuilding.name ," ",self.goalBuilding.position
            if self.villager.goto(self.goalBuilding.position):
                self.status = "carrying material"
                self.villager.carrying = self.material
                #~ print "after goto1 ",self.goalBuilding.name ," ",self.goalBuilding.position
                
            #~ print "after goto 1BIS ",self.goalBuilding.name ," ",self.goalBuilding.position
        elif self.status == "carrying material":
            #~ print "before goto2 ",self.goalBuilding.name ," ",self.goalBuilding.position
            if self.villager.goto(self.destination):
            #~ if self.villager.goto(self.goalBuilding.position):
                self.dependantTask.materials[self.material] -= 1
                self.villager.carrying = ""
                print self.material, "carried in ", self.destination
                self.status = "done"
                self.villager.money += self.salary
                #~ print "after goto 2 ",self.goalBuilding.name ," ",self.goalBuilding.position
                return True
            #~ print "after goto 2BIS ",self.goalBuilding.name ," ",self.goalBuilding.position
        return False
            
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
        #~ for r in result:
            #~ print r.name," ",r.position
        
        return result
        
class LittleWorkTask(LittleTask):
    def __init__(self, village):
        LittleTask.__init__(self, village)
        
if __name__ == '__main__':
    lbt = LittleBuildTask()
