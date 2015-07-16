import utils, random, copy

from LittleAction import *
from LittleBuilding import *

import xml.etree.ElementTree as ET

allPeople = []

def peopleNamed(name):
    for p in allPeople:
        if p.name == name:
            return p
            
    return None

class LittlePeople:
    def __init__(self, root=None):
        self.action = None

        
        self.speed = 0.04
        
        if root is not None:
            self.read(root)
        else:
            
            self.name = utils.randomName()
            
            self.pos = [0.0, 0.0]
            self.knowledge = {}
            self.knowledge["sleep"] = LittleBuildingList(type="sleep")
            self.knowledge["eat"] = LittleBuildingList(type="eat")
            self.knowledge["work"] = LittleBuildingList(type="work")
            
            self.habits = LittleOldActions(self)
            
            self.shortTermGoal = ""
            
            
            self.tired = -5*60
            self.hungry = 0
            self.money=10
        
        global allPeople
        allPeople.append(self)


    def read(self, root):
        self.name = root.attrib["name"]
        self.pos = [float(root.attrib["posX"]), float(root.attrib["posY"])]
        self.tired = int(root.attrib["tired"])
        self.hungry = int(root.attrib["hungry"])
        self.money = float(root.attrib["money"])
        self.shortTermGoal = root.attrib["shorttermgoal"]
        
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
        elem.set("money", str(self.money))
        elem.set("shorttermgoal", self.shortTermGoal)
        if self.action is not None:
            self.action.write(elem)
        
        self.habits.write(elem)
        
        sub =  ET.SubElement(elem, 'knowledge')
        for k in self.knowledge.values():
            k.write(sub)
            
   
    def update(self):
        self.tired+=1
        self.hungry +=1
        
        if self.action is not None:
            if not self.action.execute():
                if self.action.type != "move" and self.action.type != "do nothing" :
                    if self.action.remainingTime <= 0:
                        #don't add if you could not eat...

                        print self.name," remember action #"+self.action.type+"# price ", self.action.price
                        self.habits.addAction(self.action)
                self.action = None
            return
            
            
            
        candiscuss = self.canDiscuss()
        for c in candiscuss:
            if random.randint(0, 9) == 0:
                self.tellInfo(c)
                
        possibleActions = []      
        preferredActions = []    
        b = buildingImIn(self.pos)
        if b is not None:
            aa = b.getPossibleActions()
            for a in aa:
                if self.canDoAction(a):
                    possibleActions.append(a)
                    if a.type == self.shortTermGoal:
                        preferredActions.append(a)
        self.shortTermGoal = ""
        if len(preferredActions) > 0:
            #~ print self.name, " want to ", preferredActions[0].type," here"
            
            self.startAction(random.choice(preferredActions).copy())
            return
        
        
        if self.tired > 20*60 and random.randint(0, 20) != 0:
            #~ print "must sleep"
            a =  LittleSleepAction( people=self,startHour=[utils.globalTime.hour, utils.globalTime.minute])
            self.moveToAction(a)
            return
        
        if self.hungry > 10*60 and random.randint(0, 20) != 0:
            #~ print "must eat"
            a = LittleEatAction( people=self,startHour=[utils.globalTime.hour, utils.globalTime.minute]) 
            self.moveToAction(a)
            return
        

        

        
        myHabits = self.habits.findHabits([utils.globalTime.hour, utils.globalTime.minute])
        #~ myHabits = [LittleAction(self, "do nothing", [time.hour, time.minute])]
        
        r = random.randint(0, 9)
        if r < 9:
            a = random.choice(myHabits)
            
            if self.canDoAction(a):
                possibleActions.append(a)
                #~ self.action = a.copy()
                #~ return
                
        #~ if random.randint(0, 1)==0:
        #~ dest = [0., 0.]
        #~ dest[0] = self.pos[0] + random.randint(-1, 1)
        #~ dest[1] = self.pos[1] + random.randint(-1, 1)
        a= LittleMoveAction(people=self,  startHour=[utils.globalTime.hour, utils.globalTime.minute])
        possibleActions.append(a)
            #~ return

        a = LittleAction(people=self, type="do nothing", startHour=[utils.globalTime.hour, utils.globalTime.minute])
        possibleActions.append(a)
        
        a = random.choice(possibleActions)
        #~ print "a.type ", a.type, " price ", a.price
        if a.type is not "move" and a.type is not "do nothing":
            self.moveToAction(a)
            return

        self.startAction(a)


    def moveToAction(self, a):
        self.shortTermGoal = a.type
        if not a.hasLocation():
            a.getLocation()
        a =  LittleMoveAction(people=self,  startHour=[utils.globalTime.hour, utils.globalTime.minute], pos=a.pos)
        #~ print self.name , " will go to ", a.pos, " for ", self.shortTermGoal
        self.startAction(a)

    def startAction(self, a):
        a.people = self
        if not a.hasLocation():
            a.getLocation()
        self.action = a
        #~ print self.name , " will ", a.type, " for ", a.price

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
            
    def tellInfo(self, p):
        knowledgeType = random.choice(self.knowledge.values())
        #~ print "tell info about ",knowledgeType.type
        b = knowledgeType.getLastSeen()
        
        if b is not None:
            bb = buildingImIn(b.pos)
            print self.name," : Hey, ",p.name, " tu connais ",bb.name, " ?"
            print self.name," : C'est un super ",knowledgeType.type, " en ",b.pos
            #~ print self.name," tells ",p.name, " about something for ",knowledgeType.type," named ", b.name," at ",b.pos
            p.knowledge[knowledgeType.type].seenBuilding(pos=b.pos)
            
    def canDiscuss(self):
        #~ print self.name, "can discuss ?"
        samepos = self.samePos()
        candiscuss = []
        for p in samepos:
            if p.action is None or p.action.type == "do nothing" or p.action.type == "eat":
                candiscuss.append(p)
                #~ print self.name, " can discuss with ",p.name
        return candiscuss
        
    def samePos(self):
        samepos = []
        for p in allPeople:
            if p.name == self.name:
                continue
            #~ print 
            if abs(self.pos[0] - p.pos[0]) < 1 and abs(self.pos[1] - p.pos[1])<1:
                samepos.append(p)
        return samepos