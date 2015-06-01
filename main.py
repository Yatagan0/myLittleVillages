#! /usr/bin/python
# -*- coding: utf-8 -*-

import random, utils

from LittlePeople import *
from LittleBuilding import *
from LittleDisplay import *

if __name__ == '__main__':

    
    allPeople = []
    
        
    
    bb = LittleBuilding( [0.,0.],"dortoir")
    b = LittleBuilding( [0.,0.],"cantine")
    
    
    for i in range(0, 1):
        p = LittlePeople()
        p.knowledge["sleep"].seenBuilding(bb)
        p.knowledge["eat"].seenBuilding(b)
        print p.name

        allPeople.append(p)
        
    #~ t = LittleSleepTask([], [])

    
    DO_DISPLAY = True

    counter = 400
    
    while counter > 0:
        counter -= 1
        
        #~ print "------------------"
        utils.globalTime.addTime()
        print utils.globalTime
        for p in allPeople:
            p.update(utils.globalTime)
        if DO_DISPLAY:
            if not display(allPeople):
                counter=0
            
    print allPeople[0].habits
