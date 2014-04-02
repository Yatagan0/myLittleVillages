import utils, random

class LittleVillager:
    def __init__(self):
        self.name = "defaultVillagerName"
        self.gender = 0
        self.object = None
        self.busy = False
        
    def generate(self):
        self.name = utils.allU[random.randint(0, len(utils.allU)-1)]+utils.allL[random.randint(0, len(utils.allL)-1)] + " "+utils.allU[random.randint(0, len(utils.allU)-1)]+utils.allL[random.randint(0, len(utils.allL)-1)] +utils.allL[random.randint(0, len(utils.allL)-1)]
        self.gender = random.randint(0,1)
        
    def selectTask(self, taskList):
        self.busy=True
        
    def performTask(self):
        self.busy = False

if __name__ == '__main__':
    lv = LittleVillager()