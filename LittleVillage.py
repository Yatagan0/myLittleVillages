import random, utils, copy

from LittleVillager import *
from LittleTask import *
from LittlePlace import *

import xml.etree.ElementTree as ET
from xml.dom import minidom


class LittleVillage:
    def __init__(self):
        self.toDoList = []
        self.villagers = []
        #~ self.places=[]
        self.buildings=[]
        #~ self.globalPosition = [0.,0.]
        self.name = "defaultVillageName"
        self.askedBuildings = {}
        self.askedBuildings['warehouse'] = []
        #~ self.carrying = ""
        
    def readVillage(self, path):
        tree =  ET.parse(path)
        root = tree.getroot()
        mainAttrib = root.attrib
        self.name = mainAttrib["name"]
        for child in root:
            if (child.tag == "villager"):
                #~ print "object ",child.attrib["name"], " added"
                lv = LittleVillager(self)
                lv.readVillager(child)
                self.villagers.append(lv)
            if (child.tag == "building"):
                #~ print "object ",child.attrib["name"], " added"
                type = child.attrib["type"] 
                name = ""
                 
                if type == "storage":
                    b =  LittleStorage(name, self)
                elif type == "house":
                    b =  LittleHouse(name, self)
                elif type == "field":
                    b = LittleExternalPlace(name, self)
                elif type == "production":
                    b =  LittleWorkshop(name, self)
                    
                b.readBuilding(child)
                self.buildings.append(b)
                    
            if(child.tag == "task"):
                type = child.attrib["type"] 
                name = ""
                 
                if type == "build":
                    t =  LittleBuildTask( self, name)
                elif type == "carry":
                    t = LittleCarryTask( self)
                elif type == "production":
                    t = LittleWorkTask( None, self)
                    
                t.readTask(child)
                self.toDoList.append(t)
                    
                    
            if child.tag == "askingBuilding":
                self.askedBuildings[child.attrib["building"] ] = []
                for subchild in child:
                    if subchild.tag == "asking":
                        self.askedBuildings[child.attrib["building"] ].append([int(subchild.attrib["askingX"]), int(subchild.attrib["askingY"]) ])
                    

                 

                
        allTasks = copy.copy(self.toDoList)
        
        for b in self.buildings:
            for t in b.taskList:
                allTasks.append(t)
                
        for v in self.villagers:
            #~ v.busy = False
            tid = v.task
            for t in allTasks:
                #~ print t.id
                try:
                    if t.owner == v.name:
                        t.owner = v

                except:
                    pass

                if t.id == tid:
                    v.task = t
                    t.villager = v
                    #~ break
            if  isinstance(v.task, int):
                v.busy = False
                print "warning, ",v.name," did not find task ",tid
                
            if v.home is not None:
                for b in self.buildings:
                    if b.id == v.home:
                        v.home = b
                        break
                
                
        for t in allTasks:
            if isinstance(t.owner, basestring):
                    print "warning, owner ",t.owner," not found"
            
            if isinstance(t.villager,basestring):
                print "warning, task ",t.id, " has not his villager ",t.villager
            
            if t.type == "build" and t.building is not None:
                #~ print "task ",t.id
                for b in self.buildings:
                    if b.id == t.building:
                        t.building = b
                        #~ print "has a building"
                        break
                if  isinstance(t.building, int):
                    print "warning, ",t.name," did not find building ", t.building
            elif t.type == "carry":
                #~ print "task ",t.id
                if isinstance(t.initial, int):
                    for b in self.buildings:
                        if t.initial == b.id:
                            t.initial = b
                            #~ print "has a initial"
                            break
                    if  isinstance(t.initial, int):
                        print "warning, ",t.name," did not find initial building ", t.initial
                    
                if isinstance(t.goal, int):
                    for b in self.buildings:
                        if t.goal == b.id:
                            t.goal= b
                            #~ print "has a goal"
                            break
                    if  isinstance(t.goal, int):
                        print "warning, ",t.name," did not find goal building ", t.goal
                            
            elif t.type == "production":
                if t.workshop is not None:
                    #~ print "task ",t.id
                    for b in self.buildings:
                        if t.workshop == b.id:
                            t.workshop = b
                            #~ print "has a workshop"
                            break
                    if  isinstance(t.workshop, int):
                        print "warning, ",t.name," did not find workshop ", t.workshop
                 
                    
        
    def writeVillage(self, path):
        root = ET.Element('village')
        root.set("name", self.name)
        for v in self.villagers:
            v.writeVillager(root)
        for b in self.buildings:
            b.writeBuilding(root)
            
        print len(self.toDoList)," tasks in village"
        for t in self.toDoList:
            t.writeTask(root)
            
            
        print "askedBuildings ", self.askedBuildings
            
        for b in self.askedBuildings.keys():
            ab = ET.SubElement(root, 'askingBuilding')
            ab.set("building", str(b))
            for p in self.askedBuildings[b]:
                aabb =  ET.SubElement(ab, 'asking')
                aabb.set("askingX", str(p[0]))
                aabb.set("askingY", str(p[1]))
            
        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        towrite = reparsed.toprettyxml(indent="  ")
        #print towrite
        file = open(path, "w")
        
        file.write(towrite)
        
        file.close()
        
    def createRandomVillage(self, num):
        startName = utils.allU 
        middleName = utils.allL 
        endName = ["touille", "mont", "vert", "gny", "leaux", "rrand", "lieu", "guen"]
        self.name= startName[random.randint(0, len(startName)-1)]+middleName[random.randint(0, len(middleName)-1)]+endName[random.randint(0, len(endName)-1)]

        for i in range(num):
            lv = LittleVillager(self)
            lv.generate()
            self.villagers.append(lv)
            
        newBuilding("storage", "warehouse", [0, 0], "ok", self)
        self.buildings[0].setMaterial("stone", 0)
        self.buildings[0].setMaterial("wood", 10)
        newBuilding("storage", "warehouse", [1, 1], "ok", self)
        self.buildings[1].setMaterial("stone", 10)
        self.buildings[1].setMaterial("wood", 0)
        newBuilding("production", "woodcutter", [0, -1], "ok", self)
        self.buildings[2].startProducing("wood", 3, 1)
        newBuilding("production", "stonecutter", [1, 2], "ok", self)
        self.buildings[3].startProducing("stone", 3, 1)
        
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
        lwt = LittleWorkTask(workshop, workshop.village)
        workshop.addTask(lwt)
        #self.toDoList.append(lwt)
        
    def addCarryTask(self, fromB,toB, mat, mandatory = True):
        if fromB.id == toB.id:
            return
        lct = LittleCarryTask(self, fromB, toB, mat)
        lct.mandatory = mandatory
        #~ self.toDoList.append(lct)
        fromB.taskList.append(lct)

    def addNewBuilding(self, type, name, position, state):
        return newBuilding(type, name, position, state, self)


    def getClosestBuilding(self, buildingName, destination, villagerpos = None, nb=1):
        listToSort = []
        for b in self.buildings:
            if b.name == buildingName and b.state=="ok":
                if villagerpos is not None:
                    listToSort.append([b, 1*utils.distance(villagerpos, b.position) + 1*utils.distance(destination, b.position) ])
                else:
                    listToSort.append([b, utils.distance(destination, b.position) ])

        sortedList = sorted(listToSort,  key=lambda tup: tup[1])
        #~ print "closest ",sortedList[0][1]
        if sortedList[0][1] == 0:
            sortedList = sortedList[1:] #dont find yourself
            print "don't find yourself"
        result = []
        for i in range(min(nb, len(sortedList))):
            result.append(sortedList[i][0])
        
        return result
        
    def getClosestBuilding2(self, position):
        nb = 30
        listToSort = []
        for b in self.buildings:
            listToSort.append([b, utils.distance(position, b.position) ])

        sortedList = sorted(listToSort,  key=lambda tup: tup[1])
        result = []
        for i in range(min(nb, len(sortedList))):
            result.append(sortedList[i][0])
        
        return result
        
    def getClosestTasks(self, position, dist = 1.5, nb=10):
        blist = self.getClosestBuilding2(position)
        tlist = []
        #~ tlist = copy.copy(self.toDoList)
        for t in self.toDoList:
            if t.canPerform():
                tlist.append(t)
        
        for b in blist:
            for t in b.taskList:
                if t.canPerform():
                    tlist.append(t)
        
        return tlist #+self.toDoList
        
    def cleanTasks(self):
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
                    
                    
    def seeAskedBuildings(self):
        if random.randint(0, 99) > 0:
            return
        building = random.choice(self.askedBuildings.keys())
        print "looking for a new building ", building
        
        mean = utils.getMeanPos(self.askedBuildings[building])
        #~ print mean
        mean = map(int, mean)
        print mean
        
        close = []
        far = []
        for p in self.askedBuildings[building]:
            if p[0] > mean[0] -3 and p[0] < mean[0] + 3 and p[1] > mean[1] -3 and p[1] < mean[1] + 3:
                close.append(p)
            else:
                far.append(p)
        print len(close), " close askers"
        if len(close) > 100:
            print "village decided to print a new ",utils.workshopName[building]," at position ", mean
            self.askedBuildings[building] = far
            lbt = LittleBuildTask(self, utils.workshopName[building], mean)
            self.toDoList.append(lbt)
            
        #TODO:
        #remove too far askers and redo mean
        #check that the same building is not already present close
        # warehouse
        
        
    def iterate(self):
        print "--------------------"
        
        self.seeAskedBuildings()
        
        for p in self.villagers:
            #~ print p.position
            p.execute()
            #~ print p.position
            #~ print "&&&&"

        for b in self.buildings:
            b.cleanTasks()
                
        self.cleanTasks()

                    
            

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
