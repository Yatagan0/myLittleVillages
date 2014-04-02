import utils, random

class LittleTask:
    def __init__(self):
        self.state = "to do"
        


class LittleBuildTask(LittleTask):
    def __init__(self, name):
        LittleTask.__init__(self)
        self.name = name
        self.materials = {}
        
        if name == "warehouse":
            self.remainingTime = 10
            self.material["wood"] = 10
            self.material["stone"] = 10
            

class LittleCarryTask(LittleTask):
    def __init__(self):
        LittleTask.__init__(self)
        
        
class LittleWorkTask(LittleTask):
    def __init__(self):
        LittleTask.__init__(self)
        
if __name__ == '__main__':
    lbt = LittleBuildTask()
