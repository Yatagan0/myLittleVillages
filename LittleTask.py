import utils, random

from LittlePlace import *

class LittleTask:
    def __init__(self, village):
        self.state = "to do"
        self.status = "to start"
        self.village=village
        self.name ="defaultTaskName"
        
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
                size +=1
                posX = random.randint(-size, size)
                posY= random.randint(-size, size)
               
            self.building.position = [posX, posY]
            print "end pos for ", self.name, " ", self.building.position 
        
            for m in self.materials:
                for i in range(self.materials[m]):
                    lct = LittleCarryTask(self.village)
                    lct.material = m
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
        
    def execute(self):
        if self.status == "to start":
            self.status = "getting material"
        elif self.status == "getting material":
            self.status = "carrying material"
        elif self.status == "carrying material":
            self.dependantTask.materials[self.material] -= 1
            self.status = "done"
        
class LittleWorkTask(LittleTask):
    def __init__(self, village):
        LittleTask.__init__(self, village)
        
if __name__ == '__main__':
    lbt = LittleBuildTask()
