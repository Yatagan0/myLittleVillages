import utils, random

global taskID 
taskID = 0

class LittlePlace:
    def __init__(self):
        self.name = "defaultPlaceName"
        self.position =[0, 0]
        self.content = {}
        self.state = "ok"
        
        global taskID
        self.id = taskID
        taskID += 1


class LittleExternalPlace(LittlePlace):
    def __init__(self):
        LittlePlace.__init__(self)

class LittleBuilding(LittlePlace):
    def __init__(self, name):
        LittlePlace.__init__(self)
        self.name = name
        self.capacity = 0
        
        self.demand = []
        
        self.productionTask = []
        

if __name__ == '__main__':
    lb = LittleBuilding()
    print lb.name