#! /usr/bin/python
# -*- coding: utf-8 -*-

import random, utils

from LittlePeople import *
from LittleBuilding import *


import xml.etree.ElementTree as ET
from xml.dom import minidom

if __name__ == '__main__':

    newVillage =True
    DO_DISPLAY =False
    
    allPeople = []
    path = "village.xml"
    
    if newVillage:

        mayor = LittlePeople()
        bb = LittleBuilding(pos=[0.,0.])#
        bb = LittleHotel( pos=[0.,0.],owner = mayor)
        b =LittleBuilding(pos=[0.,0.])# LittleRestaurant( pos=[0.,0.], owner = mayor)
        print mayor.name
        allPeople.append(mayor)
        
        #~ p1= LittlePeople()
        #~ bbb = LittleRestaurant( pos=[0.,0.], owner=p1)
        #~ print p1.name
        #~ allPeople.append(p1)

        #~ p2= LittlePeople()
        #~ bbb = LittleRestaurant( pos=[0.,0.], owner=p2)
        #~ print p1.name
        #~ allPeople.append(p2)


        
        #~ for i in range(0, 5):
            #~ p = LittlePeople()
            #~ p.knowledge["sleep"].seenBuilding(building=bb)
            #~ p.knowledge["eat"].seenBuilding(building=b)
            #~ print p.name
            #~ allPeople.append(p)
            #~ LittleConstructingBuilding( pos = [0., 0.], owner=p, futureType="LittleField")

        for p in allPeople:
            p.knowledge["sleep"].seenBuilding(building=bb)
            p.knowledge["eat"].seenBuilding(building=b)            

        #~ b = LittleConstructingBuilding( pos = [0., 0.], owner=None, futureType="LittleHotel")
        #~ b = LittleConstructingBuilding( pos = [0., 0.], owner=None, futureType="LittleRestaurant")
        #~ b = LittleConstructingBuilding( pos = [0., 0.], owner=None, futureType="LittleRestaurant")

            
    else:
        tree =  ET.parse(path)
        root = tree.getroot()
        for child in root:
            if (child.tag == "time"):
                utils.globalTime.read(child)
            elif (child.tag == "people"):
                p=LittlePeople(child)
                allPeople.append(p)
            elif child.tag == "building":
                b = readBuilding(child)

    #~ b = LittleConstructingBuilding( pos = [0., 0.], owner=None, futureType="LittleHotel")
    

    counter = 400
    
    while counter > 0:
        counter -= 1
        
        #~ print "------------------"
        utils.globalTime.addTime()
        print utils.globalTime
        for p in allPeople:
            p.update()
        if DO_DISPLAY:
            from LittleDisplay import *
            if not display(allPeople, allBuildings):
                counter=0
            
    #~ print allPeople[0].habits
    
#~ lv.writeVillage(path)
    root = ET.Element('village')
    utils.globalTime.write(root)
    
    for p in allPeople:
        p.write(root)
        
    for b in allBuildings:
        print b.type
        b.write(root)
    
    
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    towrite = reparsed.toprettyxml(indent="  ")
    #print towrite
    file = open(path, "w")
    
    file.write(towrite)
    
    file.close()
    
