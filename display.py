import numpy as np
import cv2

from LittleVillage import *
# Load an color image in grayscale


minx = -10.
maxx =10.
miny = -10.
maxy = 10.


def posToPixel(img, pos):
    rows,cols,channels = img.shape
    
    pixelx =int( (pos[0] - minx)*cols/(maxx - minx))
    pixely =int( (pos[1] - miny)*rows/(maxy - miny))
    return [pixelx, pixely]
    
def pixelToPos(img, pixel):
    return pixel

def printBuilding(bg, building, pos):
    pixel = posToPixel(bg, pos)
    
 
    rows,cols,channels = building.shape
    #http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_core/py_image_arithmetics/py_image_arithmetics.html#image-arithmetics
    #~ roi = bg[pixel[0]:(pixel[0]+rows), pixel[1]:(cols+pixel[1]) ]
    # Now create a mask of logo and create its inverse mask also
    #~ img2gray = cv2.cvtColor(building,cv2.COLOR_BGR2GRAY)
    #~ ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    #~ mask_inv = cv2.bitwise_not(mask)
    #~ # Now black-out the area of logo in ROI
    #~ img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

    #~ # Take only region of logo from logo image.
    #~ img2_fg = cv2.bitwise_and(building,building,mask = mask)

    # Put logo in ROI and modify the main image
    #~ dst = cv2.add(img1_bg,img2_fg)
    #~ dst = cv2.add(roi, building)
    bg[pixel[0]:(pixel[0]+rows), pixel[1]:(cols+pixel[1]) ] = building  
        
        
def printPeople(bg, people, pos):
    pixel = posToPixel(bg, pos)
    

    rows,cols,channels = people.shape
    bg[pixel[0]:(pixel[0]+rows), pixel[1]:(cols+pixel[1]) ] = people 
    
def displayVillage(village):
    bg = cv2.imread('plain_s.jpg')#,cv2.IMREAD_UNCHANGED)
    building  = cv2.imread('building_s.jpg')#,cv2.IMREAD_UNCHANGED)
    people  = cv2.imread('people.jpg')#,cv2.IMREAD_UNCHANGED)
    place  = cv2.imread('field_s.jpg')
    materials  = cv2.imread('materials.jpg')
    
    for b in village.buildings:
        if b.state == "in construction":
            printBuilding(bg, materials, b.position)
        else:
            if b.type == "storage":
                printBuilding(bg, place, b.position)
            elif b.type == "house":
                printBuilding(bg, building, b.position)
            elif b.type == "field":
                printBuilding(bg, place, b.position)
            elif b.type == "production":
                printBuilding(bg, building, b.position)
            #~ printBuilding(bg, building, b.position)
    #~ for p in village.places:
        #~ if p.state == "in construction":
            #~ printBuilding(bg, materials, p.position)
        #~ else:
            #~ printBuilding(bg, place, p.position)       
    for p in village.villagers:
        printPeople(bg, people, p.position)
        
    return bg

#~ printBuilding(bg, building, [50, 100])
#~ printBuilding(bg, people, [150, 200])

lv = LittleVillage()

#~ lbt = LittleBuildTask(lv, "warehouse")
#~ lv.toDoList.append(lbt)
lbt = LittleBuildTask(lv, "stonecutter")
lv.toDoList.append(lbt)
#~ lbt = LittleBuildTask(lv, "warehouse")
#~ lv.toDoList.append(lbt)
#~ lbt = LittleBuildTask(lv, "house")
#~ lv.toDoList.append(lbt)
#~ lbt = LittleBuildTask(lv, "house")
#~ lv.toDoList.append(lbt)
#~ lbt = LittleBuildTask(lv, "house")
#~ lv.toDoList.append(lbt)
#~ lbt = LittleBuildTask(lv, "house")
#~ lv.toDoList.append(lbt)
#~ lbt = LittleBuildTask(lv, "field")
#~ lv.toDoList.append(lbt)

lv.createRandomVillage(10)
path = "village.xml"
lv.readVillage(path)



mustRun = True

while mustRun:
    lv.iterate()
    bg = displayVillage(lv)
    cv2.imshow('image',bg)
    key = cv2.waitKey(33)
    if key == 27:
        mustRun = False
    
    
cv2.destroyAllWindows()
print lv
lv.writeVillage(path)
