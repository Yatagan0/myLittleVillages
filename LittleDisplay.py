import numpy as np
import cv2

minx = -10.
maxx =10.
miny = -10.
maxy = 10.

global bg
#~ bg = cv2.imread('plain1.png')

WIDTH = 700
HEIGHT=700
bg = np.zeros((HEIGHT,WIDTH,3), np.uint8)
bg[:, :] = (255, 255, 255)


[h, w, c] = bg.shape
toDisplayHeight = h/(maxy - miny)
toDisplayWidth= w/(maxx - minx)

def posToPixel(img, pos):
    rows,cols,channels = img.shape
    
    pixelx = int((-pos[1] - miny)*rows/(maxy - miny))
    pixely =int((pos[0] - minx)*cols/(maxx - minx) )
    return [pixelx, pixely]
    
allImages = {}
allImages["default"] =  np.zeros((toDisplayHeight ,toDisplayWidth,3), np.uint8)




def addInAllImages(name, path, ratio=1.):
    img = cv2.imread(path)
    #~ print img
    allImages[name] = np.zeros((ratio*toDisplayHeight,ratio*toDisplayWidth,3), np.uint8)
    
    cv2.cv.Resize(cv2.cv.fromarray(img), cv2.cv.fromarray(allImages[name] )) 

addInAllImages("people", "img/people.jpg", ratio=0.5)
addInAllImages("building", "img/building.jpg")
addInAllImages("field", "img/field.jpg")
addInAllImages("hotel", "img/hotel.jpg")
addInAllImages("restaurant", "img/restaurant.jpg")
 
class displayTree:
    def __init__(self, image="default"):
        self.image = allImages[image]
        self.children = {}
        #~ self.bg = bg
        
    def addChild(self, name, tree):
        self.children[name] = tree
        
    #~ def setImage(self, im):
        #~ self.image = np.zeros((toDisplayHeight,toDisplayWidth,3), np.uint8)

        #~ cv2.cv.Resize(cv2.cv.fromarray(im), cv2.cv.fromarray(self.image))
        #self.image = im
        
    def display(self, name, pos):
        name = name.split('-', 1)
        
        childName = name[0]
        fullChildName = ""
        if len(name) > 1:
            fullChildName = name[1]
        if childName in self.children.keys():
            self.children[childName].display( fullChildName, pos)
            return
        #~ name = name.split('/', 2)
        #~ print name
        #~ if(len(name) > 1):
            #~ childName = name[1]
            #~ fullChildName = name[1]
            #~ if len(name) > 2:
                #~ fullChildName = name[1] + name[2]
            #~ if childName in self.children.keys():
                #~ self.children[childName].display( fullChildName, pos)
                #~ return
            
        if self.image is not None:
            global bg
            pixel = posToPixel(bg, pos)
            rows,cols,channels = self.image.shape
            
            rows2,cols2,channels2 = bg.shape
            if pixel[0] > 0 and pixel[0]+rows < rows2:
                if pixel[1] > 0 and pixel[1]+cols < cols2:
                    try:
                        bg[pixel[0]:(pixel[0]+rows), pixel[1]:(cols+pixel[1]) ] = self.image 
                    except Exception, e:
                        print "bla ",e
            return

        print "WARNING, no child named ",name," and not image attributed !" 
   
DT = displayTree()
DT_people = displayTree("people")
DT.addChild("people", DT_people)
DT_building = displayTree("building")
DT_field = displayTree("field")
DT_building.addChild("field", DT_field)
DT_hotel = displayTree("hotel")
DT_building.addChild("hotel", DT_hotel)
DT_restaurant = displayTree("restaurant")
DT_building.addChild("restaurant", DT_restaurant)
DT.addChild("building", DT_building)
    
def display(people, buildings):
    clear()
    for b in buildings:
        DT.display("building-"+b.type, b.pos)
    for pp in people:
        DT.display("people", pp.pos)
    cv2.imshow('LittleDispay',bg)
    key = cv2.waitKey(33)
    return key == -1
    
def clear():
    bg = np.zeros((HEIGHT,WIDTH,3), np.uint8)
    bg[:, :] = (255, 255, 255)
    
def killDisplay():
    cv2.destroyAllWindows()
    
        
if __name__ == '__main__':

    
    
    display()
    cv2.waitKey()
    killDisplay()