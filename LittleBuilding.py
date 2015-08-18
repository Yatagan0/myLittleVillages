import utils, random, copy
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
#~ from LittleNewAction import *

class WorkSlot:
    def __init__(self, root=None, types=[], building=None, name=""):
        
        self.building = building
        self.workTools = []
        if root is not None:
            self.read(root)
        else:
            self.types = types +["constructing"]*10
            #~ 
            self.name = name
            self.occupied = False

        
    def getPossibleActions(self, actionType=[]):
        if self.occupied:
            return []
            
            
        if "constructing" in self.types :
        
            if(actionType==[] or "work" in actionType or "build" in actionType):

                recipe = allRecipes["build"]
                meanTime = (recipe.timeMax - recipe.timeMin)/2.
                price=int(10*self.building.prices["basePrice"]*meanTime)/10.
                act = LittleWorkAction(workslot=self, type="build" )
                act.price = -price
                return [act]
            return []
            
        
        actions = []

        for type in self.types:
            if type not in workSlotTypes.keys():
                #~ print "no actions for workslot type ",type
                continue
            else:
                
                for a in workSlotTypes[type].recipes:
                    recipe = allRecipes[a]
                    
                    if actionType != []:
                        #~ print "recipe ",a, "action types ",actionType
                        if a in specialWorks and a not in actionType:
                            #~ print "special, not here"
                            continue
                        if a not in specialWorks and a not in actionType and "work" not in actionType:
                            #~ print "not special, not here"
                            continue
                    
                    meanTime = (recipe.timeMax - recipe.timeMin)/2.
                    price=int(10*self.building.prices["basePrice"]*meanTime)/10.
                    if a == "sleep":
                        act = LittleSleepAction(workslot=self)
                        act.price = price
                    elif a == "eat":
                        act = LittleEatAction(workslot=self)
                        act.price = utils.getDict(self.building.prices, "eat")
                        #~ act.price = price
                    else:
                        act = LittleWorkAction(workslot=self, type=a)
                        act.price = -int(10*self.building.prices["basePrice"]*meanTime)/10.
                    
                    if act.canExecute():
                        actions.append(act)
                    
        
        return actions
        
    def read(self, root):
        self.types = root.attrib["types"].split("-")
        if self.types[0] == '':
            self.types = []
        #~ print self.types
        self.name = root.attrib["name"]
        self.occupied = root.attrib["occupied"]=="True"
        for child in root:
            if child.tag == "worktool":
                self.workTools.append([child.attrib["name"], child.attrib["state"]])
        
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
        elem.set("occupied", str(self.occupied))
        for o in self.workTools:
            sub =  ET.SubElement(elem, 'worktool')
            sub.set("name", o[0])
            sub.set("state", o[1])

    def hasObjects(self, objects):
        #~ print "has objectss"
        takenObjects = []
        result = True
        for o in objects:
            if o[2] == "delete":
                if not o[0] in self.building.objects.keys():
                    result = False
                    utils.addToDict(self.building.wantObjects, o[0], 1)
                    #~ self.building.wantObjects.append(o[0])
                    break
                utils.addToDict(self.building.objects, o[0], -1)
                #~ self.building.objects.remove(o[0])
                takenObjects.append(o[0])
            else:
                if not self.hasObject(o[0], o[1]):
                    result = False
                    break
                    
        for o in takenObjects:
            utils.addToDict(self.building.objects, o, 1)
        #~ self.building.objects += takenObjects
        return result
                    
            

    def hasObject(self, name, state=""):
        for o in self.workTools:
            if o[0] == name:
                if state == "" or state==o[1]:
                    #~ print "has object ",name, state
                    return True
        #~ print "dont have object ",name, state
        return False
        
    def objectStatus(self, name, prev, new):
        if prev=="new":
            print "object ", name, " created in ", self.building.pos
            utils.addToDict(self.building.objects, name, 1)
            #~ self.building.objects.append(name)
            return
            
        if new == "delete":
            print "object ", name, " removed in ", self.building.pos
            #~ self.building.objects.remove(name)
            utils.addToDict(self.building.objects, name, -1)
            return         
        
        for o in self.workTools:
            if o[0] == name:
                
                if prev == "" or prev==o[1]:
                    o[1] = new
                    return

class LittleBuilding:
    def __init__(self, root=None, pos = [0., 0.], type="building", owner=None):

        self.possibleActions = []
        self.workSlots=[]
        self.objects={}
        self.wantObjects = {}
        self.wantToBuy = {}
        self.prices = {}
        self.costs = {}
        self.profits = {}
        
        if root is not None:
            self.read(root)
        else:
            self.pos = self.findFreePos(pos, 0)
            print "building ",type," at ",self.pos
            self.type = type
            self.name = "unnamed building"
            self.owner = owner
            if self.owner is not None:
                self.owner.ownedBuildings.append(self.pos)
            self.money=0
            self.prices["basePrice"] = 0.1
            #~ self.basePrice = 0.1
            self.lastManaged =0

        
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
        #~ elem.set("basePrice", str(self.basePrice))
        elem.set("lastManaged", str(self.lastManaged))
        if self.owner is None:
            elem.set("owner", "")
        elif isinstance(self.owner, basestring):
            elem.set("owner", self.owner)
        else:
            elem.set("owner", self.owner.name)
            
        utils.saveDict(elem, self.objects, 'object')
        utils.saveDict(elem, self.wantObjects, 'wantobject')
        utils.saveDict(elem, self.wantToBuy, 'wanttobuy')
        utils.saveDict(elem, self.prices, 'price')
        utils.saveDict(elem, self.costs, 'cost')
        utils.saveDict(elem, self.profits, 'profit')
        #~ for o in self.objects.keys():
            #~ sub =  ET.SubElement(elem, 'object')
            #~ sub.set("name", o)    
            #~ sub.set("quantity", str(self.objects[o]))
        #~ for o in self.wantObjects.keys():
            #~ sub =  ET.SubElement(elem, 'wantobject')
            #~ sub.set("name", o)    
            #~ sub.set("quantity", str(self.wantObjects[o]))            
        #~ for o in self.wantToBuy.keys():
            #~ sub =  ET.SubElement(elem, 'wanttobuy')
            #~ sub.set("name", o)    
            #~ sub.set("quantity", str(self.wantToBuy[o]))    
            
        #~ for p in self.prices.keys():
            #~ sub =  ET.SubElement(elem, 'price')
            #~ sub.set("name", p)    
            #~ sub.set("quantity", str(self.prices[p]))
            
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
        #~ self.basePrice = float(root.attrib["basePrice"])
        self.lastManaged = float(root.attrib["lastManaged"])
        from LittlePeople import peopleNamed
        self.owner = peopleNamed(root.attrib["owner"])
        if self.owner is None and root.attrib["owner"] is not "" :
            self.owner = root.attrib["owner"]
            
            
        for child in root:
            if child.tag == "workslot":
                #~ print "append workslot"
                self.workSlots.append(WorkSlot(root=child, building=self))
            elif child.tag == "object":
                self.objects[child.attrib["name"]] = float(child.attrib["quantity"])
                #~ utils.addToDict(self.objects, child.attrib["name"], 1.)
                #~ self.objects.append(child.attrib["name"])        
            elif child.tag == "wantobject":
                self.wantObjects[child.attrib["name"]] = float(child.attrib["quantity"])
                #~ utils.addToDict(self.wantObjects, child.attrib["name"], 1.)
                #~ self.wantObjects.append(child.attrib["name"])   
            elif child.tag == "wanttobuy":
                self.wantToBuy[child.attrib["name"]] = float(child.attrib["quantity"])
            elif child.tag == "price":
                self.prices[child.attrib["name"]] = float(child.attrib["quantity"])
            elif child.tag == "cost":
                self.costs[child.attrib["name"]] = float(child.attrib["quantity"])
            elif child.tag == "profit":
                self.profits[child.attrib["name"]] = float(child.attrib["quantity"])
                
    def findFreePos(self, pos, size):
        r0 = random.randint(pos[0]-size, pos[0]+size)
        r1 = random.randint(pos[1]-size, pos[1]+size)
        #~ print "trying at ",[r0, r1]
        if buildingImIn([r0, r1]) is None:
            return [r0, r1]
        return self.findFreePos(pos, size+1)
        
    def hourlyUpdate(self):
        #~ print "building hourly update"
        self.lastManaged +=1
            
    def dailyUpdate(self):
        pass       
 
    def update(self):
        pass   
        
    def getPossibleActions(self, isOwner=False, actionTypes=[]):
        #~ print self.owner
        actions = []
        for s in self.workSlots:
            actions = actions + s.getPossibleActions(actionTypes)
            
        if isOwner and (actionTypes == [] or "manage" in actionTypes):
            if len(self.workSlots) == 0:
                print "can't manage without workslots !"
            else:
                #~ print "manage action possible"
                actions.append(LittleManageAction(workslot=self.workSlots[0]))

            
        reallyWantToBuy = copy.deepcopy(self.wantToBuy)
            
        if actionTypes == [] or "buy" in actionTypes:
            for o in self.objects.keys():
                if utils.getDict(self.wantToBuy, o) > self.objects[o]:
                #~ if o in reallyWantToBuy.keys() and reallyWantToBuy[o] > 0:
                    #~ reallyWantToBuy[o] -=1
                #~ else:
                    #~ print "can sell ",o
                    actions.append(LittleBuyAction(workslot=self.workSlots[0], object=o))
            
        #~ print len(actions)," possible actions for type ",actionTypes," in ",self.name
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
            
            self.name = utils.randomBuildingName("restaurant", self.owner.name)
        else:
            self.name = utils.randomBuildingName("restaurant")

        for i in range(0, 3):
            ws = WorkSlot(types=["table"], building=self, name = "slot"+str(i))
            ws.workTools.append(["table", "clean"])
            self.workSlots.append(ws)
                
    def write(self, root):
        elem = LittleBuilding.write(self, root)
        elem.set("class", "LittleRestaurant")
    

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
            self.name = utils.randomBuildingName("hotel",self.owner.name)
        else:
            self.name = utils.randomBuildingNameName("hotel")

        for i in range(0, 5):
            ws = WorkSlot(types=["room"], building=self, name = "slot"+str(i))
            ws.workTools.append(["bed", "clean"])
            self.workSlots.append(ws)
        
                
    def write(self, root):
        elem = LittleBuilding.write(self, root)
        elem.set("class", "LittleHotel")

        
    def read(self, root):
        print "read hotel"
        LittleBuilding.read(self, root)

        
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

        for i in range(0, 3):
            ws = WorkSlot(types=["field"], building=self, name = "slot"+str(i))
            ws.workTools.append(["field", "clear"])
            self.workSlots.append(ws)
        
                
    def write(self, root):
        elem = LittleBuilding.write(self, root)
        elem.set("class", "LittleField")

 
class LittleShop(LittleBuilding):
    def __init__(self, root=None, owner=None, pos=None):
        LittleBuilding.__init__(self, root=root, pos=pos, type="shop", owner=owner)
        
        if root is not None:
            #~ self.read(root)
            pass
        else:
            self.owner = owner
            if self.owner is not None:
                self.name = utils.randomBuildingName("shop",self.owner.name)
            else:
                self.name = utils.randomBuildingNameName("shop")

            for i in range(0,1):
                ws = WorkSlot(types=["shop"], building=self, name = "slot"+str(i))
                self.workSlots.append(ws)
                
            #~ self.objects += ["pain", "pain", "pain"]
            for i in range(0, 3):
                utils.addToDict(self.objects, "pain", 1)
        
                
    def write(self, root):
        elem = LittleBuilding.write(self, root)
        elem.set("class", "LittleShop")

    def getPossibleActions(self, isOwner=False, actionTypes=[]):
        actions = LittleBuilding.getPossibleActions(self, isOwner, actionTypes)

        if actionTypes == [] or "buy" in actionTypes:
            for o in self.objects:
                print "can sell ",o
                actions.append(LittleBuyAction(workslot=self.workSlots[0], object=o))
            
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
        
    def findClosest(self, pos, checkReliable= True, notHere=None):
        dist = -1
        bestb=None
        #~ rpos = [0., 0.]
        
        for b in self.known:
            if notHere is not None and notHere[0] == b.pos[0] and notHere[1] == b.pos[1] :
                continue
            
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
                    
            if d < dist+1 and random.randint(0, 2) == 0:
                dist = d
                bestb = b
                
        if bestb is not None:
            return bestb.pos
        return None
        
    def getLastSeen(self):
        #~ blast = None
        #~ dmin = -1
        #~ for b in self.known:
            #~ t = -utils.globalTime.durationTo(b.lastSeen)

            #~ if dmin == -1 or t < dmin:
                #~ dmin = t
                #~ blast = b
                
        #~ return blast
        if len(self.known) == 0:
            return None
        
        return random.choice(self.known)
            
            
def readBuilding(root):
    #~ print "readBuilding ", root.attrib["class"]
    if root.attrib["class"] == "LittleRestaurant":
        b = LittleRestaurant(root=root)
    elif root.attrib["class"] == "LittleHotel":
        b = LittleHotel(root=root) 
    elif root.attrib["class"] == "LittleField":
        b = LittleField(root=root) 
    elif root.attrib["class"] == "LittleShop":
        b = LittleShop(root=root)  
    else:
        b = LittleBuilding(root=root)
    return b
            
if __name__ == '__main__':
    #~ b = LittleConstructingBuilding(pos=[0., 0.], owner=None, futureType="LittleHotel")
    #~ print b.__class__.__name__
    #~ b.finish()
    #~ print b.__class__.__name__
    b = LittleField(pos=[0., 0.])
    
    
    