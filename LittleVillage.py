import utils
from LittlePeople import *
from LittleBuilding import *

buildings = ["restaurant", "hotel"]+[ "field"]*3

class LittleVillage:
    def __init__(self, root=None):
        self.people = []        
        if root is not None:
            self.read(root)
        else:
            self.name = utils.randomCityName()
            self.money=0.
        
        
    def read(self, root):
        self.name = root.attrib["name"]
        self.money = float(root.attrib["money"])
        for child in root:
            if (child.tag == "time"):
                utils.globalTime.read(child)
            elif (child.tag == "people"):
                p=LittlePeople(child)
                p.village=self
                self.people.append(p)
            elif child.tag == "building":
                b = readBuilding(child)
        
        
    def write(self, root):
        root.set("name", self.name)
        root.set("money", str(self.money))
        for p in self.people:
            p.write(root)
        return root
        
    def update(self):
        utils.globalTime.addTime()
        print utils.globalTime
        
        if utils.globalTime.minute == 0:
            #~ print "hourly update"
            self.hourlyUpdate()
            if utils.globalTime.hour == 0:
                #~ print "daily update"
                self.dailyUpdate()
        
        for p in self.people:
            p.update()
            
        for b in allBuildings:
            b.update()
    
            
    def hourlyUpdate(self):
        for p in self.people:
            p.hourlyUpdate()
            
        for b in allBuildings:
            b.hourlyUpdate()
            
    def dailyUpdate(self):
        for p in self.people:
            p.dailyUpdate()
            
        for b in allBuildings:
            b.dailyUpdate()
            
        if self.money >= 5.0:
            self.addPeople()
        
    def addPeople(self):
        
        buildingType =buildings[len(self.people)%len(buildings)]

        p = LittlePeople()
        self.people.append(p)
        if buildingType=="restaurant":
            b = LittleRestaurant( pos=[0.,0.], owner=p)
            #~ p.knowledge["eat"].seenBuilding(building=b)
        elif buildingType=="hotel":
            b = LittleHotel( pos=[0.,0.], owner=p)
            #~ p.knowledge["sleep"].seenBuilding(building=b)
        elif buildingType=="field":
            b = LittleField( pos=[0.,0.], owner=p)
            #~ p.knowledge["work"].seenBuilding(building=b)
        
        p.village = self
            
        self.money -=5