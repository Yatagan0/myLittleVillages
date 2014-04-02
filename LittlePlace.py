import utils, random

class LittlePlace:
    def __init__(self):
        self.name = "defaultPlaceName"
        self.position =[0, 0]
        self.content = []


class LittleExternalPlace(LittlePlace):
    def __init__(self):
        LittlePlace.__init__(self)

class LittleBuilding(LittlePlace):
    def __init__(self):
        LittlePlace.__init__(self)
        

if __name__ == '__main__':
    lb = LittleBuilding()
    print lb.name