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
            elem.set("posX", str(self.pos[0]))
            elem.set("posY", str(self.pos[1]))
        return elem

    def canExecute(self):
        if self.workslot is None or isinstance(self.workslot, basestring):
            from LittleBuilding import findWorkslot
            self.workslot = findWorkslot( self.pos, self.workslot)
        if self.type not in allRecipes.keys() or self.workslot is None:
            print "unknown recipe"
            return True
        recipe = allRecipes[self.type]
        for t in recipe.transformingStart:
            if not self.workslot.hasObject(t[0], t[1]):
                return False
        #TO DO
        return True
       
    def startExecution(self, people):
        self.people = people
        t = utils.globalTime
        self.startHour = [t.hour, t.minute]
        
        if self.workslot is None or isinstance(self.workslot, basestring):
            #~ print 'find workslot ', self.type
            from LittleBuilding import findWorkslot
            self.workslot = findWorkslot( self.pos, self.workslot)
        
        #~ print "starting ", self.workslot, " at ", self.pos

        if self.type not in allRecipes.keys():
            self.remainingTime = 60
            print people.name, " fait un truc"
            
        else:
            recipe = allRecipes[self.type]
            self.remainingTime = random.randint(recipe.timeMin, recipe.timeMax)
            if recipe.description != "":
                print people.name, " ", recipe.description
            if self.workslot is not None:
                self.workslot.occupied = True
             
                #~ print "transforming"
                for t in recipe.transformingStart:
                    #~ print t
                    self.workslot.objectStatus(t[0], t[1], t[2])
        
     
    def endExecution(self):
        if isinstance(self.workslot, basestring) :
            #~ print "workslot name ",self.workslot, " pos ",self.pos
            if self.pos is not None:
                if self.workslot is None or isinstance(self.workslot, basestring):
                    from LittleBuilding import findWorkslot
                    self.workslot = findWorkslot( self.pos, self.workslot)
            
        #~ print "ending ", self.workslot, " at ", self.pos
        if self.workslot is not None:
            if self.price > 0.:
                peopleRatio = 1.
                buildingRatio = 0.95
            else:
                peopleRatio = 0.95
                buildingRatio = 1.
                
            self.people.money -= peopleRatio*self.price
            self.workslot.building.money += buildingRatio*self.price
            self.workslot.occupied = False
            
            self.people.village.money += 0.05*abs(self.price)


        if self.type in allRecipes.keys():
            recipe = allRecipes[self.type]
             
            #~ print "transforming"
            for t in recipe.transformingEnd:
                #~ print t
                self.workslot.objectStatus(t[0], t[1], t[2])
                


       
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
        if isinstance(self.workslot, basestring) or self.workslot is None:
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
 
    
    def write(self, root):
        elem =  LittleAction.write(self, root)
        elem.set("class", "LittleSleepAction")
        return elem

    def endExecution(self):
        LittleAction.endExecution(self)
        self.people.tired = 0
        self.people.knowledge["sleep"].seenBuilding(pos=self.pos, reliable=1)
 
        
    def getLocation(self, people):
        if self.pos is None:
            self.pos = people.knowledge["sleep"].findClosest(people.pos)
        if isinstance(self.workslot, basestring) or self.workslot is None:
            from LittleBuilding import findWorkslot
            self.workslot = findWorkslot( self.pos, self.workslot)
        
class LittleEatAction(LittleAction):
    def __init__(self,root=None,workslot=None):
        LittleAction.__init__(self, root=root, type="eat", workslot=workslot)
            
    def write(self, root):
        elem =  LittleAction.write(self, root)
        elem.set("class", "LittleEatAction")
        return elem
 

    def endExecution(self):
        LittleAction.endExecution(self)
        self.people.hungry = 0
        self.people.knowledge["eat"].seenBuilding(pos=self.pos, reliable=1)        
        
    def getLocation(self, people):
        if self.pos is None:
            self.pos = people.knowledge["eat"].findClosest(people.pos)
        if isinstance(self.workslot, basestring) or self.workslot is None:
            from LittleBuilding import findWorkslot
            self.workslot = findWorkslot( self.pos, self.workslot)
            
class LittleWorkAction(LittleAction):
    def __init__(self,root=None,workslot=None, type="work"):
        LittleAction.__init__(self, root=root, type=type, workslot=workslot)
        if root is not None:
            self.read(root)
        
    def write(self, root):
        elem =  LittleAction.write(self, root)
        elem.set("class", "LittleWorkAction")
        #~ elem.set("description", self.description)
        return elem

    def endExecution(self):
        LittleAction.endExecution(self)
        if self.type == "build":
            #~ print self.workslot.types
            #~ print self.workslot.building.name, self.workslot.name
            self.workslot.types.remove("constructing")
        
        self.people.knowledge["work"].seenBuilding(pos=self.pos, reliable=1)       
 
    def getLocation(self, people):
        if self.pos is None:
            self.pos = people.knowledge["work"].findClosest(people.pos)
        if isinstance(self.workslot, basestring) or self.workslot is None:
            from LittleBuilding import findWorkslot
            self.workslot = findWorkslot( self.pos, self.workslot)
            
class LittleManageAction(LittleAction):
    def __init__(self,root=None,workslot=None ):
        LittleAction.__init__(self, root=root, type="manage", workslot=workslot)
        if root is not None:
            self.read(root)
                
    def write(self, root):
        elem =  LittleAction.write(self, root)
        elem.set("class", "LittleManageAction")
        #~ elem.set("description", self.description)
        return elem
        
        
    def canExecute(self):
        print "can execute move"
        return True
        
     
    def startExecution(self, people):
        LittleAction.startExecution(self, people)
        print self.people.name," manage ",self.workslot.business.name

    def execute(self):
        #~ if self.people.go(self.pos):
            #~ self.endExecution()
            #~ return False
            
        return True

    #~ def getLocation(self, people):
        #~ if self.pos is None:
            #~ self.pos = [people.pos[0]+random.randint(-1, 1), people.pos[1]+random.randint(-1, 1)]
            #~ print "self pos ",self.pos
        
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
            a = LittleEatAction()
            a.startHour = [7, 0]
            day.append(a)
            a = LittleEatAction()
            a.startHour = [12, 0]
            day.append(a)
            a = LittleEatAction( )
            a.startHour = [20, 0]
            day.append(a)
            a = LittleSleepAction()
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
    elif root.attrib["class"] == "LittleManageAction":
        a = LittleManageAction(root=root)
    else:
        a = LittleAction(root=root)
        
    a.people = people
    return a