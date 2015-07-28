import utils, random
import xml.etree.ElementTree as ET

from LittleRecipe import *

class LittleNewAction:
    def __init__(self, root=None, workslot = None, type="", price=0.):
        self.workslot = workslot
        self.type = type
        self.price = price
        self.people = None
        self.pos = None
        self.startHour = None#[0., 0.]
        if root is not None:
            self.read(root)
        else:
            self.remainingTime = 30
            #~ self.status= "not started"
            
        if self.type not in allRecipes.keys():
            print "unknown recipe"
            
            
    
    def read(self, root):
        self.type = root.attrib["type"]
        if "startHour" in root.attrib.keys():
            self.startHour = [int(root.attrib["startHour"]),int(root.attrib["startMinute"]) ]
        self.remainingTime = int(root.attrib["remainingTime"])
        self.price = float(root.attrib["price"])

        if "workslotName" in root.attrib.keys():
            self.workslot = root.attrib["workslotName"]
            self.pos = [float(root.attrib["posX"]),float(root.attrib["posY"]) ]
            from LittleBuilding import findWorkslot
            self.workslot = findWorkslot( self.pos, self.workslot)

        
    def write(self, root):
        elem =  ET.SubElement(root, 'action')
        elem.set("class", "LittleNewAction")
        elem.set("type", self.type)
        if self.startHour is not None:
            elem.set("startHour", str(self.startHour[0]))
            elem.set("startMinute", str(self.startHour[1]))
        elem.set("remainingTime", str(self.remainingTime))
        elem.set("price", str(self.price))
        if self.workslot is not None:
            elem.set("workslotName", self.workslot.name);
            elem.set("posX", str(self.workslot.building.pos[0]))
            elem.set("posY", str(self.workslot.building.pos[1]))
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
        self.status = "executing"

        if self.type not in allRecipes.keys():
            self.remainingTime = 60
            print people.name, " fait un truc"
            
        else:
            self.remainingTime = random.randint(allRecipes[self.type].timeMin, allRecipes[self.type].timeMax)
            print people.name, " ", allRecipes[self.type].description, " pendant ",self.remainingTime 
        
     
    def endExecution(self):
        if self.workslot is not None:
            self.people.money -= self.price
            self.workslot.building.money += self.price
            print "has workslot"
            self.workslot.objectStatus("bed", "clean", "dirty")
       
    def execute(self):
        self.remainingTime -= 1
        if self.remainingTime <= 0:
            
            self.endExecution()
            return False
            
        return True

        
    def init(self):
        print "init"
    
    def copy(self):
        print "copy"
        root = ET.Element('village')
        act = self.write(root)
        a = LittleNewAction(root=act)
        return a
        
    def hasLocation(self):
        return self.pos != None
        
    def getLocation(self, people):
        if self.pos is None:
            self.pos = [people.pos[0], people.pos[1]]
        if isinstance(self.workslot, basestring):
            from LittleBuilding import findWorkslot
            self.workslot = findWorkslot( self.pos, self.workslot)