#! /usr/bin/python
# -*- coding: utf-8 -*-

import random, utils

from LittlePeople import *
from LittleBuilding import *
from LittleDisplay import *

import xml.etree.ElementTree as ET
from xml.dom import minidom

if __name__ == '__main__':

    newVillage = False
 
    allPeople = []
    path = "village.xml"
    
    if newVillage:


        bb = LittleBuilding( pos=[0.,0.],type="dortoir")
        b = LittleBuilding( pos=[0.,0.],type="cantine")
        
        
        for i in range(0, 2):
            p = LittlePeople()
            p.knowledge["sleep"].seenBuilding(bb)
            p.knowledge["eat"].seenBuilding(b)
            print p.name

            allPeople.append(p)
  
    else:
        tree =  ET.parse(path)
        root = tree.getroot()
        for child in root:
            if (child.tag == "time"):
                utils.globalTime.read(child)
            elif (child.tag == "people"):
                p=LittlePeople(child)
                allPeople.append(p)
            elif child.tag == "building":
                b = LittleBuilding(child)

    #~ lv.readVillage(path)
    
      
    #~ t = LittleSleepTask([], [])

    
    DO_DISPLAY = True

    counter = 400
    
    while counter > 0:
        counter -= 1
        
        #~ print "------------------"
        utils.globalTime.addTime()
        #~ print utils.globalTime
        for p in allPeople:
            p.update(utils.globalTime)
        if DO_DISPLAY:
            if not display(allPeople, allBuildings):
                counter=0
            
    #~ print allPeople[0].habits
    
#~ lv.writeVillage(path)
    root = ET.Element('village')
    utils.globalTime.write(root)
    
    for p in allPeople:
        p.write(root)
        
    for b in allBuildings:
        print b.type
        b.write(root)
    
    
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    towrite = reparsed.toprettyxml(indent="  ")
    #print towrite
    file = open(path, "w")
    
    file.write(towrite)
    
    file.close()
    
    
    
    
    
    
    
            
    #~ def readVillage(self, path):
        #~ tree =  ET.parse(path)
        #~ root = tree.getroot()
        #~ mainAttrib = root.attrib
        #~ self.name = mainAttrib["name"]
        #~ for child in root:
            #~ if (child.tag == "villager"):
                #~ print "object ",child.attrib["name"], " added"
                #~ lv = LittleVillager(self)
                #~ lv.readVillager(child)
                #~ self.villagers.append(lv)
            #~ if (child.tag == "building"):
                #~ print "object ",child.attrib["name"], " added"
                #~ type = child.attrib["type"] 
                #~ name = ""
                 
                #~ if type == "storage":
                    #~ b =  LittleStorage(name, self)
                #~ elif type == "house":
                    #~ b =  LittleHouse(name, self)
                #~ elif type == "field":
                    #~ b = LittleExternalPlace(name, self)
                #~ elif type == "production":
                    #~ b =  LittleWorkshop(name, self)
                    
                #~ b.readBuilding(child)
                #~ self.buildings.append(b)
                    
            #~ if(child.tag == "task"):
                #~ type = child.attrib["type"] 
                #~ name = ""
                 
                #~ if type == "build":
                    #~ t =  LittleBuildTask( self, name)
                #~ elif type == "carry":
                    #~ t = LittleCarryTask( self)
                #~ elif type == "production":
                    #~ t = LittleWorkTask( None, self)
                    
                #~ t.readTask(child)
                #~ self.toDoList.append(t)
                    
                    
            #~ if child.tag == "askingBuilding":
                #~ self.askedBuildings[child.attrib["building"] ] = []
                #~ for subchild in child:
                    #~ if subchild.tag == "asking":
                        #~ self.askedBuildings[child.attrib["building"] ].append([int(subchild.attrib["askingX"]), int(subchild.attrib["askingY"]) ])
                    

                 

                
        #~ allTasks = copy.copy(self.toDoList)
        
        #~ for b in self.buildings:
            #~ for t in b.taskList:
                #~ allTasks.append(t)
                
        #~ for v in self.villagers:
            #~ tid = v.task
            #~ for t in allTasks:
                #~ try:
                    #~ if t.owner == v.name:
                        #~ t.owner = v

                #~ except:
                    #~ pass

                #~ if t.id == tid:
                    #~ v.task = t
                    #~ t.villager = v
            #~ if  isinstance(v.task, int):
                #~ v.busy = False
                #~ print "warning, ",v.name," did not find task ",tid
                
            #~ if v.home is not None:
                #~ for b in self.buildings:
                    #~ if b.id == v.home:
                        #~ v.home = b
                        #~ break
                
                
        #~ for t in allTasks:
            #~ if isinstance(t.owner, basestring):
                    #~ print "warning, owner ",t.owner," not found"
            
            #~ if isinstance(t.villager,basestring):
                #~ print "warning, task ",t.id, " has not his villager ",t.villager
            
            #~ if t.type == "build" and t.building is not None:
                #~ for b in self.buildings:
                    #~ if b.id == t.building:
                        #~ t.building = b
                        #~ break
                #~ if  isinstance(t.building, int):
                    #~ print "warning, ",t.name," did not find building ", t.building
            #~ elif t.type == "carry":
                #~ if isinstance(t.initial, int):
                    #~ for b in self.buildings:
                        #~ if t.initial == b.id:
                            #~ t.initial = b
                            #~ break
                    #~ if  isinstance(t.initial, int):
                        #~ print "warning, ",t.name," did not find initial building ", t.initial
                    
                #~ if isinstance(t.goal, int):
                    #~ for b in self.buildings:
                        #~ if t.goal == b.id:
                            #~ t.goal= b
                            #~ break
                    #~ if  isinstance(t.goal, int):
                        #~ print "warning, ",t.name," did not find goal building ", t.goal
                            
            #~ elif t.type == "production":
                #~ if t.workshop is not None:
                    #~ for b in self.buildings:
                        #~ if t.workshop == b.id:
                            #~ t.workshop = b
                            #~ break
                    #~ if  isinstance(t.workshop, int):
                        #~ print "warning, ",t.name," did not find workshop ", t.workshop
                 
                    
        
    #~ def writeVillage(self, path):
        #~ root = ET.Element('village')
        #~ root.set("name", self.name)
        #~ for v in self.villagers:
            #~ v.writeVillager(root)
        #~ for b in self.buildings:
            #~ b.writeBuilding(root)
            
        #~ print len(self.toDoList)," tasks in village"
        #~ for t in self.toDoList:
            #~ t.writeTask(root)
            
            
        #~ print "askedBuildings ", self.askedBuildings
            
        #~ for b in self.askedBuildings.keys():
            #~ ab = ET.SubElement(root, 'askingBuilding')
            #~ ab.set("building", str(b))
            #~ for p in self.askedBuildings[b]:
                #~ aabb =  ET.SubElement(ab, 'asking')
                #~ aabb.set("askingX", str(p[0]))
                #~ aabb.set("askingY", str(p[1]))
            
        #~ rough_string = ET.tostring(root, 'utf-8')
        #~ reparsed = minidom.parseString(rough_string)
        #~ towrite = reparsed.toprettyxml(indent="  ")
        #~ #print towrite
        #~ file = open(path, "w")
        
        #~ file.write(towrite)
        
        #~ file.close()