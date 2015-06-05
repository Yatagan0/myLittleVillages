#! /usr/bin/python
# -*- coding: utf-8 -*-

import random, utils

from LittlePeople import *
from LittleBuilding import *
from LittleDisplay import *

import xml.etree.ElementTree as ET
from xml.dom import minidom

if __name__ == '__main__':


    path = "village.xml"

    #~ lv.readVillage(path)
    
    allPeople = []
    
        
    
    bb = LittleBuilding( [0.,0.],"dortoir")
    b = LittleBuilding( [0.,0.],"cantine")
    
    
    for i in range(0, 3):
        p = LittlePeople()
        p.knowledge["sleep"].seenBuilding(bb)
        p.knowledge["eat"].seenBuilding(b)
        print p.name

        allPeople.append(p)
        
    #~ t = LittleSleepTask([], [])

    
    DO_DISPLAY = True

    counter = 4000
    
    while counter > 0:
        counter -= 1
        
        #~ print "------------------"
        utils.globalTime.addTime()
        print utils.globalTime
        for p in allPeople:
            p.update(utils.globalTime)
        if DO_DISPLAY:
            if not display(allPeople, allBuildings):
                counter=0
            
    print allPeople[0].habits
    
#~ lv.writeVillage(path)
    root = ET.Element('village')
    
    
    
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    towrite = reparsed.toprettyxml(indent="  ")
    #print towrite
    file = open(path, "w")
    
    file.write(towrite)
    
    file.close()