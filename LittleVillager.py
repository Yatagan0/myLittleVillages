import utils, random, copy
import xml.etree.ElementTree as ET


class LittleVillager:
    def __init__(self, village):
        self.name = "defaultVillagerName"
        self.gender = 0
        self.object = None
        self.busy = False
        self.task = None
        self.position = [0., 0.]
        self.speed = 0.04 #1.0
        self.money = 0.0
        self.village = village
        self.destination = []

        
    def writeVillager(self, root):
        villager = ET.SubElement(root, 'villager')
        villager.set("name", self.name)
        villager.set("gender", str(self.gender))
        villager.set("busy", str(self.busy))
        if self.task is not None and self.busy:
            villager.set("task", str(self.task.id))
        villager.set("positionX", str(self.position[0]))
        villager.set("positionY", str(self.position[1]))
        villager.set("speed", str(self.speed))
        villager.set("money", str(self.money))
        if len(self.destination) > 0 :
            villager.set("destinationX", str(self.destination[0]))
            villager.set("destinationY", str(self.destination[1]))

    def readVillager(self, elem):
        att = elem.attrib
        self.name = att["name"]
        self.gender = int(att["gender"])
        self.busy = bool(att["busy"])
        
        self.position[0] = float(att["positionX"])
        self.position[1] = float(att["positionY"])
        self.speed = float(att["speed"])
        self.money = float(att["money"])
        if "task" in att.keys():
            self.task =int(att["task"])
        else:
            self.task = -1
        if "destinationX" in att.keys():
            self.destination = [0.0, 0.0]
            self.destination[0] = float(att["destinationX"])
            self.destination[1] = float(att["destinationY"])         
        
    def generate(self):
        self.name = utils.allU[random.randint(0, len(utils.allU)-1)]+utils.allL[random.randint(0, len(utils.allL)-1)] + " "+utils.allU[random.randint(0, len(utils.allU)-1)]+utils.allL[random.randint(0, len(utils.allL)-1)] +utils.allL[random.randint(0, len(utils.allL)-1)]
        self.gender = random.randint(0,1)
        
    def estimateTask(self, t):
        salary = float(t.salary)
        #~ print "salary ",salary
        cost = 0.
        if t.type == "carry":
            if not isinstance(t.initial, basestring):
                cost = utils.distance(self.position, t.initial.position) 
            else:
                cost = utils.distance(self.position, t.goal.position) 
        elif t.type == "build":
            if t.pos == []:
                
                cost = 1.
            else:
                cost = utils.distance(self.position, t.pos) 
        elif t.type == "production":
            cost = utils.distance(self.position, t.workshop.position) + t.remainingTime
        else:
            print t.type
            
        if cost == 0.:
            if t.mandatory:
                return 1.
            else:
                return 0.
        result = salary/cost
        if not t.mandatory:
            result = 0.8*result
        return result
        
    def selectTask(self, taskList):
        choice = []
        for t in taskList:
            #~ print t.name, "in state ", t.state
            if t.state== "to do" and t.canPerform():
                #~ print self.name, " executing ", t.name, " ", t.id
                p = self.estimateTask(t)
                choice.append([t, p])
                if len(choice) >= 10:
                    break
                
        if len(choice) ==0:
            return
        choice =  sorted(choice, key=lambda k: k[1]) 
        choice.reverse()
        #~ print "best value ",choice[0][1]
        #~ print "worst value ",choice[-1][1]
        
        
    
    
        r = random.randint(0, min(10, len(choice)-1))
        #~ print "r ",r
        rr = random.randint(0, r)
        #~ print "rr ",rr
        #~ print "len ", len(choice)
    
        self.busy=True
        self.task = choice[rr][0]
        
        
        #~ rr = random.randint(0, len(taskList) - 1)
        #~ self.task = taskList[rr]
        
        print self.name, " starts ", self.task.name, " ", self.task.id
        self.task.villager = self
        self.task.state = "in progress"
        return
            
    def goto(self, target):
        #~ return True
        #~ print "target ", target
        d = utils.distance(self.position, target)
        #~ print "distance ", d
        #~ print "target ", target
        if d < self.speed:
            self.position[0] = target[0]
            self.position[1] = target[1]
            return True
        else:
            self.position[0] += self.speed*(target[0] - self.position[0])/d
            #~ self.position[1] = target[1]
            self.position[1] += self.speed*(target[1] - self.position[1])/d
            #~ print "target ", target
            return False

        
    def performTask(self):
        #~ print "perform ",self.task.id
        toReturn = self.task.execute()
        if toReturn:
            
            #~ print "finished"
            self.task.state = "to do"
            #~ print self.task.name, " status ", self.task.status
            self.busy = False
        return toReturn

        

        
    def execute(self):
        if len(self.destination) > 0:
            #~ print "wandering"
            #~ print self.position
            if self.goto(self.destination):
                
                #~ print "end of wandering"
                self.destination = []
            #~ print self.position
        else:
            if not self.busy:
                list = self.village.getClosestTasks(self.position)
                self.selectTask(list)
                if not self.busy:
                    print "no task found. looking around"
                    self.destination = copy.copy(self.position)
                    self.destination[0] += random.randint(-1, 1)
                    self.destination[1] += random.randint(-1, 1)
            else:
                toDoNow = self.performTask()
                if toDoNow:
                    if self.task.status == "fail":
                    
                        print self.name, " failed ", self.task.name, " ", self.task.id
                        self.destination = copy.copy(self.position)
                        self.destination[0] += random.randint(-1, 1)
                        self.destination[1] += random.randint(-1, 1)   
                    #~ else:
                        #~ print self.name, " finished ", self.task.name, " ", self.task.id
                        

if __name__ == '__main__':
    lv = LittleVillager()