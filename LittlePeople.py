import utils, random, copy

from LittleAction import *
from LittleBuilding import *

import xml.etree.ElementTree as ET


class LittlePeople:
    def __init__(self, root=None):
        self.action = None

        
        self.speed = 0.04
        
        if root is not None:
            self.read(root)
            return
            
        self.name = utils.randomName()
        
        self.pos = [0.0, 0.0]
        self.knowledge = {}
        self.knowledge["sleep"] = LittleBuildingList(type="sleep")
        self.knowledge["eat"] = LittleBuildingList(type="eat")
        
        self.habits = LittleOldActions(self)
        
        
        self.tired = -5*60
        self.hungry = 0


    def read(self, root):
        self.name = root.attrib["name"]
        self.pos = [float(root.attrib["posX"]), float(root.attrib["posY"])]
        self.tired = int(root.attrib["tired"])
        self.hungry = int(root.attrib["hungry"])
        for child in root:
            if (child.tag == "habits"):     
                self.habits = LittleOldActions(self, child)
            elif child.tag=="action":
                self.action = readAction(child, self)
            elif child.tag == "knowledge":
                self.knowledge = {}
                for cc in child:
                    self.knowledge[cc.attrib["type"]] = LittleBuildingList(cc)
                
                
    def write(self, root):
        elem =  ET.SubElement(root, 'people')
        elem.set("name", self.name)
        elem.set("posX", str(self.pos[0]))
        elem.set("posY", str(self.pos[1]))
        elem.set("tired", str(self.tired))
        elem.set("hungry", str(self.hungry))
        if self.action is not None:
            self.action.write(elem)
        
        self.habits.write(elem)
        
        sub =  ET.SubElement(elem, 'knowledge')
        for k in self.knowledge.values():
            k.write(sub)
            
   
    def update(self, time):
        self.tired+=1
        self.hungry +=1
        
        if self.action is not None:
            if not self.action.execute():
                self.habits.addAction(self.action)
                self.action = None
            return
        
        if self.tired > 20*60:
            #~ print "must sleep"
            self.action = LittleSleepAction( people=self,startHour=[time.hour, time.minute])
            return
        
        if self.hungry > 10*60:
            #~ print "must eat"
            self.action = LittleEatAction( people=self,startHour=[time.hour, time.minute]) 
            return
        
        myHabits = self.habits.findHabits([time.hour, time.minute])
        #~ myHabits = [LittleAction(self, "do nothing", [time.hour, time.minute])]
        
        r = random.randint(0, 9)
        if r < 9:
            a = random.choice(myHabits)
            
            if self.canDoAction(a):
                self.action = a.copy()
                return

        self.action = LittleAction(people=self, type="do nothing", startHour=[time.hour, time.minute])


    def canDoAction(self, a):
        if a.type == "sleep" and self.tired < 5*60:
            return False
        if a.type == "eat" and self.hungry < 3*60:
            return False
        return True
      
    def go(self, pos):
        #~ print self.name, " ", self.pos
        d = utils.distance(self.pos,pos)

        if d < self.speed:
            self.pos[0] = pos[0]
            self.pos[1] = pos[1]
            return True
        else:
            self.pos[0] += self.speed*(pos[0] - self.pos[0])/d
            self.pos[1] += self.speed*(pos[1] - self.pos[1])/d
            return False