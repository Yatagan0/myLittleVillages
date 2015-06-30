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
 

class LittleKnownBuilding:
    def __init__(self, pos):
        
        self.pos = pos
        self.lastSeen = utils.globalTime.now()
        self.reliable = 0.5
        
    def write(self, root):
        elem =  ET.SubElement(root, 'known') 
        elem.set("posX", str(self.pos[0]))
        elem.set("posY", str(self.pos[1]))
        elem.set("reliable", str(self.reliable))
        elem.set("minute", str(self.lastSeen[0]))
        subel.set("hour", str(self.lastSeen[1]))
        subel.set("day", str(self.lastSeen[2]))
        subel.set("month", str(self.lastSeen[3]))
        subel.set("year", str(self.lastSeen[4]))
        
    def seen(self, reliable):
        print "seen !"
        self.lastSeen = utils.globalTime.now()
        if reliable > -1:
            self.reliable = 0.9*self.reliable + 0.1*reliable        
       
class LittleBuildingList:

    
    def __init__(self):
        self.known = []
        
    def write(self, root, type):
        elem =  ET.SubElement(root, 'knowntype') 
        elem.set("type", type)
        for k in self.known:
            k.write(elem)
        
    def seenBuilding(self, building, reliable=-1):
        b = self.findBuilding(building.pos)
        b.seen(reliable)
        
            
    def findBuilding(self, pos):
        for b in self.known:
            if pos[0] == b.pos[0] and pos[1] == b.pos[1] :
                return b
        
        b = LittleKnownBuilding(pos)
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
            
            
            
            