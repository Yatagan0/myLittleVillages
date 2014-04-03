import utils, random

class LittleTask:
    def __init__(self):
        self.state = "to do"
        self.status = "to start"
        


class LittleBuildTask(LittleTask):
    def __init__(self, name):
        LittleTask.__init__(self)
        self.name = name
        self.materials = {}
        
        if name == "warehouse":
            self.remainingTime = 10
            self.materials["wood"] = 10
            self.materials["stone"] = 10
            
    def execute(self, param):
        print self.name, " executing"
        if self.status is "to do":
            #select position
            #add bring items
            self.status = "waiting for materials"
        elif self.status is "waiting for materials":
            #check if remaining materials
            self.status = "building"
        elif self.status is "building":
            #check if remaining time
            self.status = "done"
            

class LittleCarryTask(LittleTask):
    def __init__(self):
        LittleTask.__init__(self)
        
        
class LittleWorkTask(LittleTask):
    def __init__(self):
        LittleTask.__init__(self)
        
if __name__ == '__main__':
    lbt = LittleBuildTask()
