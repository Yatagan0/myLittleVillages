import random, utils

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
        #~ self.carrying = ""
        
    def readVillage(self, path):
        tree =  ET.parse(path)
        root = tree.getroot()
        mainAttrib = root.attrib
        self.name = mainAttrib["name"]
        for child in root:
            if (child.tag == "villager"):
                #~ print "object ",child.attrib["name"], " added"
                lv = LittleVillager()
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
                    
            if(child.tag == "task"):
                type = child.attrib["type"] 
                name = ""
                 
                if type == "build":
                    t =  LittleBuildTask(name, self)
                elif type == "carry":
                    t = LittleCarryTask(name, self)
                elif type == "production":
                    t = LittleWorkTask(name, self)

                 
                 
                t.readTask(child)
                self.toDoList.append(t)
                
        for v in self.villagers:
            v.busy = False
            #~ tid = v.task
            #~ for t in self.toDoList:
                #~ if t.id == tid:
                    #~ v.task = t
                    #~ break
        
    def writeVillage(self, path):
        root = ET.Element('village')
        root.set("name", self.name)
        for v in self.villagers:
            v.writeVillager(root)
        for b in self.buildings:
            b.writeBuilding(root)
            
        for t in self.toDoList:
            t.writeTask(root)
            
        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        towrite = reparsed.toprettyxml(indent="  ")
        #print towrite
        file = open(path, "w")
        
        file.write(towrite)
        
        file.close()
        
    def createRandomVillage(self, num):
        #~ startName = utils.allU 
        #~ middleName = utils.allL 
        #~ endName = ["touille", "mont", "vert", "gny", "leaux", "rrand", "lieu", "guen"]
        #~ self.name= startName[random.randint(0, len(startName)-1)]+middleName[random.randint(0, len(middleName)-1)]+endName[random.randint(0, len(endName)-1)]

        #~ for i in range(num):
            #~ lv = LittleVillager()
            #~ lv.generate()
            #~ self.villagers.append(lv)
            
        #~ newBuilding("storage", "warehouse", [0, -2], "ok", self)
        #~ self.buildings[0].setMaterial("stone", 40)
        #~ self.buildings[0].setMaterial("wood", 10)
        #~ newBuilding("production", "woodcutter", [0, 4], "ok", self)
        #~ self.buildings[1].startProducing("wood", 3, 1)
        #~ newBuilding("storage", "warehouse", [0, 3], "ok", self)
        pass
        
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
