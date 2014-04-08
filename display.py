import numpy as np
import cv2

# Load an color image in grayscale
bg = cv2.imread('plain.jpg')#,cv2.IMREAD_UNCHANGED)
building  = cv2.imread('building.jpg')#,cv2.IMREAD_UNCHANGED)

def posToPixel(pos):
    return pos
    
def pixelToPos(pixel):
    return pixel

def printBuilding(bg, building, pos):
    pixel = pixelToPos(pos)
    
 
    rows,cols,channels = building.shape
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
        

printBuilding(bg, building, [50, 100])

#~ Mat a; //5x7
#~ Mat big; //100x100

#~ // ...your code

#~ building.copyTo(bg.colRange(51,150).rowRange.(63,63+63-1));
#~ roi = cv2.rect()
#~ cv::Rect roi( cv::Point( originX, originY ), smallImage.size() );
#~ smallImage.copyTo( bigImage( roi ) );


#~ bg =cv2.add(bg,building)

cv2.imshow('image',bg)
cv2.waitKey(0)
cv2.destroyAllWindows()