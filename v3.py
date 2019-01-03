# Uses Python 2.5.2 !

import Image
import math
import sys

# Name of your png image
name = 'l'
im = Image.open(name + '.jpg')

im_pix = im.load()

h = im.size[1]
w = im.size[0]
k = (w-1)/2.0

# Resolution of the angle
thetares = 3
# Number of leds
Nleds = 60

# Create empty matrix of the right dimension
M = [[''] * Nleds]
for l in range(0,360/3 - 1,1):
    M.append([''] * Nleds)

if w != Nleds*2 or h!= Nleds*2:
    sys.exit('Please choose an 120x120 pixels image')



# First loop
j = -1

for theta in range(0,360,thetares):
    j = j + 1
    i = w/4
    if (j<360/(thetares*2)):
        for r in range(0,Nleds,2):
            rprime = r+0.5
            thetaprime = (theta/360.0)*(2.0*math.pi)
            xprime = rprime*math.cos(thetaprime)
            yprime = rprime*math.sin(thetaprime)
            x = xprime + k
            y = (-1)*(yprime - k)
            xint = round(x)
            yint = round (y)
            
            jcorr = j
            icorr = i
        
            r = im_pix[xint,yint][0]
            g = im_pix[xint,yint][1]
            b = im_pix[xint,yint][2]
        
            rcorr = (int) (math.floor(r/32.0)) << 5
            gcorr = (int) (math.floor(g/32.0)) << 2
            bcorr = (int) (math.floor(b/64.0))

            rgb = rcorr+gcorr+bcorr

            if rgb == 255:
                rgb = 0
            
        
            M[jcorr][icorr] = rgb

            i = i + 1

    else:
        for r in range(1,Nleds,2):
            rprime = r+0.5
            thetaprime = (theta/360.0)*(2.0*math.pi)
            xprime = rprime*math.cos(thetaprime)
            yprime = rprime*math.sin(thetaprime)
            x = xprime + k
            y = (-1)*(yprime - k)
            xint = round(x)
            yint = round (y)
        
            jcorr = j - 360/(thetares*2)
            icorr = -i + Nleds - 1
        
            r = im_pix[xint,yint][0]
            g = im_pix[xint,yint][1]
            b = im_pix[xint,yint][2]
        
            rcorr = (int) (math.floor(r/32.0)) << 5
            gcorr = (int) (math.floor(g/32.0)) << 2
            bcorr = (int) (math.floor(b/64.0))

            rgb = rcorr+gcorr+bcorr

            if rgb == 255:
                rgb = 0
            
        
            M[jcorr][icorr] = rgb

            i = i + 1


# Second loop
j = -1

for theta in range(0,360,thetares):
    j = j + 1
    i = w/4
    if (j<360/(thetares*2)):
        for r in range(1,Nleds,2):
            rprime = r+0.5
            thetaprime = (theta/360.0)*(2.0*math.pi)
            xprime = rprime*math.cos(thetaprime)
            yprime = rprime*math.sin(thetaprime)
            x = xprime + k
            y = (-1)*(yprime - k)
            xint = round(x)
            yint = round (y)
            
            jcorr = j+360/(thetares*2)
            icorr = i
        
            r = im_pix[xint,yint][0]
            g = im_pix[xint,yint][1]
            b = im_pix[xint,yint][2]
        
            rcorr = (int) (math.floor(r/32.0)) << 5
            gcorr = (int) (math.floor(g/32.0)) << 2
            bcorr = (int) (math.floor(b/64.0))

            rgb = rcorr+gcorr+bcorr

            if rgb == 255:
                rgb = 0
            
        
            M[jcorr][icorr] = rgb

            i = i + 1

    else:
        for r in range(0,Nleds,2):
            rprime = r+0.5
            thetaprime = (theta/360.0)*(2.0*math.pi)
            xprime = rprime*math.cos(thetaprime)
            yprime = rprime*math.sin(thetaprime)
            x = xprime + k
            y = (-1)*(yprime - k)
            xint = round(x)
            yint = round (y)
        
            jcorr = j
            icorr = -i + Nleds - 1

            r = im_pix[xint,yint][0]
            g = im_pix[xint,yint][1]
            b = im_pix[xint,yint][2]

            rcorr = (int) (math.floor(r/32.0)) << 5
            gcorr = (int) (math.floor(g/32.0)) << 2
            bcorr = (int) (math.floor(b/64.0))

            rgb = rcorr+gcorr+bcorr

            if rgb == 255:
                rgb = 0
            
        
            M[jcorr][icorr] = rgb

            i = i + 1





# Write to text file

f = open(name + '.txt', 'w')
f.write('const uint8_t ledList [numberOfPositions][numberOfLeds] PROGMEM = {')

for l in range(len(M)):
    if l != 0:
        f.write(',')
    f.write('{')
    for m in range(len(M[0])):
        f.write(str(M[l][m]))
        if m != len(M[0])-1:
            f.write(',')
        if m == len(M[0])-1:
            f.write('}')

f.write('};')
f.close()

print('Succes!')


