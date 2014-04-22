import utils, random

global taskID 
taskID = 0

class LittlePlace:
    def __init__(self, village):
        self.name = "defaultPlaceName"
        self.type = "defaultPlaceType"
        self.position =[0, 0]
        self.content = {}
        self.state = "ok"
        
        self.village = village
        
        global taskID
        self.id = taskID
        taskID += 1


class LittleExternalPlace(LittlePlace):
    def __init__(self,name,  village):
        LittlePlace.__init__(self, village)
        self.type = "field"
        self.name = name

class LittleBuilding(LittlePlace):
    def __init__(self, name, village):
        LittlePlace.__init__(self, village)
        self.type = "defaultBuilding"
        self.name = name
        self.capacity = 0
        
        self.demand = []
        
        self.productionTask = []
        
        
class LittleStorage(LittleBuilding):
    def __init__(self, name, village):
        LittleBuilding.__init__(self, name, village)
        self.type = "storage"

class LittleHouse(LittleBuilding):
    def __init__(self, name, village):
        LittleBuilding.__init__(self, name, village)
        self.type = "house"

class LittleWorkshop(LittleBuilding):
    def __init__(self, name, village):
        LittleBuilding.__init__(self, name, village)
        self.type = "production"   
        self.production = ""
        self.productionTime = 0

    def startProducing(self, prod, time, num):
        self.production = prod
        self.productionTime = time
        for i in range(0, num):
            self.addProductionTask()
            
    def addProductionTask(self):
        pass
        
def newBuilding(type, name, position, state, village):
    #~ print "new building"
    if type == "storage":
        b =  LittleStorage(name, village)
    elif type == "house":
        b =  LittleWorkshop(name, village)
    elif type == "field":
        b = LittleExternalPlace(name, village)
    elif type == "production":
        b =  LittleHouse(name, village)
    else:
        print "warning, ",type," not recognized as a place type"
        b = LittlePlace(village)
        
    b.state = state
    b.position = position
    village.buildings.append(b)
    return b
    

if __name__ == '__main__':
    lb = LittleBuilding()
    print lb.name