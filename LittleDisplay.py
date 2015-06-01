import numpy as np
import cv2

minx = -10.
maxx =10.
miny = -10.
maxy = 10.

global bg
bg = cv2.imread('plain1.png')

[h, w, c] = bg.shape
toDisplayHeight = h/(maxy - miny)
toDisplayWidth= w/(maxx - minx)

def posToPixel(img, pos):
    rows,cols,channels = img.shape
    
    pixelx = int((-pos[1] - miny)*rows/(maxy - miny))
    pixely =int((pos[0] - minx)*cols/(maxx - minx) )
    return [pixelx, pixely]
    
    
def display():
    cv2.imshow('LittleDispay',bg)
    key = cv2.waitKey(33)
    return key == -1
    
def killDisplay():
    cv2.destroyAllWindows()
    
        
if __name__ == '__main__':

    
    
    display()
    cv2.waitKey()
    killDisplay()