import utils, random
import xml.etree.ElementTree as ET


allBuildings = []

def buildingImIn(pos):
    if pos is None:
        return None
    for b in allBuildings:
        if pos[0] == b.pos[0] and pos[1] == b.pos[1] :
            return b
    return None
    
def buildingNamed(name):
    for b in allBuildings:
        if b.name == name:
            return b
            
def findWorkslot(pos, name):
    b = buildingImIn(pos)
    if b is not None:
        for s in b.workSlots:
            if s.name == name:
                return s
    return None

from LittleAction import *
from LittleNewAction import *

class WorkSlot:
    def __init__(self, root=None, types=[], building=None, name=""):
        
        self.building = building
        self.objects = []
        if root is not None:
            self.read(root)
        else:
            self.types = types
            self.objects.append(["bed", "clean"])
            self.name = name
        
    def getPossibleActions(self):
        actions = []
        for o in self.objects:
            if o[0] == "bed" and o[1] == "clean":
                actions.append(LittleNewAction(  price=1, workslot = self))
        return actions
        
    def read(self, root):
        self.types = root.attrib["types"].split("-")
        if self.types[0] == '':
            self.types = []
        #~ print self.types
        self.name = root.attrib["name"]
        for child in root:
            if child.tag == "object":
                self.objects.append([child.attrib["name"], child.attrib["state"]])
        
    def write(self, root):
        elem =  ET.SubElement(root, 'workslot')
        #~ print self.types
        s = ""
        for t in self.types:
            s+=t+"-"
        if len(s) > 0:
            s = s[:-1]
        #~ print s
        elem.set("types", s)
        elem.set("name", self.name)
        for o in self.objects:
            sub =  ET.SubElement(elem, 'object')
            sub.set("name", o[0])
            sub.set("state", o[1])

    def hasObject(self, name, state=""):
        for o in self.objects:
            if o[0] == name:
                if state == "" or state==o[1]:
                    return True
        return False
        
    def objectStatus(self, name, prev, new):
        for o in self.objects:
            if o[0] == name:
                if prev == "" or prev==o[1]:
                    o[1] = new
                    return

class LittleBuilding:
    def __init__(self, root=None, pos = [0., 0.], type="building", owner=None):

        self.possibleActions = []
        self.workSlots=[]

        if root is not None:
            self.read(root)
        else:
            self.pos = self.findFreePos(pos, 0)
            print "building ",type," at ",self.pos
            self.type = type
            self.name = "unnamed building"
            self.owner = owner
            self.money=0
            
            print "new work slots"
            for i in range(0, 3):
                self.workSlots.append(WorkSlot(types=["test", "building"], building=self, name = "slot"+str(i)))
        
        global allBuildings
        allBuildings.append(self)
        #~ print "num of buildings ",len(allBuildings)
        
    def write(self, root):
        elem =  ET.SubElement(root, 'building')
        elem.set("posX", str(self.pos[0]))
        elem.set("posY", str(self.pos[1]))
        elem.set("type", self.type)
        elem.set("name", self.name)
        elem.set("money", str(self.money))
        if self.owner is None:
            elem.set("owner", "")
        elif isinstance(self.owner, basestring):
            elem.set("owner", self.owner)
        else:
            elem.set("owner", self.owner.name)
            
        for s in self.workSlots:
            s.write(elem)
        elem.set("class", "LittleBuilding")
        return elem

    def read(self, root):
        self.type = root.attrib["type"]
        self.pos = [float(root.attrib["posX"]), float(root.attrib["posY"])]
        self.name = root.attrib["name"]
        #~ print self.name
        self.money = float(root.attrib["money"])
        from LittlePeople import peopleNamed
        self.owner = peopleNamed(root.attrib["owner"])
        if self.owner is None and root.attrib["owner"] is not "" :
            self.owner = root.attrib["owner"]
            
        for child in root:
            if child.tag == "workslot":
                #~ print "append workslot"
                self.workSlots.append(WorkSlot(root=child, building=self))
        
    def findFreePos(self, pos, size):
        r0 = random.randint(pos[0]-size, pos[0]+size)
        r1 = random.randint(pos[1]-size, pos[1]+size)
        #~ print "trying at ",[r0, r1]
        if buildingImIn([r0, r1]) is None:
            return [r0, r1]
        return self.findFreePos(pos, size+1)
        
    def getPossibleActions(self, isOwner=False):
        actions = []
        for s in self.workSlots:
            actions = actions + s.getPossibleActions()
        return actions
 
class LittleRestaurant(LittleBuilding):
    def __init__(self, root=None, owner=None, pos=None):
        LittleBuilding.__init__(self, root=root, pos=pos, type="restaurant", owner=owner)
        
        if root is not None:
            #~ self.read(root)
            pass
        else:
            self.owner = owner
            self.init()

            
    def init(self):
        if self.owner is not None:
            #~ print "OWNER ", self.owner
            if isinstance(self.owner, basestring):
                from LittlePeople import peopleNamed
                self.owner = peopleNamed(self.owner)
            
            self.name = utils.randomRestaurantName(self.owner.name)
        else:
            self.name = utils.randomRestaurantName()
            
        self.couverts = 3
        self.meals = 0
        self.cleanCouverts = self.couverts 
                
    def write(self, root):
        elem = LittleBuilding.write(self, root)
        elem.set("class", "LittleRestaurant")
        elem.set("couverts", str(self.couverts))
        elem.set("meals", str(self.meals))
        elem.set("cleancouverts", str(self.cleanCouverts))
        
    def read(self, root):
        LittleBuilding.read(self, root)
        self.couverts = int(root.attrib["couverts"])
        self.meals = int(root.attrib["meals"])
        self.cleanCouverts = int(root.attrib["cleancouverts"])
        
                
    def getPossibleActions(self, isOwner=False):
        actions = [LittleEatAction( people=None,startHour=[0, 0], pos=self.pos, price=4)]
        for i in range(self.couverts - self.meals):
            actions.append( LittleWorkAction( people=None,startHour=[0, 0], pos=self.pos, desc="prepare a manger chez", type="cook", price=-3))
        for i in range(self.couverts - self.cleanCouverts):
            actions.append( LittleWorkAction( people=None,startHour=[0, 0], pos=self.pos, desc="fait la plonge chez", type="dishes", price = -1))
        
        return actions
    

class LittleHotel(LittleBuilding):
    def __init__(self, root=None, owner=None, pos=None):
        LittleBuilding.__init__(self, root=root, pos=pos, type="hotel", owner=owner)
        
        if root is not None:
            #~ self.read(root)
            pass
        else:
            self.owner = owner
            self.init()
            
    def init(self):
        print "init !"
        if self.owner is not None:
            if isinstance(self.owner, basestring):
                from LittlePeople import peopleNamed
                self.owner = peopleNamed(self.owner)
            self.name = utils.randomHotelName(self.owner.name)
        else:
            self.name = utils.randomHotelName()
            
        self.beds = 6
        self.cleanBeds = self.beds
                
    def write(self, root):
        elem = LittleBuilding.write(self, root)
        elem.set("class", "LittleHotel")
        elem.set("beds", str(self.beds))
        elem.set("cleanbeds", str(self.cleanBeds))
        
    def read(self, root):
        print "read hotel"
        LittleBuilding.read(self, root)
        self.beds= int(root.attrib["beds"])
        self.cleanBeds = int(root.attrib["cleanbeds"])
        
                
    def getPossibleActions(self, isOwner=False):
        actions = [LittleSleepAction( people=None,startHour=[0, 0], pos=self.pos, price=1)]
        for i in range(self.beds - self.cleanBeds):
            actions.append( LittleWorkAction( people=None,startHour=[0, 0], pos=self.pos, desc="nettoie une chambre chez", type="cleanbed", price = -1))
        
        return actions
        
class LittleField(LittleBuilding):
    def __init__(self, root=None, owner=None, pos=None):
        LittleBuilding.__init__(self, root=root, pos=pos, type="field", owner=owner)
        
        if root is not None:
            #~ self.read(root)
            pass
        else:
            self.owner = owner
            self.init()
            
    def init(self):
        print "init !"
        if self.owner is not None:
            if isinstance(self.owner, basestring):
                from LittlePeople import peopleNamed
                self.owner = peopleNamed(self.owner)
        self.name = "field"

        self.planted=[["nothing", "none", [0, 0, 0, 0, 0]]]*3
        print self.planted

                
    def write(self, root):
        elem = LittleBuilding.write(self, root)
        elem.set("class", "LittleField")
        for p in self.planted:
            sub = ET.SubElement(elem, 'planted')
            sub.set("planted", p[0])
            sub.set("state", p[1])
            sub.set("minute", str(p[2][0]))
            sub.set("hour", str(p[2][1]))
            sub.set("day", str(p[2][2]))
            sub.set("month", str(p[2][3]))
            sub.set("year", str(p[2][4]))
        
    def read(self, root):
        LittleBuilding.read(self, root)
        self.planted = []
        for child in root:
            if (child.tag == "planted"):   
                p = []
                p.append(child.attrib["planted"])
                p.append(child.attrib["state"])
                p.append([int(child.attrib["minute"]), int(child.attrib["hour"]),int(child.attrib["day"]),int(child.attrib["month"]),int(child.attrib["year"])])
                self.planted.append(p)

        
                
    def getPossibleActions(self, isOwner=False):
        actions = []
               
        return actions
        
class LittleConstructingBuilding(LittleBuilding):
    def __init__(self, root=None, pos = [0., 0.], owner=None, futureType=None):
        
        LittleBuilding.__init__(self, root=root, pos=pos, type="constructing", owner=owner)
        
        if root is not None:
            pass
            #~ self.read(root)
        else:
        
            self.name = "constructing"
            self.futureType = futureType
            self.numWorkers = 4
            self.workTasks = 4
            
    def read(self, root):
        LittleBuilding.read(self, root)
        self.numWorkers= int(root.attrib["numWorkers"])
        self.workTasks = int(root.attrib["workTasks"])
        self.futureType = root.attrib["futureType"]
        
    def write(self, root):
        elem = LittleBuilding.write(self, root)
        elem.set("class", "LittleConstructingBuilding")
        elem.set("numWorkers", str(self.numWorkers))
        elem.set("workTasks", str(self.workTasks))      
        elem.set("futureType", self.futureType)      
        
    def finish(self):
        global allBuildings
        allBuildings.remove(self)
        if self.futureType == "LittleHotel":
            #~ self.__class__= LittleHotel
            self= LittleHotel( owner=self.owner, pos=self.pos)
        elif self.futureType == "LittleRestaurant":
            #~ self.__class__= LittleRestaurant
            self= LittleRestaurant( owner=self.owner, pos=self.pos)
        elif self.futureType == "LittleField":
            #~ self.__class__= LittleRestaurant
            self= LittleField( owner=self.owner, pos=self.pos) 
        else:
            #~ self.__class__= LittleBuilding
            self= LittleBuilding( owner=self.owner, pos=self.pos)
        #~ self.init()
        print "building in ",self.pos," is now finished ! Its name is ",self.name,"!"
        
    def getPossibleActions(self, isOwner=False):
        actions = []
        for i in range(min(self.numWorkers, self.workTasks)):
            actions.append( LittleWorkAction( people=None,startHour=[0, 0], pos=self.pos, desc="construit", type="construct", price = -2))
        
        return actions
       
class LittleKnownBuilding:
    def __init__(self, root=None, pos=[0., 0.]):
        
        if root is not None:
            self.read(root)
            return
        
        self.pos = pos
        self.lastSeen = utils.globalTime.now()
        self.reliable = 0.5

    def write(self, root):
        elem =  ET.SubElement(root, 'known') 
        elem.set("posX", str(self.pos[0]))
        elem.set("posY", str(self.pos[1]))
        elem.set("reliable", str(self.reliable))
        elem.set("minute", str(self.lastSeen[0]))
        elem.set("hour", str(self.lastSeen[1]))
        elem.set("day", str(self.lastSeen[2]))
        elem.set("month", str(self.lastSeen[3]))
        elem.set("year", str(self.lastSeen[4]))
        
    def read(self, root):
        self.pos = [float(root.attrib["posX"]), float(root.attrib["posY"])]
        self.reliable = float(root.attrib["reliable"])
        self.lastSeen = [int(root.attrib["minute"]),int(root.attrib["hour"]), int(root.attrib["day"]), int(root.attrib["month"]), int(root.attrib["year"])]
        
    def seen(self, reliable):
        #~ print "seen !"
        self.lastSeen = utils.globalTime.now()
        if reliable > -1:
            self.reliable = 0.9*self.reliable + 0.1*reliable        
       
class LittleBuildingList:

    def __init__(self, root=None, type=""):
        if root is not None:
            self.read(root)
            return
        self.known = []
        self.type = type
        
    def write(self, root):
        elem =  ET.SubElement(root, 'knowntype') 
        elem.set("type", self.type)
        for k in self.known:
            k.write(elem)
            
    def read(self, root):
        self.type = root.attrib["type"]
        self.known=[]
        for child in root:
            self.known.append(LittleKnownBuilding(root=child))
        
        
    def seenBuilding(self, building=None, pos=[0., 0.], reliable=-1):
        if building is not None:
            b = self.findBuilding(building.pos)
        else:
            b = self.findBuilding(pos)
        b.seen(reliable)
        
            
    def findBuilding(self, pos):
        for b in self.known:
            if pos[0] == b.pos[0] and pos[1] == b.pos[1] :
                return b
        #~ print "new buidling !"
        b = LittleKnownBuilding(pos=pos)
        self.known.append(b)
        return b
        
    def findClosest(self, pos, checkReliable= True):
        dist = -1
        bestb=None
        #~ rpos = [0., 0.]
        
        for b in self.known:
            d = utils.distance(pos, b.pos)
            if dist == -1:
                dist = d
                bestb = b
                continue
            #~ print b.pos
            if checkReliable:
                if bestb.reliable < b.reliable and random.randint(0, 2) == 0:
                    dist = d
                    bestb = b    
                    continue
                    
            if d < dist:
                dist = d
                bestb = b
                
        #~ print rpos
        return bestb.pos
        
    def getLastSeen(self):
        blast = None
        dmin = -1
        for b in self.known:
            t = -utils.globalTime.durationTo(b.lastSeen)
            #~ print t
            if dmin == -1 or t < dmin:
                dmin = t
                blast = b
                
        return blast
            
            
def readBuilding(root):
    #~ print "readBuilding ", root.attrib["class"]
    if root.attrib["class"] == "LittleRestaurant":
        b = LittleRestaurant(root=root)
    elif root.attrib["class"] == "LittleHotel":
        b = LittleHotel(root=root) 
    elif root.attrib["class"] == "LittleConstructingBuilding":
        b = LittleConstructingBuilding(root=root) 
    elif root.attrib["class"] == "LittleField":
        b = LittleField(root=root) 
    else:
        b = LittleBuilding(root=root)
    return b
            
if __name__ == '__main__':
    #~ b = LittleConstructingBuilding(pos=[0., 0.], owner=None, futureType="LittleHotel")
    #~ print b.__class__.__name__
    #~ b.finish()
    #~ print b.__class__.__name__
    b = LittleField(pos=[0., 0.])
    
    
    