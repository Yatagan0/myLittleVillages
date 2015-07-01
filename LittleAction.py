import utils, random
import xml.etree.ElementTree as ET



class LittleAction:
    def __init__(self, root=None, people=None, type="do nothing", startHour=None, pos=None):
        self.people = people 
        self.pos = pos
        self.building = None
        if root is not None:
            self.read(root)
            return
        

        self.type = type
        self.startHour = startHour
 
        self.init()
        
    def __str__(self):
        s = self.type+" starting "+str(self.startHour[0])+":"+str(self.startHour[1])+"\n"
        return s
        
    def read(self, root):
        self.type = root.attrib["type"]
        self.startHour = [int(root.attrib["startHour"]),int(root.attrib["startMinute"]) ]
        self.status = root.attrib["status"]
        self.remainingTime = int(root.attrib["remainingTime"])
        if "posX" in root.attrib.keys():
            #~ print "has pos"
            self.pos = [float(root.attrib["posX"]),float(root.attrib["posY"]) ]
            #~ print self.pos
        #~ else:
            #~ print "no pos"
        
    def write(self, root):
        elem =  ET.SubElement(root, 'action')
        elem.set("class", "LittleAction")
        elem.set("type", self.type)
        elem.set("startHour", str(self.startHour[0]))
        elem.set("startMinute", str(self.startHour[1]))
        elem.set("status", self.status)
        elem.set("remainingTime", str(self.remainingTime))
        if self.pos is not None:
            elem.set("posX", str(self.pos[0]))
            elem.set("posY", str(self.pos[1]))
        return elem
        
    def execute(self):
        if self.status == "not started":
            t = utils.globalTime
            self.startHour = [t.hour, t.minute]
        self.status = "executing"
        self.remainingTime -= 1
        return self.remainingTime > 0
        
    def init(self):
        #~ print "init"
        self.status = "not started"
        self.remainingTime = 59
    
    def copy(self):
        a = LittleAction(people=self.people, type=self.type, startHour=self.startHour, pos=self.pos)
        return a
        
    def hasLocation(self):
        return self.pos != None
        
    def getLocation(self):
        self.pos = [self.people.pos[0], self.people.pos[1]]
        
class LittleMoveAction(LittleAction):
    def __init__(self,root=None,people=None, startHour=None,pos=None):
        LittleAction.__init__(self, root,people,"move", startHour, pos)
        if root is not None:
            self.read(root)
        #~ else:
            #~ self.pos = 
            
    def read(self, root):
        LittleAction.read(self,root)
        #~ self.pos = [float(root.attrib["posX"]),float(root.attrib["posY"]) ]
        
        
    def write(self, root):
        elem =  LittleAction.write(self, root)
        #~ elem.set("posX", str(self.pos[0]))
        #~ elem.set("posY", str(self.pos[1]))
        elem.set("class", "LittleMoveAction")

        
    def copy(self):
        a = LittleMoveAction(people=self.people, startHour=self.startHour, pos=self.pos)
        return a      

    def execute(self):
        if self.status == "not started":
            t = utils.globalTime
            self.startHour = [t.hour, t.minute]

        self.status = "executing"
        if self.people.go(self.pos):
            return False
                
        return True     

    def getLocation(self):
        self.pos = [self.people.pos[0]+random.randint(-1, 1), self.people.pos[1]+random.randint(-1, 1)]
        #~ from LittleBuilding import buildingImIn
        #~ self.buidling = buildingImIn(self.pos)
        
class LittleSleepAction(LittleAction):
    def __init__(self,root=None,people=None, startHour=None,pos=None):
        LittleAction.__init__(self, root,people,"sleep", startHour, pos)
        if root is not None:
            self.read(root)
        else:
            self.init()
        
    def init(self):
        self.status = "not started"
        self.remainingTime = 7*60 +random.randint(0, 60)
        #~ self.pos = [0., 0.]
        
    def read(self, root):
        LittleAction.read(self,root)
        #~ self.pos = [float(root.attrib["posX"]),float(root.attrib["posY"]) ]
        if self.pos is not None:
            
            from LittleBuilding import buildingImIn
            self.building = buildingImIn(self.pos)
    
    def write(self, root):
        elem =  LittleAction.write(self, root)
        #~ elem.set("posX", str(self.pos[0]))
        #~ elem.set("posY", str(self.pos[1]))
        elem.set("class", "LittleSleepAction")

        
    def copy(self):
        a = LittleSleepAction(people=self.people, startHour=self.startHour, pos=self.pos)
        return a
        
    def execute(self):
        if self.status == "not started":
            t = utils.globalTime
            self.startHour = [t.hour, t.minute]
           
        self.status = "executing"
        if self.people.go(self.pos):
            self.remainingTime -= 1
            if self.remainingTime > 0:
                return True
                
            else:
                self.people.tired = 0
                self.people.knowledge["sleep"].seenBuilding(pos=self.pos)
                return False
                
        return True
        
    def getLocation(self):
        if self.pos is None:
            self.pos = self.people.knowledge["sleep"].findClosest(self.people.pos)
        from LittleBuilding import buildingImIn
        self.buidling = buildingImIn(self.pos)
        
class LittleEatAction(LittleAction):
    def __init__(self,root=None, people=None, startHour=None,pos=None):
        LittleAction.__init__(self,root, people, "eat", startHour,pos)
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
        a = LittleEatAction(people=self.people, startHour=self.startHour, pos=self.pos)
        return a
        
    def execute(self):
        
        if self.building is None:
                from LittleBuilding import buildingImIn
                self.building = buildingImIn(self.pos)

        if self.status == "not started":
            t = utils.globalTime
            self.startHour = [t.hour, t.minute]
            
            print self.people.name, " va manger a ",self.building.name
            #~ print self.people.name, " va manger a ",self.pos
        self.status = "executing"
        if self.people.go(self.pos):
            self.remainingTime -= 1
            if self.remainingTime > 0:
                return True
                
            else:
                self.people.hungry = 0
                self.people.knowledge["eat"].seenBuilding(pos=self.pos, name=self.building.name)
                return False
                
        return True
        
    def getLocation(self):
        if self.pos is None:
            self.pos = self.people.knowledge["eat"].findClosest(self.people.pos)
        from LittleBuilding import buildingImIn
        self.building = buildingImIn(self.pos)
        #~ print "get location ",self.pos
        #~ print "get location ",self.building.name

        
class LittleOldActions():
    def __init__(self,people, root=None):
        self.days = []
        if root is not None:
            
            self.read(root, people)
            return
            
        for i in range(0,9):
            day = []
            #~ day.append(LittleAction("sleep", [6, 0]))
            day.append(LittleEatAction( people=people,startHour=[7, 0]))
            #~ day.append(LittleAction(people,"do nothing", [8, 0]))
            #~ day.append(LittleAction(people,"do nothing", [11, 0]))
            day.append(LittleEatAction(people=people,startHour= [12, 0]))
            #~ day.append(LittleAction(people,"do nothing", [13, 0]))
            #~ day.append(LittleAction(people,"do nothing", [19, 0]))
            day.append(LittleEatAction( people=people,startHour=[20, 0]))
            #~ day.append(LittleAction(people,"do nothing", [21, 0]))
            day.append(LittleSleepAction( people=people,startHour=[22, 0]))
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
        a.init()
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
        a = LittleEatAction(root=root, people=people)
    elif root.attrib["class"] == "LittleSleepAction":
        a = LittleSleepAction(root=root, people=people)
    elif root.attrib["class"] == "LittleMoveAction":
        a = LittleMoveAction(root=root, people=people)
    else:
        a = LittleAction(root=root, people=people)
    return a