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
    
    rows2,cols2,channels2 = bg.shape
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
    
    if pixel[0] > 0 and pixel[0]+rows < rows2:
         if pixel[1] > 0 and pixel[1]+cols < cols2:
             try:
                bg[pixel[0]:(pixel[0]+rows), pixel[1]:(cols+pixel[1]) ] = building  
             except Exception, e:
                print "bla ",e
        
        
def printPeople(bg, people, pos):
    pixel = posToPixel(bg, pos)
    rows2,cols2,channels2 = bg.shape

    rows,cols,channels = people.shape
    if pixel[0] > 0 and pixel[0]+rows < rows2:
         if pixel[1] > 0 and pixel[1]+cols < cols2:
             try:
                bg[pixel[0]:(pixel[0]+rows), pixel[1]:(cols+pixel[1]) ] = people 
             except Exception, e:
                print "blu ",e
    
def displayVillage(village):
    bg = cv2.imread('plain_s.jpg')#,cv2.IMREAD_UNCHANGED)
    building  = cv2.imread('building_s.jpg')#,cv2.IMREAD_UNCHANGED)
    people  = cv2.imread('people.jpg')#,cv2.IMREAD_UNCHANGED)
    peopleB  = cv2.imread('peopleB.jpg')
    place  = cv2.imread('field_s.jpg')
    materials  = cv2.imread('materials.jpg')
    woodcutter  = cv2.imread('woodcutter.jpg')
    stonecutter  = cv2.imread('stonecutter.jpg')
    
    for b in village.buildings:
        #~ print "printing ",b.name
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
                if b.name =="stonecutter":
                    printBuilding(bg, stonecutter, b.position)
                elif b.name =="woodcutter":
                    printBuilding(bg, woodcutter, b.position)
                else:
                    printBuilding(bg, building, b.position)
            #~ printBuilding(bg, building, b.position)
    #~ for p in village.places:
        #~ if p.state == "in construction":
            #~ printBuilding(bg, materials, p.position)
        #~ else:
            #~ printBuilding(bg, place, p.position)       
    for p in village.villagers:
        if p.busy :
            printPeople(bg, peopleB, p.position)
        else:
            printPeople(bg, people, p.position)
        
    return bg

#~ printBuilding(bg, building, [50, 100])
#~ printBuilding(bg, people, [150, 200])

lv = LittleVillage()
path = "village.xml"

lv.readVillage(path)

#~ lv.createRandomVillage(10)
#~ lbt = LittleBuildTask(lv, "stonecutter")
#~ lv.toDoList.append(lbt)
#~ lbt = LittleBuildTask(lv, "woodcutter")
#~ lv.toDoList.append(lbt)
#~ lbt = LittleBuildTask(lv, "warehouse")
#~ lv.toDoList.append(lbt)
#~ lbt = LittleBuildTask(lv, "house", position=[0, -1])
#~ lv.toDoList.append(lbt)
#~ lbt = LittleBuildTask(lv, "house", position=[0, -1])
#~ lv.toDoList.append(lbt)
#~ lbt = LittleBuildTask(lv, "house", position=[1, 2])
#~ lv.toDoList.append(lbt)
#~ lbt = LittleBuildTask(lv, "house", position=[1, 2])
#~ lv.toDoList.append(lbt)
#~ lbt = LittleBuildTask(lv, "house", position=[0, -1])
#~ lv.toDoList.append(lbt)
#~ lbt = LittleBuildTask(lv, "house", position=[1, 2])
#~ lv.toDoList.append(lbt)




mustRun = True

while mustRun:
    lv.iterate()
    bg = displayVillage(lv)
    cv2.imshow('image',bg)
    key = cv2.waitKey(33)
    if (key & 255) == 27:
        mustRun = False
    
    
cv2.destroyAllWindows()
print lv
lv.writeVillage(path)
