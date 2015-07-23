import utils, random
import xml.etree.ElementTree as ET



class LittleNewAction:
    def __init__(self, root=None, workslot = None, type="do nothing test", price=0.):
        self.workslot = workslot
        self.type = type
        self.price = price
        self.people = None
        self.pos = None
        if root is not None:
            self.read(root)
            
            
    
    def read(self, root):
        print "READ"
        self.type = root.attrib["type"]
        #~ self.startHour = [int(root.attrib["startHour"]),int(root.attrib["startMinute"]) ]
        #~ self.status = root.attrib["status"]
        #~ self.remainingTime = int(root.attrib["remainingTime"])
        self.price = float(root.attrib["price"])
        #~ if "posX" in root.attrib.keys():
            #~ self.pos = [float(root.attrib["posX"]),float(root.attrib["posY"]) ]
            #~ from LittleBuilding import buildingImIn
            #~ self.building = buildingImIn(self.pos)
        if "workslotName" in root.attrib.keys():
            self.workslot = root.attrib["workslotName"]
            pos = [float(root.attrib["posX"]),float(root.attrib["posY"]) ]
            from LittleBuilding import buildingImIn
            self.building = buildingImIn(self.pos)
            
            if self.building is not None:
                for s in self.building.workSlots:
                    if s.name == root.attrib["workslotName"]:
                        self.workslot = s
        
    def write(self, root):
        print "WRITING"
        elem =  ET.SubElement(root, 'action')
        elem.set("class", "LittleNewAction")
        elem.set("type", self.type)
        #~ elem.set("startHour", str(self.startHour[0]))
        #~ elem.set("startMinute", str(self.startHour[1]))
        #~ elem.set("status", self.status)
        #~ elem.set("remainingTime", str(self.remainingTime))
        elem.set("price", str(self.price))
        if self.workslot is not None:
            elem.set("workslotName", self.workslot.name);
            elem.set("posX", str(self.workslot.building.pos[0]))
            elem.set("posY", str(self.workslot.building.pos[1]))
        return elem
        
    def execute(self):
        print "EXECUTE"
        return False

        
    def init(self):
        print "init"
    
    def copy(self):
        print "copy"
        a = LittleNewAction(workslot=self.workslot, type=self.type,  price=self.price)
        return a
        
    def hasLocation(self):
        return self.pos != None
        
    def getLocation(self):
        self.pos = [0., 0.]
        #~ self.pos = [self.people.pos[0], self.people.pos[1]]