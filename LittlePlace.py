import utils, random
import xml.etree.ElementTree as ET

from LittleTask import *

global taskID 
taskID = 0

class LittlePlace:
    def __init__(self, village):
        self.name = "defaultPlaceName"
        self.type = "defaultPlaceType"
        self.position =[0, 0]
        self.content = {}
        self.state = "ok"
        
        self.village = village
        self.taskList = []
        

        
    def writeBuilding(self, root):
        building = ET.SubElement(root, 'building')
        building.set("name", self.name)
        building.set("type", self.type)
        building.set("state", self.state)
        building.set("id", str(self.id))
        building.set("positionX", str(self.position[0]))
        building.set("positionY", str(self.position[1]))
        for m in self.content.keys():
            mat = ET.SubElement(building, 'material')
            mat.set("name", m)
            mat.set("quantity", str(self.content[m]))
            
        for t in self.taskList:
            t.writeTask(building)
            
        return building
        

    def readBuilding(self, elem):
        att = elem.attrib
        self.name = att["name"]
        self.type = att["type"]
        
        
        self.state = att["state"]
        self.id = int(att["id"])
        
        global taskID
        if self.id >= taskID:
            taskID = self.id +1
        
        
        self.position[0] = int(att["positionX"])
        self.position[1] = int(att["positionY"])
        for child in elem:
            if (child.tag == "material"):
                attm = child.attrib
                self.content[attm["name"]] = int(attm["quantity"])
                
            if(child.tag == "task"):
                type = child.attrib["type"] 
                name = ""
                 
                if type == "build":
                    t =  LittleBuildTask( self.village, name)
                elif type == "carry":
                    t = LittleCarryTask( self.village)
                elif type == "production":
                    t = LittleWorkTask( None, None, self.village)

                 
                t.readTask(child)
                self.addTask(t)
                #~ self.taskList.append(t)
                #TODO : identify villagers and buildings
        
            #~ self.writeWorkshop(building)
        
    def getMaterial(self, mat, num, mandatory=True):
        if mat not in self.content.keys():
            self.content[mat] = 0
            #~ print "no ",mat," here"
            return False
        if self.content[mat] < num:
            #~ print "no ",mat," here"
            return False
        self.content[mat] -= num
        print "got ",num," ",mat," from ",self.id," remaining : ",self.content[mat]
        return True
        
    def setMaterial(self, mat, num):
        #Todo check capacity
        if mat not in self.content.keys():
            self.content[mat] = num
        else:
            self.content[mat] += num
        print "adding ",num," ",mat," in ",self.id," there is now ",self.content[mat]
        
    def __str__(self):
        s = self.name+ " "+ str(self.position)
        #~ print "printing ",self.name
        #~ s=" "+str(self.id)
        if not self.state == "ok":
                s+= " ("+self.state+")"
        for m in self.content.keys():
            s += "\n  "+m+" "+str(self.content[m])
            
        return s
        
        
    def addTask(self, task):
        #~ print "bla"
        self.taskList.append(task)
        #~ self.village.toDoList.append(task)

    def cleanTasks(self):
        inds = range(len(self.taskList))
        inds.reverse()
        for i in inds:
            if self.taskList[i].status == "done":
                #~ print self.toDoList[i].name, " finished"
                self.taskList.pop(i)
            elif self.taskList[i].status == "fail":
                if not self.taskList[i].mandatory:
                    self.taskList.pop(i)
                elif random.randint(0, 9) == 0:
                    t = self.taskList.pop(i)
                    t.status = "to start"
                    self.taskList.append(t)
                    #~ print "postponning task ",t.id

class LittleExternalPlace(LittlePlace):
    def __init__(self,name,  village):
        LittlePlace.__init__(self, village)
        self.type = "field"
        self.name = name

class LittleBuilding(LittlePlace):
    def __init__(self, name, village):
        LittlePlace.__init__(self, village)
        self.type = "defaultBuilding"
        self.name = name

        
        
class LittleStorage(LittleBuilding):
    def __init__(self, name, village):
        LittleBuilding.__init__(self, name, village)
        self.type = "storage"

#someone gets material from storage
    def getMaterial(self, mat, num, mandatory = True):
        if not mandatory and self.content[mat] - num < 1:
            print "NIET"
            result =  False
        else :
            result = LittlePlace.getMaterial(self, mat, num, mandatory)
        if not result and (mandatory or random.randint(0, 1) == 0):
            neighbors = self.village.getClosestBuilding( "warehouse", self.position, nb=1)
            for n in neighbors:
                self.village.addCarryTask( n, self, mat, mandatory=False)
                print "warehouse ",self.id," is asking ",mat," to warehouse ",n.id

        return result

#someone sets material to storage
    def setMaterial(self, mat, num):
        result = LittlePlace.setMaterial(self, mat, num)
        #~ print "test2"
        return result

class LittleHouse(LittleBuilding):
    def __init__(self, name, village):
        LittleBuilding.__init__(self, name, village)
        self.type = "house"

class LittleWorkshop(LittleBuilding):
    def __init__(self, name, village):
        LittleBuilding.__init__(self, name, village)
        self.type = "production"   
        
        self.production = ""
        self.productionTime = 0

    def startProducing(self):
        
        #~ self.production = prod
        #~ self.productionTime = int(utils.allWorkshops[self.name].time)
        
        for p in utils.allWorkshops[self.name].productions:
            task = LittleWorkTask(self, p, self.village)
            task.setData(self, p.needed, p.produced, int(p.time))
            self.addTask(task)
            
        
        

        #~ for i in range(0, num):
            #~ self.addProductionTask()
            
    #~ def addProductionTask(self):
        #~ task = LittleWorkTask(self, self.village)
        #~ self.addTask(task)
        #~ self.village.toDoList.append(task)
        #~ self.village.addProductionTask(self)
        
    def writeBuilding(self, elem):
        subelem = LittlePlace.writeBuilding(self,elem)
        #~ print "bla in writeworkshop"
        subelem.set("production", self.production)
        subelem.set("productionTime", str(self.productionTime))
        
    def readBuilding(self, elem):
        LittlePlace.readBuilding(self,elem)
        att = elem.attrib
        self.production = att["production"]
        self.productionTime = int(att["productionTime"])

        
        
def newBuilding(type, name, position, state, village):
    #~ print "new building"
    if type == "storage":
        b =  LittleStorage(name, village)
    elif type == "house":
        b =  LittleHouse(name, village)
    elif type == "field":
        b = LittleExternalPlace(name, village)
    elif type == "production":
        b =  LittleWorkshop(name, village)
    else:
        print "warning, ",type," not recognized as a place type"
        b = LittlePlace(village)
        
    b.state = state
    b.position = position
    global taskID
    b.id = taskID
    taskID += 1
    village.buildings.append(b)
    return b
    

if __name__ == '__main__':
    lb = LittleBuilding()
    print lb.name