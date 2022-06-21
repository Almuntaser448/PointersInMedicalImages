from math import pi,  sin, sqrt
import matplotlib.pyplot as plt
import numpy as np


def centroid(img,interest=255):
    #interest:la couleur de la CC

    nbx=0 #la somme des positions en abscisse des pixels interessants
    nby=0
    nbPixel=0


    for i in range(len(img)):
        for j in range(len(img[0])):
            if (img[i,j])==interest:
                nbx+=i
                nby+=j
                nbPixel+=1

    moy=(int(nbx/nbPixel),int(nby/nbPixel))
    return moy

def maxRad(img,center):
    
    x,y,xc,yc,maxrad=0,0,0,0,0
    objective=np.max(img)
    moy=centroid(img)
    for i in range (len(img)):
        for j in range (len(img[0])):
            if img[i,j]==objective:
                x,y = i,j
                xc,yc = moy[0],moy[1]
                sq = (sqrt((x-xc)**2 + (y-yc)**2))
                if maxrad < sq:
                    maxrad = sq

    return maxrad

def polarFourier(img, maxRadFreq, maxAngleFreq):
       
    ctr=centroid(img)
    ctr=(int(ctr[0]),int(ctr[1]))
   
    maxrad=int(maxRad(img,ctr))
    
    FR=np.zeros((maxRadFreq, maxAngleFreq),dtype="float64")
    FI=np.zeros((maxRadFreq, maxAngleFreq),dtype="float64")
    
    for rad in range(maxRadFreq):
        for ang in range(maxAngleFreq):
            for x in range(0, len(img)):
                for y in range(0, len(img[1])):
                    
                    radius = np.sqrt( (x-ctr[0])**2 + (y-ctr[1])**2)
                    theta = np.arctan2((y-ctr[0]),(x-ctr[1]))
                    
                    if theta<0:
                        theta+=2*pi
                    if img[x,y]!=0:
                        FR[rad,ang] += img[x,y]*np.cos(2*pi*rad*(radius/maxrad) + ang*theta)
                        FI[rad,ang] -= img[x,y]*np.sin(2*pi*rad*(radius/maxrad) + ang*theta)
                        
    return (FR, FI)



def GFD(FR,FI,maxrad):
    DC=0
    GFD=np.zeros((len(FR[0])*len(FR)))
    for rad in range(0, len(FR)):
        for ang in range(0, len(FR[0])):
            if (rad==0 and ang==0):
                DC=sqrt(FR[0,0]**2 +FI[0,0]**2)
                GFD[0]=DC/(pi*maxrad**2)
            else:
                GFD[rad*len(FR[0])+ang]=sqrt((FR[rad,ang]**2)+(FI[rad,ang]**2))/DC
    return GFD

def computeGFD(imgPath): 
    img=plt.imread(imgPath)
    FR,FI=polarFourier(img,4,9)
    return list(GFD(FR,FI,maxRad(img,centroid(img))))
    