import utils, random

allBuildings = []

def buildingImIn(pos):
    for b in allBuildings:
        if pos[0] == b.pos[0] and pos[1] == b.pos[1] :
            return b
    return None


class LittleBuilding:
    def __init__(self, pos, type):
        self.pos = self.findFreePos(pos, 0)
        print "building ",type," at ",self.pos
        self.type = type
        
        global allBuildings
        allBuildings.append(self)
        
        
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
        
    def seen(self, reliable):
        self.lastSeen = utils.globalTime.now()
        if reliable > -1:
            self.reliable = 0.9*self.reliable + 0.1*reliable        
        
class LittleBuildingList:

    
    def __init__(self):
        self.known = []
        
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
            
            
            
            