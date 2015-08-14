#! /usr/bin/python
# -*- coding: utf-8 -*-

import random, utils


from LittleBuilding import *
from LittleVillage import *


import xml.etree.ElementTree as ET
from xml.dom import minidom

if __name__ == '__main__':

    newVillage =False
    DO_DISPLAY =True
    
    path = "village.xml"
    
    if newVillage:
        
        village = LittleVillage()
        
        for i in range(0, 4):
            village.addPeople()
        village.money = 0
        
        for b in allBuildings:
            w=b.workSlots[0]
            #~ for w in b.workSlots:
            while "constructing" in w.types:
                w.types.remove("constructing")

            
    else:
        tree =  ET.parse(path)
        root = tree.getroot()
        village = LittleVillage(root)

    

    counter = 400
    
    while counter > 0:
        counter -= 1
        
        village.update()
        
        #~ print "------------------"
        #~ utils.globalTime.addTime()
        #~ print utils.globalTime
        #~ for p in village.people:
            #~ p.update()
        if DO_DISPLAY:
            from LittleDisplay import *
            if not display(village.people, allBuildings):
                counter=0
            
    root = ET.Element('village')
    utils.globalTime.write(root)
    
    village.write(root)
    
    for b in allBuildings:
        b.write(root)
    
    
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    towrite = reparsed.toprettyxml(indent="  ")
    #print towrite
    file = open(path, "w")
    
    file.write(towrite)
    
    file.close()
    
