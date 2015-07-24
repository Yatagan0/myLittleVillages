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
        else:
            self.remainingTime = 30
            self.status= "not started"
            
            
    
    def read(self, root):
        print "READ"
        self.type = root.attrib["type"]
        if "startHour" in root.attrib.keys():
            self.startHour = [int(root.attrib["startHour"]),int(root.attrib["startMinute"]) ]
        self.status = root.attrib["status"]
        self.remainingTime = int(root.attrib["remainingTime"])
        self.price = float(root.attrib["price"])
        #~ if "posX" in root.attrib.keys():
            #~ self.pos = [float(root.attrib["posX"]),float(root.attrib["posY"]) ]
            #~ from LittleBuilding import buildingImIn
            #~ self.building = buildingImIn(self.pos)
        if "workslotName" in root.attrib.keys():
            self.workslot = root.attrib["workslotName"]
            self.pos = [float(root.attrib["posX"]),float(root.attrib["posY"]) ]
            from LittleBuilding import findWorkslot
            self.workslot = findWorkslot( self.pos, self.workslot)
            
            #~ self.building = buildingImIn(self.pos)
            
            #~ if self.building is not None:
                #~ for s in self.building.workSlots:
                    #~ if s.name == root.attrib["workslotName"]:
                        #~ self.workslot = s
        
    def write(self, root):
        print "WRITING"
        elem =  ET.SubElement(root, 'action')
        elem.set("class", "LittleNewAction")
        elem.set("type", self.type)
        elem.set("startHour", str(self.startHour[0]))
        elem.set("startMinute", str(self.startHour[1]))
        elem.set("status", self.status)
        elem.set("remainingTime", str(self.remainingTime))
        elem.set("price", str(self.price))
        if self.workslot is not None:
            elem.set("workslotName", self.workslot.name);
            elem.set("posX", str(self.workslot.building.pos[0]))
            elem.set("posY", str(self.workslot.building.pos[1]))
        return elem
       
    def startExecution(self, people):
        self.people = people
        t = utils.globalTime
        self.startHour = [t.hour, t.minute]
        self.status = "executing"
     
    def endExecution(self):
        pass
       
    def execute(self):
        #~ if self.status == "not started":
            #~ t = utils.globalTime
            #~ self.startHour = [t.hour, t.minute]
        #~ self.status = "executing"
        self.remainingTime -= 1
        if self.remainingTime <= 0:
            if self.workslot is not None:
                self.people.money -= self.price
                self.workslot.building.money += self.price
            
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
        
    def getLocation(self):
        self.pos = [0., 0.]
        #~ self.pos = [self.people.pos[0], self.people.pos[1]]