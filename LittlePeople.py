import utils, random, copy

from LittleAction import *
from LittleBuilding import *


class LittlePeople:
    def __init__(self):
        self.name = utils.randomName()
        
        self.pos = [0.0, 0.0]
        self.speed = 0.04
        
        self.habits = LittleOldActions(self,)
        self.action = None
        
        self.tired = -5*60
        self.hungry = 0

        self.knowledge = {}
        self.knowledge["sleep"] = LittleBuildingList()
        self.knowledge["eat"] = LittleBuildingList()

   
    def update(self, time):
        self.tired+=1
        self.hungry +=1
        
        if self.action is not None:
            if not self.action.execute():
                self.habits.addAction(self.action)
                self.action = None
            return
        
        if self.tired > 20*60:
            #~ print "must sleep"
            self.action = LittleSleepAction( self,[time.hour, time.minute])
            return
        
        if self.hungry > 10*60:
            #~ print "must eat"
            self.action = LittleEatAction( self,[time.hour, time.minute]) 
            return
        
        myHabits = self.habits.findHabits([time.hour, time.minute])
        #~ myHabits = [LittleAction(self, "do nothing", [time.hour, time.minute])]
        
        r = random.randint(0, 9)
        if r < 9:
            a = random.choice(myHabits)
            
            if self.canDoAction(a):
                self.action = a.copy()
                return

        self.action = LittleAction(self, "do nothing", [time.hour, time.minute])


    def canDoAction(self, a):
        if a.type == "sleep" and self.tired < 5*60:
            return False
        if a.type == "eat" and self.hungry < 3*60:
            return False
        return True
      
    def go(self, pos):
        #~ print self.name, " ", self.pos
        d = utils.distance(self.pos,pos)

        if d < self.speed:
            self.pos[0] = pos[0]
            self.pos[1] = pos[1]
            return True
        else:
            self.pos[0] += self.speed*(pos[0] - self.pos[0])/d
            self.pos[1] += self.speed*(pos[1] - self.pos[1])/d
            return False