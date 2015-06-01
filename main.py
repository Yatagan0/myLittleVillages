#! /usr/bin/python
# -*- coding: utf-8 -*-

import random, utils

from LittlePeople import *
from LittleBuilding import *


if __name__ == '__main__':

    
    allPeople = []
    
        
    b = LittleBuilding( [0.,0.],"cantine")
    bb = LittleBuilding( [0.,0.],"dortoir")
    
    
    for i in range(0, 2):
        p = LittlePeople()
        p.knowledge["sleep"].seenBuilding(bb)
        p.knowledge["eat"].seenBuilding(b)
        print p.name

        allPeople.append(p)
        
    #~ t = LittleSleepTask([], [])

    
    

    counter = 40000
    
    while counter > 0:
        counter -= 1
        
        #~ print "------------------"
        utils.globalTime.addTime()
        #~ print utils.globalTime
        for p in allPeople:
            p.update(utils.globalTime)
            
    print allPeople[0].habits
    print "#######"
    print allPeople[1].habits