import utils, random

from LittlePlace import *
import xml.etree.ElementTree as ET

global taskID 
taskID = 0

class LittleTask:
    def __init__(self, village):
        self.state = "to do"
        self.status = "to start"
        self.village=village
        self.name ="defaultTaskName"
        self.type = "task"
        self.villager = None
        self.salary = 0.0
        
        self.mandatory = True
        
        global taskID
        self.id = taskID
        taskID += 1
 
    def execute(self):
        print "executing default"

    def canPerform(self):
        #~ print "default perform"
        return self.status != "done" and self.state == "to do"
        #~ return True
        

    def readTask(self, elem):
        att = elem.attrib
        self.name = att["name"]
        self.type = att["type"]
        self.state = att["state"]
        self.status = att["status"]
        #~ self.villager = att["villager"]
        self.salary = float(att["salary"])
        self.mandatory = att["mandatory"]=="True"
        #~ print "read ",att["mandatory"], " understood ", self.mandatory 
        
        self.id = int(att["id"])
        #~ print "created task ",self.id
        
        global taskID
        if self.id >= taskID:
            taskID = self.id +1
            
    def writeTask(self, root):
        building = ET.SubElement(root, 'task')
        building.set("name", self.name)
        building.set("type", self.type)
        building.set("state", self.state)
        building.set("id", str(self.id))
        building.set("status", self.status)
        #~ building.set("villager", str(self.villager.name))
        building.set("salary", str(self.salary))

        building.set("mandatory", str(self.mandatory))

            
        return building  


class LittleBuildTask(LittleTask):
    def __init__(self, village, name):
        LittleTask.__init__(self, village)
        self.name = name
        self.materials = {}
        self.building = None
        self.buildingtype = ""
        self.pos = []
        
        self.type = "build"
        
        if name == "warehouse":
            self.remainingTime = 10
            self.materials["wood"] = 10
            self.materials["stone"] = 10
            self.buildingtype = "storage"
        elif name == "house":
            self.remainingTime = 10
            self.materials["wood"] = 8
            self.materials["stone"] = 8
            self.buildingtype = "house"
        elif name == "field":
            self.remainingTime = 3
            self.materials["wood"] = 1
            self.buildingtype = "field"
        elif name == "forest":
            self.remainingTime = 1
            self.buildingtype = "field"
        elif name == "woodcutter":
            self.remainingTime = 10
            self.materials["wood"] = 10
            self.materials["stone"] = 10
            self.buildingtype = "production"
        elif name == "stonecutter":
            self.remainingTime = 10
            self.materials["wood"] = 10
            self.materials["stone"] = 10
            self.buildingtype = "production"
            
        #WARNING, to redo !
        self.salary = 1
        #~ self.salary = 1 + 1*self.materials["wood"]  + 1*self.materials["stone"]  + 1*self.remainingTime


    def readTask(self, elem):
        att = elem.attrib
        LittleTask.readTask(self, elem)
        if int(att["building"]) == -1:
            self.building = None
            
        else:
            self.building = int(att["building"])
            
        if "positionX" in att.keys():
            self.pos = [0, 0]
            self.pos[0] = int(att["positionX"])
            self.pos[1] = int(att["positionY"])
            
        self.buildingtype = att["buildingType"]
        
        self.remainingTime = int(att["remainingTime"])
        for child in elem:
            if (child.tag == "material"):
                attm = child.attrib
                self.materials[attm["name"]] = int(attm["quantity"])

            
    def writeTask(self, root):
        subelem = LittleTask.writeTask(self, root)

        if self.building is not None:
            subelem.set("building", str(self.building.id))
            
        else:
            subelem.set("building", str(-1))
            
        if len(self.pos)==2:
            subelem.set("positionX", str(self.pos[0]))
            subelem.set("positionY", str(self.pos[1]))
        
        subelem.set("buildingType", self.buildingtype)
        
        subelem.set("remainingTime", str(self.remainingTime))
        
        for m in self.materials.keys():
            mat = ET.SubElement(subelem, 'material')
            mat.set("name", m)
            mat.set("quantity", str(self.materials[m]))


            
    def execute(self):
        #~ print self.name, " executing"
        if self.status == "to start":
            #select position
            #add bring items
            if self.pos == []:
                posX = 0
                posY = 0
                size = 0
                while( not self.village.positionFree(posX, posY)):
                    size +=1
                    posX = random.randint(-size, size)
                    posY= random.randint(-size, size)
                self.pos = [posX, posY]
                #~ print "end pos for ", self.name, " ", self.building.position 
            elif self.villager.goto(self.pos):
                if not self.village.positionFree(self.pos[0], self.pos[1]):
                    self.pos = []
                else:
                    self.building = newBuilding(self.buildingtype, self.name, self.pos, "in construction", self.village)


                    for m in self.materials:
                        for i in range(self.materials[m]):
                            lct = LittleCarryTask(self.village, "warehouse", self.building, m)
                            #~ lct.material = m
                            #~ lct.destination = self.building.position 
                            #~ lct.dependantTask = self
                            lct.salary = 1
                            self.village.toDoList.append(lct)
                           
                    self.status = "waiting for materials"
                    self.villager.money += 1
                    return True
        elif self.status == "waiting for materials":
            #check if remaining materials
            self.status = "building"
            return True

        elif self.status == "building":
            #check if remaining time
            self.remainingTime -=1
            self.villager.money += 1
            if self.remainingTime == 0:
                for m in self.materials:
                    self.building.getMaterial(m, self.materials[m])
                
                
                self.building.state = "ok"
                if self.building.type == "production":
                    if self.name == "stonecutter":
                        self.building.startProducing("stone", 5, 1)
                    elif self.name == "woodcutter":
                        self.building.startProducing("wood", 3, 1)
                print self.building.name, "finished in ", self.building.position
                self.status = "done"
                
                return True
            return True
                
        return False
        
    def canPerform(self):
        if self.status == "waiting for materials" and self.state == "to do":
            for m in self.materials:
                #~ if self.materials[m] > 0:
                if m not in self.building.content.keys():
                    #~ print self.id," cant parform : ",m," not known in ", self.building.id
                    return False
                if self.building.content[m] < self.materials[m]:
                    #~ print self.id," cant perform, not enough ",m," in ",self.building.id
                    #~ print "cannot perform"
                    return False
        #~ print "can perform"
        return self.status != "done" and self.state == "to do"

            

class LittleCarryTask(LittleTask):
    def __init__(self, village, initial = None, goal = None, material = None):
        LittleTask.__init__(self, village)
        self.name = "carryTask"
        #~ self.dependantTask = None
        self.material = material
        self.goal = goal
        self.initial = initial
        self.type = "carry"
 
    def readTask(self, elem):
        att = elem.attrib
        LittleTask.readTask(self, elem)
        self.material = att["material"]
        if "initialName" in att.keys():
            self.initial = att["initialName"]
        else:
            self.initial = int(att["initial"])
            
        if "goalName" in att.keys():
            self.goal = att["goalName"]
        else:
            self.goal = int(att["goal"])

            
    def writeTask(self, root):
        subelem = LittleTask.writeTask(self, root)

        subelem.set("material", self.material)
        if isinstance(self.initial, basestring):
            subelem.set("initialName", self.initial)
        else:
            subelem.set("initial", str(self.initial.id))
            
        if isinstance(self.goal, basestring):
            subelem.set("goalName", self.goal)
        else:
            subelem.set("goal", str(self.goal.id))

        
    def execute(self):
        #~ print self.name, " executing"
        if self.status == "to start":
            #both can't be string
            if isinstance(self.goal, basestring):
                #~ self.goallist = self.getClosestBuilding(self.goal, self.initial.position, 1)
                self.goallist = self.village.getClosestBuilding(self.goal, self.initial.position)

                if self.goal == self.initial.name:
                    self.goallist.pop(0)
                self.goal = self.goallist[0]
            elif isinstance(self.initial, basestring):
                #~ self.initiallist = self.getClosestBuilding(self.initial, self.goal.position, 1)
                self.initiallist = self.village.getClosestBuilding(self.initial, self.goal.position, self.villager.position)
                if self.goal.name == self.initial and not  self.goal.state == "in construction":
                    self.initiallist.pop(0)
                self.initial = self.initiallist[0]
            #~ print "goal position ",self.goalBuilding.name ," ",self.goalBuilding.position
            self.status = "getting material"
            
        elif self.status == "getting material":
            #~ print "before goto1 ",self.goalBuilding.name ," ",self.goalBuilding.position
            if self.villager.goto(self.initial.position):
                
                if self.initial.getMaterial(self.material, 1, self.mandatory):
                    self.status = "carrying material"
                    self.villager.carrying = self.material
                else:
                    print "there is no ",self.material," here"
                    self.status = "fail"
                    return True

        elif self.status == "carrying material":
            #~ print "before goto2 ",self.goalBuilding.name ," ",self.goalBuilding.position
            if self.villager.goto(self.goal.position):
            #~ if self.villager.goto(self.goalBuilding.position):
                self.goal.setMaterial(self.material, 1)
                self.villager.carrying = ""
                #~ if self.dependantTask is not None:
                    #~ self.dependantTask.setMaterial(self.material, 1)
                print self.material, "carried in ", self.goal.name
                self.status = "done"
                self.villager.money += self.salary
                #~ print "after goto 2 ",self.goalBuilding.name ," ",self.goalBuilding.position
                return True
            #~ print "after goto 2BIS ",self.goalBuilding.name ," ",self.goalBuilding.position
        return False
            

        
class LittleWorkTask(LittleTask):
    def __init__(self, workshop, village):
        LittleTask.__init__(self, village)
        if workshop is not None:
            self.workshop = workshop
            self.remainingTime = self.workshop.productionTime
        else:
            self.workshop = None
        self.type = "production"

    def readTask(self, elem):
        att = elem.attrib
        LittleTask.readTask(self, elem)
        #~ if "workshop" in att.keys():
        self.workshop = int(att["workshop"])
        self.remainingTime = int(att["remainingTime"])
        #~ print "read remaining time ",self.remainingTime

            
    def writeTask(self, root):
        #~ print "wrinting work task"
        subelem = LittleTask.writeTask(self, root)
        if self.workshop is not None:
            subelem.set("workshop", str(self.workshop.id))
            subelem.set("remainingTime", str(self.remainingTime))
        else:
            print "warning, workTask ",self.id," has no workshop"
        #~ print "finished wrinting work atsk"

        
    def execute(self):
        if self.status == "to start":
            if self.villager.goto(self.workshop.position):
                self.status = "producing"
                return False
        elif self.status == "producing":
            if self.remainingTime > 0:
                print "producing ",self.workshop.production
                print "remaining time ",self.remainingTime
                self.remainingTime -=1
                return False
            
            print "produced ",self.workshop.production
            self.workshop.setMaterial(self.workshop.production, 1)
            lct = LittleCarryTask(self.village, self.workshop,  "warehouse",  self.workshop.production)
            #~ lct.dependantTask = self
            lct.salary = 1
            self.village.toDoList.append(lct)
            self.village.addProductionTask(self.workshop)
            
            self.status = "done"
            #~ self.villager.money += self.salary
            return True
        
        
if __name__ == '__main__':
    lbt = LittleBuildTask()
