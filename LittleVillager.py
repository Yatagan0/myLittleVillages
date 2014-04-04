import utils, random

class LittleVillager:
    def __init__(self):
        self.name = "defaultVillagerName"
        self.gender = 0
        self.object = None
        self.busy = False
        self.task = None
        
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
                self.task.state = "in progress"
                return
            


        
    def performTask(self):
        self.task.execute([])
        self.task.state = "to do"
        print self.task.name, " status ", self.task.status
        self.busy = False

if __name__ == '__main__':
    lv = LittleVillager()