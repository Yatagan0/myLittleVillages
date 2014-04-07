import utils, random



class LittleVillager:
    def __init__(self):
        self.name = "defaultVillagerName"
        self.gender = 0
        self.object = None
        self.busy = False
        self.task = None
        self.position = [0., 0.]
        self.speed = 1.0
        
    def generate(self):
        self.name = utils.allU[random.randint(0, len(utils.allU)-1)]+utils.allL[random.randint(0, len(utils.allL)-1)] + " "+utils.allU[random.randint(0, len(utils.allU)-1)]+utils.allL[random.randint(0, len(utils.allL)-1)] +utils.allL[random.randint(0, len(utils.allL)-1)]
        self.gender = random.randint(0,1)
        
    def selectTask(self, taskList):
        for t in taskList:
            #~ print t.name, "in state ", t.state
            if t.state== "to do":
                print self.name, " executing ", t.name
                self.busy=True
                self.task = t
                t.villager = self
                self.task.state = "in progress"
                return
            
    def goto(self, target):
        d = utils.distance(self.position, target)
        if d < self.speed:
            self.position = target
            return True
        else:
            self.position[0] += self.speed*(target[0] - self.position[0])/d
            self.position[1] += self.speed*(target[1] - self.position[1])/d
            return False

        
    def performTask(self):
        toReturn = self.task.execute()
        if toReturn:
            self.task.state = "to do"
            #~ print self.task.name, " status ", self.task.status
            self.busy = False
            return toReturn

if __name__ == '__main__':
    lv = LittleVillager()