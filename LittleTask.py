import utils, random, copy

#from LittlePlace import *
import xml.etree.ElementTree as ET

global taskID 
taskID = 0

class LittleTask:
    def __init__(self, village, owner=None):
        self.state = "to do"
        self.status = "to start"
        self.village=village
        self.name ="defaultTaskName"
        self.type = "task"
        self.villager = None
        self.salary = 0.0
        
        self.mandatory = True
        
        self.owner = owner
        
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
        
        if "owner" in att.keys():
            self.owner = att["owner"]
        
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
        
        if self.owner is not None:
            building.set("owner", str(self.owner.name))

            
        return building  


class LittleBuildTask(LittleTask):
    def __init__(self, village, name, position = [0,0], owner=None):

        LittleTask.__init__(self, village, owner)

        self.name = name
        self.materials = {}
        self.building = None
        self.buildingtype = ""
        self.pos = position
        self.hasPos = False
        
        self.owner = owner

        self.type = "build"
        
        if name in utils.allWorkshops.keys():
            tobuild = utils.allWorkshops[name]
            
            self.remainingTime = tobuild.buildTime
            
            self.materials = copy.deepcopy(tobuild.build)
            
            print "need ",self.remainingTime," time to build"
        
        if name == "warehouse":
            #~ self.remainingTime = 10
            #~ self.materials["wood"] = 10
            #~ self.materials["stone"] = 10
            self.buildingtype = "storage"
        elif name == "house":
            #~ self.remainingTime = 10
            #~ self.materials["wood"] = 8
            #~ self.materials["stone"] = 8
            self.buildingtype = "house"
        elif name == "field":
            self.remainingTime = 3
            self.materials["wood"] = 1
            self.buildingtype = "field"
        elif name == "forest":
            self.remainingTime = 1
            self.buildingtype = "field"
        elif name == "woodcutter":
            #~ self.remainingTime = 10
            #~ self.materials["wood"] = 10
            #~ self.materials["stone"] = 10
            self.buildingtype = "production"
        elif name == "stonecutter":
            #~ self.remainingTime = 10
            #~ self.materials["wood"] = 10
            #~ self.materials["stone"] = 10
            self.buildingtype = "production"
            
        #WARNING, to redo !
        self.salary = 1.
        #~ self.salary = 1 + 1*self.materials["wood"]  + 1*self.materials["stone"]  + 1*self.remainingTime


    def readTask(self, elem):
        att = elem.attrib
        LittleTask.readTask(self, elem)
        if int(att["building"]) == -1:
            self.building = None
            
        else:
            self.building = int(att["building"])
            
        #~ if "positionX" in att.keys():
        self.pos = [0, 0]
        self.pos[0] = int(att["positionX"])
        self.pos[1] = int(att["positionY"])
        self.hasPos = att["hasPos"]=="True"
            
        self.buildingtype = att["buildingType"]
        
        self.remainingTime = int(att["remainingTime"])
        for child in elem:
            if (child.tag == "material"):
                attm = child.attrib
                self.materials[attm["name"]] = int(attm["quantity"])
                
        if "owner" in att.keys():
            self.owner = att["owner"]

            
    def writeTask(self, root):
        subelem = LittleTask.writeTask(self, root)

        if self.building is not None:
            subelem.set("building", str(self.building.id))
            
        else:
            subelem.set("building", str(-1))
            
        subelem.set("positionX", str(self.pos[0]))
        subelem.set("positionY", str(self.pos[1]))
        subelem.set("hasPos", str(self.hasPos))
        
        subelem.set("buildingType", self.buildingtype)
        
        subelem.set("remainingTime", str(self.remainingTime))
        
        for m in self.materials.keys():
            mat = ET.SubElement(subelem, 'material')
            mat.set("name", m)
            mat.set("quantity", str(self.materials[m]))
        
        if self.owner is not None:
            subelem.set("owner", str(self.owner.name))



            
    def execute(self):
        #~ print self.name, " executing"
        if self.status == "to start":
            #select position
            #add bring items
            if not self.hasPos:
                print "self.pos ",self.pos
                posX = int(self.pos[0])
                posY = int(self.pos[1])
                size = 0
                while( not self.village.positionFree(posX, posY)):
                    size +=1
                    posX = random.randint(-size+self.pos[0], size+self.pos[0])
                    posY= random.randint(-size+self.pos[1], size+self.pos[1])
                self.pos = [posX, posY]
                self.hasPos = True
                #~ print "end pos for ", self.name, " ", self.building.position 
            elif self.villager.goto(self.pos):
                if not self.village.positionFree(self.pos[0], self.pos[1]): #position has been occupied the imewe arrive
                    self.hasPos = False
                else:
                    self.building = self.village.addNewBuilding(self.buildingtype, self.name, self.pos, "in construction")
                    if self.owner is not None:
                        self.owner.addProperty(self.building)

                    for m in self.materials:
                        for i in range(self.materials[m]):
                            #~ print "adding carry tasks"
                            lct = LittleCarryTask(self.village, "warehouse", self.building, m)
                            #~ lct.material = m
                            #~ lct.destination = self.building.position 
                            #~ lct.dependantTask = self
                            lct.salary = 1.
                            #~ self.village.toDoList.append(lct)
                            self.building.addTask(lct)
                           
                    #~ print len(self.village.toDoList), " tasks in village task"
                    print self.building.id, " is now waiting for materials"
                    self.status = "waiting for materials"
                    self.villager.money += 1
                    return True
        elif self.status == "waiting for materials":
            #check if remaining materials
            self.status = "building"
            print  self.building.name, self.building.id," passing to state building"
            for m in self.materials:
                
                if not self.building.getMaterial(m, self.materials[m]):
                    print "WARNING, could not remove materials from ", self.building.name, self.building.id
            return False

        elif self.status == "building":
            if self.villager.goto(self.pos):
                #check if remaining time
                self.remainingTime -=1
                self.villager.money += 1
                print "finishing ",self.building.name
                if self.remainingTime == 0:

                    self.building.state = "ok"
                    if self.building.type == "production":
                        if self.name == "stonecutter":
                            self.building.startProducing("stone", 5, 1)
                        elif self.name == "woodcutter":
                            self.building.startProducing("wood", 3, 1)
                    print self.building.name, "finished in ", self.building.position
                    
                    
                    
                    self.status = "done"
                return True
                
        return False
        
    def canPerform(self):
        #~ print "can perform ? ",self.status,self.id
        if self.status == "waiting for materials" and self.state == "to do":
            #~ print "testing if all materials are present"
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
        return  LittleTask.canPerform(self) #  self.status != "done" and self.state == "to do"

            

class LittleCarryTask(LittleTask):
    def __init__(self, village, initial = None, goal = None, material = None):
        LittleTask.__init__(self, village)
        self.name = "carryTask"
        #~ self.dependantTask = None
        self.material = material
        self.goal = goal
        self.initial = initial
        self.knownGoal = (goal is not None)
        self.type = "carry"
        self.salary = 1.0
 
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
            
        self.knownGoal = bool(att["knownGoal"])
            
        #~ print "read initial ",self.initial
        #~ print "read goal ", self.goal

            
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
            
        subelem.set("knownGoal", str(self.knownGoal))

        
    def execute(self):
        #~ print self.name, " executing"
        if self.status == "to start":
            #both can't be string
            if isinstance(self.goal, basestring):
                #~ self.goallist = self.getClosestBuilding(self.goal, self.initial.position, 1)
                goallist = self.village.getClosestBuilding(self.goal, self.initial.position)

                #~ if self.goal == self.initial.name:
                    #~ goallist.pop(0)
                if len(goallist)==0:
                    print "warning, could not find a ",self.goal," to set for goal"
                self.goal = goallist[0]
            
            if isinstance(self.initial, basestring):
                #~ self.initiallist = self.getClosestBuilding(self.initial, self.goal.position, 1)
                initiallist = self.village.getClosestBuilding(self.initial, self.goal.position, self.villager.position)
                #~ if self.goal.name == self.initial and not  self.goal.state == "in construction":
                    #~ initiallist.pop(0)
                if len(initiallist)==0:
                    print "warning, could not find a ",self.initial," to set for initial"
                self.initial = initiallist[0]
            #~ print "goal position ",self.goalBuilding.name ," ",self.goalBuilding.position
            self.status = "getting material"
            
        elif self.status == "getting material":
            #~ print "getting material of task ",self.id
            #~ print "initial ",self.initial
            #~ print "before goto1 ",self.goalBuilding.name ," ",self.goalBuilding.position
            if self.villager.goto(self.initial.position):
                #~ print "test1"
                if self.initial.getMaterial(self.material, 1, self.mandatory):
                    self.status = "carrying material"
                    #~ print "i got some ",self.material," here"
                    self.villager.carrying = self.material
                else:
                    print "there is no ",self.material," here"
                    self.status = "fail"
                    if self.mandatory:
                        if self.knownGoal:
                            askingName = self.material
                            askingPos = [self.goal.position[0], self.goal.position[1]] 
                        else:
                            askingName = self.materials
                            askingPos = [self.initial.position[0], self.initial.position[1]]
                            
                            
                            
                        print "adding ",askingName," to asked buildngs in pos ",askingPos
                        if askingName in self.village.askedBuildings:
                                self.village.askedBuildings[askingName].append(askingPos)
                        else:
                            self.village.askedBuildings[askingName] = [askingPos]
                    
                    return True

        elif self.status == "carrying material":
            #~ print "before goto2 ",self.goalBuilding.name ," ",self.goalBuilding.position
            if self.villager.goto(self.goal.position):
                #~ print "test2"
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
            self.salary = self.remainingTime
            self.name = "produce"+self.workshop.production
        else:
            self.workshop = None
        self.type = "production"
        
         

    def readTask(self, elem):
        att = elem.attrib
        LittleTask.readTask(self, elem)
        #~ if "workshop" in att.keys():
        self.workshop = int(att["workshop"])
        self.remainingTime = int(att["remainingTime"])
        #~ self.salary = self.workshop.productionTime
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
            self.workshop.addTask(lct)
            self.village.addProductionTask(self.workshop)
            
            self.status = "done"
            #~ self.villager.money += self.salary
            return True
        
        
if __name__ == '__main__':
    lbt = LittleBuildTask()
