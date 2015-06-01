import utils, random

class LittleAction:
    def __init__(self, people, type, startHour):
        self.people = people
        self.type = type
        self.startHour = startHour
        self.init()
        
    def __str__(self):
        s = self.type+" starting "+str(self.startHour[0])+":"+str(self.startHour[1])+"\n"
        return s
        
    def execute(self):
        if self.status == "not started":
            t = utils.globalTime
            self.startHour = [t.hour, t.minute]
        self.status = "executing"
        self.remainingTime -= 1
        return self.remainingTime > 0
        
    def init(self):
        self.status = "not started"
        self.remainingTime = 59
    
    def copy(self):
        a = LittleAction(self.people, self.type, self.startHour)
        return a
        
class LittleSleepAction(LittleAction):
    def __init__(self,people, startHour):
        LittleAction.__init__(self, people,"sleep", startHour)
        self.init()
        
    def init(self):
        self.status = "not started"
        self.remainingTime = 7*60 +random.randint(0, 60)
        self.pos = []
        
    def copy(self):
        a = LittleSleepAction(self.people, self.startHour)
        return a
        
    def execute(self):
        if self.status == "not started":
            t = utils.globalTime
            self.startHour = [t.hour, t.minute]
            self.pos = self.people.knowledge["sleep"].findClosest(self.people.pos)
        self.status = "executing"
        if self.people.go(self.pos):
            self.remainingTime -= 1
            if self.remainingTime > 0:
                return True
                
            else:
                self.people.tired = 0
                return False
                
        return True
        
class LittleEatAction(LittleAction):
    def __init__(self,people, startHour):
        LittleAction.__init__(self,people, "eat", startHour)
        self.init()
        
    def init(self):
        self.status = "not started"
        self.remainingTime = 45 +random.randint(0, 15)
        self.pos = []
        
    def copy(self):
        a = LittleEatAction(self.people, self.startHour)
        return a
        
    def execute(self):
        #~ result = LittleAction.execute(self)
        
        #~ if result is False:
            #~ self.people.hungry = 0
        #~ return result
        
        
        if self.status == "not started":
            t = utils.globalTime
            self.startHour = [t.hour, t.minute]
            self.pos = self.people.knowledge["eat"].findClosest(self.people.pos)
        self.status = "executing"
        if self.people.go(self.pos):
            self.remainingTime -= 1
            if self.remainingTime > 0:
                return True
                
            else:
                self.people.hungry = 0
                return False
                
        return True
        
class LittleOldActions():
    def __init__(self,people, toRead=None):
        self.days = []
        if toRead is None:
            for i in range(0,9):
                day = []
                #~ day.append(LittleAction("sleep", [6, 0]))
                day.append(LittleEatAction( people,[7, 0]))
                #~ day.append(LittleAction(people,"do nothing", [8, 0]))
                #~ day.append(LittleAction(people,"do nothing", [11, 0]))
                day.append(LittleEatAction(people, [12, 0]))
                #~ day.append(LittleAction(people,"do nothing", [13, 0]))
                #~ day.append(LittleAction(people,"do nothing", [19, 0]))
                day.append(LittleEatAction( people,[20, 0]))
                #~ day.append(LittleAction(people,"do nothing", [21, 0]))
                day.append(LittleSleepAction( people,[22, 0]))
                self.days.append(day)
                
    def __str__(self):
        s = ""
        for d in self.days:
            s+="day : \n"
            for a in d:
                s+=" "+str(a)
        return s
    
    def findHabits(self, time):
        habits = []
        for d in self.days[:-1]: #not today
            habits.append(self.closestAction(d, time))
            
        return habits
            
    def closestAction(self, day, time):
        #TODO prendre en compte le changement de jour
        index = 0
        diff = 24*60
        
        for a in day:
            adiff = abs((a.startHour[0] - time[0])*60 + (a.startHour[1] - time[1]))
            if adiff < diff:
                diff = adiff
                index +=1
            else:
                break
        #~ print diff
        #~ print index
        return day[index-1]
        
    def addAction(self, a):
        a.init()
        #~ t = utils.globalTime
        #~ a.startHour = [t.hour, t.minute]
        lasta = self.days[-1][-1]
        diff = (a.startHour[0] - lasta.startHour[0])*60 + (a.startHour[1] - lasta.startHour[1])
        if diff < 0:
            #~ print a.startHour
            #~ print lasta.startHour
            
            #~ print utils.globalTime, "new day"
            self.days = self.days[1:]
            self.days.append([])
        self.days[-1].append(a)
                