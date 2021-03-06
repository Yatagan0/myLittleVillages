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
        self.shortTermGoal = ""
        self.ownedBuildings = []
        self.objects = []
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
        if "shorttermgoal" in root.attrib.keys():
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
            elif child.tag=="ownedBuilding":
                self.ownedBuildings.append([float(child.attrib["posX"]), float(child.attrib["posY"])])
            elif child.tag == "object":
                self.objects.append(child.attrib["name"])                     
                
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
        
        for b in self.ownedBuildings:
            sub =  ET.SubElement(elem, 'ownedBuilding')
            sub.set("posX", str(b[0]))
            sub.set("posY", str(b[1]))
  
            
        for o in self.objects:
            sub =  ET.SubElement(elem, 'object')
            sub.set("name", o)
            
            
    def hourlyUpdate(self):
        pass
            
    def dailyUpdate(self):
        pass
   
    def update(self):
        self.tired+=1
        self.hungry +=1
        
        
        
        if self.action is not None:
            if not self.action.execute():
                #~ print self.name," action finished"
                if self.action.type != "move" and self.action.type != "do nothing" :
                    if self.action.remainingTime <= 0:
                        #don't add if you could not eat...

                        #~ print self.name," remember action #"+self.action.type+"# price ", self.action.price
                        self.habits.addAction(self.action)
                self.action = None
            return

        candiscuss = self.canDiscuss()
        for c in candiscuss:
            if random.randint(0, 9) == 0:
                self.tellInfo(c)

        #~ print "a"
        
        b = buildingImIn(self.pos)
        if self.shortTermGoal != "":
            #~ print self.name, " has short term goal ", self.shortTermGoal
            a = self.canDoActionHere( b, self.shortTermGoal)
            if a is not None:
                #~ print self.name," can do short term goal ",self.shortTermGoal
                self.startAction(a)
                self.shortTermGoal = ""
                return
             
        goalPos = None
        if self.shortTermGoal in self.knowledge.keys():
            goalPos = self.knowledge[self.shortTermGoal].findClosest(self.pos, notHere=self.pos)

        if goalPos is not None:
            #~ print self.name," will go in ", goalPos, " for short term goal ",self.shortTermGoal
            a= LittleMoveAction()
            a.pos = goalPos
            self.startAction(a)
            return
                
        if self.tired > 20*60 and random.randint(0, 10) != 0:
                a =  LittleSleepAction()
                self.moveToAction(a)
                if self.action is not None:
                    return
        
        if self.hungry > 10*60 and random.randint(0, 10) != 0:
                a = LittleEatAction( )
                self.moveToAction(a)
                if self.action is not None:
                    return
            
        #~ if self.money < 5.0 and random.randint(0, 10) != 0:
            #~ a = LittleWorkAction( )
            #~ self.moveToAction(a)
            #~ return
                
        actionChoice = random.choice(["habits", "discover", "commerce"])
        #~ print actionChoice
        possibleActions = []      
        
        
        if b is not None:
            if actionChoice == "discover":
                buildingIsMine = False
                for mb in self.ownedBuildings:
                    if b.pos[0] == mb[0] and b.pos[1] == mb[1]:
                        buildingIsMine = True
                        break
                
                aa = b.getPossibleActions(isOwner=buildingIsMine)
                for a in aa:
                    if self.canDoAction(a):
                        possibleActions.append(a)
                        
            if actionChoice == "commerce":       
                for o in self.objects:
                    if o in b.wantToBuy.keys():
                        print self.name, " can sell ",o
                        possibleActions.append(LittleSellAction(workslot=b.workSlots[0], object=o))
                        #~ self.moveToAction(LittleSellAction(workslot=b.workSlots[0], object=o))
                        #~ return

        if actionChoice == "habits": 
            myHabits = self.habits.findHabits([utils.globalTime.hour, utils.globalTime.minute])
            #~ print len(myHabits)," habit "
            for a in myHabits:
                if self.canDoAction(a):
                    possibleActions.append(a)  
                    #~ print "possible habit"
                        
        if actionChoice == "discover":
            a= LittleMoveAction()
            possibleActions.append(a)
        
        for mb in self.ownedBuildings:
            if mb[0] != self.pos[0] or mb[1] != self.pos[1]:
                a= LittleMoveAction()
                a.pos = mb
                possibleActions.append(a)           

        a = LittleAction()
        possibleActions.append(a)
        

        
        #~ print "chosing between ", len(possibleActions), " actions"
        a = random.choice(possibleActions)
        #~ print "a.type ", a.type, " price ", a.price
        #~ if a.pos is None or ( a.type is not "move" and a.type is not "do nothing"):
        self.moveToAction(a)
        #~ print "d"
            #~ return

        #~ self.startAction(a)


    def canDoActionHere(self, building,  action):
        #~ print "searching for acton of type ",action
        preferredActions = []
        if building is not None:
            buildingIsMine = False
            for mb in self.ownedBuildings:
                if building.pos[0] == mb[0] and building.pos[1] == mb[1]:
                    buildingIsMine = True
                    break
            
            preferredActions = building.getPossibleActions(isOwner=buildingIsMine, actionTypes=[action])
            #~ print len(preferredActions)," possible actions in building"
            #~ for a in aa:
                #~ print "can do ",a.type,"?"
                #~ if self.canDoAction(a):
                    #~ print a.type
                    #~ if action=="work" and a.type not in specialWorks:
                        #~ preferredActions.append(a)
                    #~ if a.type == action:
                         #~ preferredActions.append(a)

        if len(preferredActions) > 0:
            return random.choice(preferredActions).copy()
            
        return None

    def moveToAction(self, a):
        if a.type == "sell" or a.type=="buy":
            a.getLocation(self)
            self.startAction(a)
            return
        
        b = buildingImIn(self.pos)
        aa = self.canDoActionHere( b, a.type)
        if aa is not None:
            #~ print self.name," can ",a.type," here"
            self.startAction(aa)
            return
        
        #~ if not a.hasLocation():
        a.getLocation(self)
            
        if a.type != "move" and a.type != "do nothing" :
            if a.pos is None:
                #~ print "couldn't find where to ",a.type
                self.shortTermGoal = ""

                return

            #~ if a.pos[0] != self.pos[0] or a.pos[1] != self.pos[1]:
            #~ if a.workslot is None:
            self.shortTermGoal = a.type
            #~ print self.name," new short term goal ",self.shortTermGoal
            a =  LittleMoveAction( pos=a.pos)
        #~ print self.name , " will go to ", a.pos, " for ", self.shortTermGoal
        self.startAction(a)

    def startAction(self, a):
        #~ a.people = self
        #~ if not a.hasLocation():
            #~ a.getLocation(self)
        #~ if a.type== "buy":
            #~ print "startActionn ",a.workslot," ",a.pos
        a.people = self
        if a.canExecute():
            a.startExecution(self)
        #~ print "startActionn ",a.workslot
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
            #~ print self.name," : Hey, ",p.name, " tu connais ",bb.name, " ?"
            #~ print self.name," : C'est un super ",knowledgeType.type, " en ",b.pos
            #~ print self.name," tells ",p.name, " about something for ",knowledgeType.type," named ", b.name," at ",b.pos
            p.knowledge[knowledgeType.type].seenBuilding(pos=b.pos)
            
    def canDiscuss(self):
        #~ print self.name, "can discuss ?"
        samepos = self.samePos()
        candiscuss = []
        for p in samepos:
            if p.action is None or p.action.type != "sleep":
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