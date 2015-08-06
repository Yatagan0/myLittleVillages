#! /usr/bin/python
# -*- coding: utf-8 -*-

import random, utils


from LittleBuilding import *
from LittleVillage import *


import xml.etree.ElementTree as ET
from xml.dom import minidom

if __name__ == '__main__':

    newVillage =False
    DO_DISPLAY =False
    
    path = "village.xml"
    
    if newVillage:
        
        village = LittleVillage()
        
        for i in range(0, 1):
            village.addPeople()
        village.money = 0
        #~ mayor = LittlePeople()
        #~ bb = LittleBuilding(pos=[0.,0.])#
        #~ bb = LittleHotel( pos=[0.,0.],owner = mayor)
        #~ b =LittleBuilding(pos=[0.,0.])# 
        #~ b = LittleRestaurant( pos=[0.,1.], owner = mayor)
        #~ print mayor.name
        #~ allPeople.append(mayor)
        
        #~ p1= LittlePeople()
        #~ b = LittleRestaurant( pos=[0.,0.], owner=p1)
        #~ print p1.name
        #~ allPeople.append(p1)

        #~ p2= LittlePeople()
        #~ bbb = LittleField( pos=[0.,0.], owner=p2)
        #~ bbb = LittleRestaurant( pos=[0.,0.], owner=p2)
        #~ print p2.name
        #~ allPeople.append(p2)

        #~ village.people.append(mayor)
        #~ mayor.village = village
        #~ village.people.append(p1)
        #~ p1.village = village
        #~ village.people.append(p2)
        #~ p2.village = village

        
        #~ for i in range(0, 5):
            #~ p = LittlePeople()
            #~ p.knowledge["sleep"].seenBuilding(building=bb)
            #~ p.knowledge["eat"].seenBuilding(building=b)
            #~ print p.name
            #~ allPeople.append(p)
            #~ LittleConstructingBuilding( pos = [0., 0.], owner=p, futureType="LittleField")

        #~ for p in allPeople:
            #~ p.knowledge["sleep"].seenBuilding(building=bb)
            #~ p.knowledge["eat"].seenBuilding(building=b)            

        #~ b = LittleConstructingBuilding( pos = [0., 0.], owner=None, futureType="LittleHotel")
        #~ b = LittleConstructingBuilding( pos = [0., 0.], owner=None, futureType="LittleRestaurant")
        #~ b = LittleConstructingBuilding( pos = [0., 0.], owner=None, futureType="LittleRestaurant")

            
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
    
