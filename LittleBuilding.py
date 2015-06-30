import utils, random
import xml.etree.ElementTree as ET

allBuildings = []

def buildingImIn(pos):
    for b in allBuildings:
        if pos[0] == b.pos[0] and pos[1] == b.pos[1] :
            return b
    return None


class LittleBuilding:
    def __init__(self, root=None, pos = [0., 0.], type="building"):

        if root is not None:
            self.read(root)
        else:
            self.pos = self.findFreePos(pos, 0)
            print "building ",type," at ",self.pos
            self.type = type
            
        self.possibleActions = []
        
        global allBuildings
        allBuildings.append(self)
        
    def write(self, root):
        elem =  ET.SubElement(root, 'building')
        elem.set("posX", str(self.pos[0]))
        elem.set("posY", str(self.pos[1]))
        elem.set("type", self.type)

    def read(self, root):
        self.type = root.attrib["type"]
        self.pos = [float(root.attrib["posX"]), float(root.attrib["posY"])]
        
    def findFreePos(self, pos, size):
        r0 = random.randint(pos[0]-size, pos[0]+size)
        r1 = random.randint(pos[1]-size, pos[1]+size)
        #~ print "trying at ",[r0, r1]
        if buildingImIn([r0, r1]) is None:
            return [r0, r1]
        return self.findFreePos(pos, size+1)
        
    def getPossibleActions(self):
        return []
 

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
        
    def findClosest(self, pos):
        dist = 10000
        rpos = [0., 0.]
        
        for b in self.known:
            #~ print b.pos
            d = utils.distance(pos, b.pos)
            if d < dist:
                dist = d
                rpos = b.pos
                
        #~ print rpos
        return rpos
        
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
            
            
            
            