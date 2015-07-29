import utils, random
import xml.etree.ElementTree as ET

#~ from LittleNewAction import *
from LittleRecipe import *

class LittleAction:
    
    def __init__(self, root=None, workslot = None, type="do nothing", price=0.):
        self.workslot = workslot
        self.type = type
        self.price = price
        self.people = None
        self.pos = None
        self.startHour = None#[0., 0.]
        self.remainingTime = 1
        if root is not None:
            self.read(root)
        else:
            if self.workslot is not None:
                self.pos = self.workslot.building.pos
            
        if self.type not in allRecipes.keys():
            print "unknown recipe"
    

        
    def __str__(self):
        s = self.type+" starting "+str(self.startHour[0])+":"+str(self.startHour[1])+"\n"
        return s
 
 
    def read(self, root):
        self.type = root.attrib["type"]
        if "startHour" in root.attrib.keys():
            self.startHour = [int(root.attrib["startHour"]),int(root.attrib["startMinute"]) ]
        self.remainingTime = int(root.attrib["remainingTime"])
        self.price = float(root.attrib["price"])
        
        if "posX" in root.attrib.keys():
            self.pos = [float(root.attrib["posX"]),float(root.attrib["posY"]) ]

        if "workslotName" in root.attrib.keys():
            self.workslot = root.attrib["workslotName"]
            if self.pos is not None:
                from LittleBuilding import findWorkslot
                WS = findWorkslot( self.pos, self.workslot)
                if WS is not None:
                    self.workslot = WS

        
    def write(self, root):
        elem =  ET.SubElement(root, 'action')
        elem.set("class", "LittleAction")
        elem.set("type", self.type)
        if self.startHour is not None:
            elem.set("startHour", str(self.startHour[0]))
            elem.set("startMinute", str(self.startHour[1]))
        elem.set("remainingTime", str(self.remainingTime))
        elem.set("price", str(self.price))
        if self.workslot is not None:
            if isinstance(self.workslot, basestring) :
                elem.set("workslotName", self.workslot)
            else:
                elem.set("workslotName", self.workslot.name)
        if self.pos is not None:
            #~ elem.set("posX", str(self.workslot.building.pos[0]))
            #~ elem.set("posY", str(self.workslot.building.pos[1]))
            elem.set("posX", str(self.pos[0]))
            elem.set("posY", str(self.pos[1]))
        return elem

    def canExecute(self):
        if self.type not in allRecipes.keys():
            print "unknown recipe"
        #TO DO
        return True
       
    def startExecution(self, people):
        self.people = people
        t = utils.globalTime
        self.startHour = [t.hour, t.minute]
        
        print "starting ", self.workslot, " at ", self.pos

        if self.type not in allRecipes.keys():
            self.remainingTime = 60
            print people.name, " fait un truc"
            
        else:
            self.remainingTime = random.randint(allRecipes[self.type].timeMin, allRecipes[self.type].timeMax)
            if allRecipes[self.type].description != "":
                print people.name, " ", allRecipes[self.type].description, " pendant ",self.remainingTime 
        
     
    def endExecution(self):
        if isinstance(self.workslot, basestring) :
            print "workslot name ",self.workslot, " pos ",self.pos
            if self.pos is not None:
            
                from LittleBuilding import findWorkslot
                self.workslot = findWorkslot( self.pos, self.workslot)
            
        print "ending ", self.workslot, " at ", self.pos
        if self.workslot is not None:
            self.people.money -= self.price
            self.workslot.building.money += self.price
            #~ print "has workslot"
            #~ self.workslot.objectStatus("bed", "clean", "dirty")
       
    def execute(self):
        self.remainingTime -= 1
        if self.remainingTime <= 0:
            
            self.endExecution()
            return False
            
        return True
        
    def copy(self):
        #~ print "copy"
        root = ET.Element('village')
        act = self.write(root)
        a = readAction(root=act, people=None)
        return a
        
    def hasLocation(self):
        return self.pos != None
        
    def getLocation(self, people):
        if self.pos is None:
            self.pos = [people.pos[0], people.pos[1]]
        if isinstance(self.workslot, basestring):
            from LittleBuilding import findWorkslot
            self.workslot = findWorkslot( self.pos, self.workslot)
            
class LittleMoveAction(LittleAction):
    def __init__(self,root=None,pos=None):
        LittleAction.__init__(self, root=root, type="move")
        if root is not None:
            #~ self.read(root)
            pass
        else:
            self.pos = pos
            
    #~ def read(self, root):
        #~ LittleAction.read(self,root)
        #~ self.pos = [float(root.attrib["posX"]),float(root.attrib["posY"]) ]
        
        
    def write(self, root):
        elem =  LittleAction.write(self, root)
        elem.set("class", "LittleMoveAction")
        return elem

    def canExecute(self):
        print "can execute move"
        return True
        
     
    def startExecution(self, people):
        LittleAction.startExecution(self, people)
        print self.people.name," va de ",self.people.pos," vers ", self.pos

    def execute(self):
        #~ print self.pos
        #~ print self.people
        if self.people.go(self.pos):
            self.endExecution()
            return False
            
        return True

    def getLocation(self, people):
        if self.pos is None:
            self.pos = [people.pos[0]+random.randint(-1, 1), people.pos[1]+random.randint(-1, 1)]
            #~ print "self pos ",self.pos

        
class LittleSleepAction(LittleAction):
    def __init__(self,root=None,workslot=None):
        LittleAction.__init__(self, root=root, type="sleep", workslot=workslot)
    #~ def __init__(self,root=None,people=None, startHour=None,pos=None, price=0.,workslot=None):
        #~ LittleAction.__init__(self, root,people,"sleep", startHour, pos, price, workslot)
        #~ if root is not None:
            #~ self.read(root)
        #~ else:
            #~ self.init()
        
    #~ def init(self):
        #~ self.status = "not started"
        #~ self.remainingTime = 7*60 +random.randint(0, 60)
        #~ self.pos = [0., 0.]
        
    #~ def read(self, root):
        #~ LittleAction.read(self,root)
        #~ self.pos = [float(root.attrib["posX"]),float(root.attrib["posY"]) ]
        #~ if self.pos is not None:
            
            #~ from LittleBuilding import buildingImIn
            #~ self.building = buildingImIn(self.pos)
    
    def write(self, root):
        elem =  LittleAction.write(self, root)
        #~ elem.set("posX", str(self.pos[0]))
        #~ elem.set("posY", str(self.pos[1]))
        elem.set("class", "LittleSleepAction")
        return elem

        
    #~ def copy(self):
        #~ a = LittleSleepAction(people=self.people, startHour=self.startHour, pos=self.pos, price=self.price)
        #~ return a
    def endExecution(self):
        LittleAction.endExecution(self)
        self.people.tired = 0
        self.people.knowledge["sleep"].seenBuilding(pos=self.pos, reliable=1)
            
    #~ def execute(self):
        
        #~ if self.building is None:
            #~ from LittleBuilding import buildingImIn
            #~ self.building = buildingImIn(self.pos)
            #~ self.people.tired = 0
            #~ self.people.knowledge["sleep"].seenBuilding(pos=self.pos, reliable=1)
        
        #~ if self.status == "not started":
            #~ t = utils.globalTime
            #~ self.startHour = [t.hour, t.minute]
            #~ print self.workslot
            #~ if self.workslot is not None and self.workslot.hasObject("bed", "clean"):
                #~ print "has clean bed"
           
        #~ self.status = "executing"
        #~ if self.people.go(self.pos):
            #~ self.remainingTime -= 1
            #~ if self.remainingTime > 0:
                #~ return True
                
            #~ else:
                #~ self.people.money -= self.price
                #~ self.building.money += self.price
                #~ self.building.beds +=1
                #~ self.people.tired = 0
                #~ self.people.knowledge["sleep"].seenBuilding(pos=self.pos, reliable=1)
                #~ return False
                
        #~ return True
        
    def getLocation(self, people):
        if self.pos is None:
            self.pos = people.knowledge["sleep"].findClosest(people.pos)
        #~ from LittleBuilding import buildingImIn
        #~ self.buidling = buildingImIn(self.pos)
        
class LittleEatAction(LittleAction):
    def __init__(self,root=None, people=None, startHour=None,pos=None, price=0.,workslot=None):
        LittleAction.__init__(self,root, people, "eat", startHour,pos, price, workslot)
        if root is not None:
            self.read(root)
        else:
            self.init()
        
    def init(self):
        self.status = "not started"
        self.remainingTime = 45 +random.randint(0, 15)
        #~ self.pos = [0., 0.]

    def read(self, root):
        LittleAction.read(self,root)
        #~ self.pos = [float(root.attrib["posX"]),float(root.attrib["posY"]) ]
        #~ if self.pos is not None:
            #~ print "eat ", self.pos
            #~ from LittleBuilding import buildingImIn
            #~ self.building = buildingImIn(self.pos)
            #~ print self.building
            
    def write(self, root):
        elem =  LittleAction.write(self, root)
        #~ elem.set("posX", str(self.pos[0]))
        #~ elem.set("posY", str(self.pos[1]))
        elem.set("class", "LittleEatAction")
        
    def copy(self):
        a = LittleEatAction(people=self.people, startHour=self.startHour, pos=self.pos, price=self.price)
        return a
        
    def execute(self):
        
        if self.building is None:
                from LittleBuilding import buildingImIn
                self.building = buildingImIn(self.pos)

        if self.status == "not started":
            t = utils.globalTime
            self.startHour = [t.hour, t.minute]
            if self.building.meals > 0 and self.building.cleanCouverts > 0:
                print self.people.name, " va manger a ",self.building.name
                self.building.meals -=1
                self.building.couverts -=1
                self.building.cleanCouverts -=1
            else:
                print self.people.name, " ne peux pas manger a ",self.building.name
                self.people.knowledge["eat"].seenBuilding(pos=self.pos, reliable=0)
                return False
                
            #~ print self.people.name, " va manger a ",self.pos
        self.status = "executing"
        if self.people.go(self.pos):
            self.remainingTime -= 1
            if self.remainingTime > 0:
                return True
                
            else:
                self.people.hungry = 0
                self.building.couverts +=1
                self.people.money -= self.price
                self.building.money += self.price

                #~ print "now ",self.building.meals, " meals at ", self.building.name
                #~ print "now ",self.building.cleanCouverts, " clean couverts at ", self.building.name
                self.people.knowledge["eat"].seenBuilding(pos=self.pos, reliable=1)
                return False
                
        return True
        
    def getLocation(self):
        if self.pos is None:
            self.pos = self.people.knowledge["eat"].findClosest(self.people.pos)
        from LittleBuilding import buildingImIn
        self.building = buildingImIn(self.pos)
        #~ print "get location ",self.pos
        #~ print "get location ",self.building.name

class LittleWorkAction(LittleAction):
    def __init__(self,root=None,people=None, startHour=None,pos=None, desc="", type="work", price=0., workslot=None):
        LittleAction.__init__(self, root,people,type, startHour, pos, price, workslot)
        if root is not None:
            self.read(root)
        else:
            self.description = desc
            self.init()
            
        #~ print self.description, " ", self.type
        
    def init(self):
        self.status = "not started"
        self.remainingTime = 45 +random.randint(0, 15)
            
    def read(self, root):
        LittleAction.read(self,root)
        self.description = root.attrib["description"]
        
        
    def write(self, root):
        elem =  LittleAction.write(self, root)
        elem.set("class", "LittleWorkAction")
        elem.set("description", self.description)

        
    def copy(self):
        a = LittleWorkAction(people=self.people, startHour=self.startHour, pos=self.pos, desc=self.description, type=self.type, price=self.price)
        return a      

    def execute(self):
        
        if self.building is None:
            from LittleBuilding import buildingImIn
            self.building = buildingImIn(self.pos)
        
        if self.status == "not started":
            t = utils.globalTime
            self.startHour = [t.hour, t.minute]
            
            if self.type=="cook":
                self.remainingTime = 20 + random.randint(0, 20)
            elif self.type=="dishes":
                self.remainingTime = 10 + random.randint(0, 10)
            elif self.type=="cleanbed":
                self.remainingTime = 10 + random.randint(0, 10)
            elif self.type=="construct":
                self.remainingTime = 60 + random.randint(0, 60)
                self.building.numWorkers -=1
                
            if self.description == "":
                print self.people.name, " travaille a ",self.building.name
            else:
                print self.people.name, " ", self.description, " ",self.building.name

        self.status = "executing"
        if self.people.go(self.pos):
            self.remainingTime -= 1
            if self.remainingTime > 0:
                return True
                
            else:
                #~ print "fini !"
                #~ print "finin ",self.description, " ", self.type
                self.people.money -= self.price
                self.building.money += self.price
                
                
                if self.type=="cook":
                    self.building.meals +=1
                    #~ print "now ",self.building.meals, " meals at ", self.building.name
                elif self.type=="dishes":
                    self.building.cleanCouverts +=1
                    #~ print "now ",self.building.cleanCouverts, " clean couverts at ", self.building.name
                elif self.type=="cleanbed":
                    self.building.cleanBeds +=1
                    #~ print "now ",self.building.cleanBeds, " clean beds at ", self.building.name
                elif self.type=="construct":
                    self.building.numWorkers +=1
                    self.building.workTasks -=1
                    if self.building.workTasks == 0:
                        self.building.finish()
            
                self.people.knowledge["work"].seenBuilding(pos=self.pos,reliable=1)
                return False
                
        return True

    def getLocation(self):
        if self.pos is None:
            self.pos = self.people.knowledge["work"].findClosest(self.people.pos)
        from LittleBuilding import buildingImIn
        self.building = buildingImIn(self.pos)
        
class LittleOldActions():
    def __init__(self,people, root=None):
        self.days = []
        if root is not None:
            
            self.read(root, people)
            return
            
        for i in range(0,9):
            day = []
            #~ day.append(LittleEatAction( people=people,startHour=[7, 0]))
            #~ day.append(LittleEatAction(people=people,startHour= [12, 0]))
            #~ day.append(LittleEatAction( people=people,startHour=[20, 0]))
            #~ a = LittleNewAction( type="eat")
            #~ a.startHour = [7, 0]
            #~ day.append(a)
            #~ a = LittleNewAction( type="eat")
            #~ a.startHour = [12, 0]
            #~ day.append(a)
            #~ a = LittleNewAction( type="eat")
            #~ a.startHour = [20, 0]
            #~ day.append(a)
            #~ a = LittleNewAction( type="sleep")
            #~ a.startHour = [21, 0]
            #~ day.append(a)
            
            a = LittleAction( )
            a.startHour = [21, 0]
            day.append(a)
            self.days.append(day)
                
    def __str__(self):
        s = ""
        for d in self.days:
            s+="day : \n"
            for a in d:
                s+=" "+str(a)
        return s
    
    def read(self, root, people):
        for child in root:
            day = []
            for cc in child:
                day.append(readAction(cc, people))
            self.days.append(day)
    
    def write(self, root):
        elem =  ET.SubElement(root, 'habits')
        for d in self.days:
            subelem = ET.SubElement(elem, 'day')
            for a in d:
                a.write(subelem)
    
    def findHabits(self, time):
        habits = []
        for d in self.days[:-1]: #not today
            habits.append(self.closestAction(d, time))
            
        return habits
            
    def closestAction(self, day, time):
        #TODO prendre en compte le changement de jour
        index = 0
        diff = 24*60
        
        for a in day:
            adiff = abs((a.startHour[0] - time[0])*60 + (a.startHour[1] - time[1]))
            if adiff < diff:
                diff = adiff
                index +=1
            else:
                break
        #~ print diff
        #~ print index
        return day[index-1]
        
    def addAction(self, a):
        #~ a.init()
        #~ t = utils.globalTime
        #~ a.startHour = [t.hour, t.minute]
        lasta = self.days[-1][-1]
        diff = (a.startHour[0] - lasta.startHour[0])*60 + (a.startHour[1] - lasta.startHour[1])
        if diff < 0:
            #~ print a.startHour
            #~ print lasta.startHour
            
            #~ print utils.globalTime, "new day"
            self.days = self.days[1:]
            self.days.append([])
        self.days[-1].append(a)

def readAction(root, people):
    if root.attrib["class"] == "LittleEatAction":
        a = LittleEatAction(root=root)
    elif root.attrib["class"] == "LittleSleepAction":
        a = LittleSleepAction(root=root)
    elif root.attrib["class"] == "LittleMoveAction":
        a = LittleMoveAction(root=root)
    elif root.attrib["class"] == "LittleWorkAction":
        a = LittleWorkAction(root=root)
    #~ elif root.attrib["class"] == "LittleNewAction":
        #~ a = LittleNewAction(root=root) 
        #~ a.people = people
    else:
        a = LittleAction(root=root)
        
    a.people = people
    return a