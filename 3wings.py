 
import time
from neopixel import *
import argparse
import numpy as np
import scipy as sp
import scipy.ndimage
import os
from PIL import Image

import matplotlib.pyplot as plt
# LED strip configuration:
LED_COUNT      = 24      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
lines=210
radius=37
size = 130, 130


            

def main():
    my_file = os.path.isfile("b.png")
    if my_file:
                im = Image.open('b.png')
                return im 
    im = Image.open('bb.png')
    im = im.resize(size, Image.ANTIALIAS)

    im = im.convert('RGB')
    data = np.array(im)

    result=plot_polar_image(data, origin=None)
    

    return result

def plot_polar_image(data, origin=None):
    """Plots an image reprojected into polar coordinages with the origin
    at "origin" (a tuple of (x0, y0), defaults to the center of the image)"""
    polar_grid = reproject_image_into_polar(data, origin)
    a,b,c=np.split( polar_grid, 3)
    x=np.append(np.append(b,c,axis=0),a,axis=0)
    y=np.append(np.append(c,a,axis=0),b,axis=0)
    c = np.concatenate((polar_grid,np.concatenate((x, y), axis=1)),axis=1)
    print(c.shape)
    print(x.shape)
    print(polar_grid.shape)
    plt.imsave("b.png",c)
    return polar_grid
   
   
def index_coords(data, origin=None):
    """Creates x & y coords for the indicies in a numpy array "data".
    "origin" defaults to the center of the image. Specify origin=(0,0)
    to set the origin to the lower left corner of the image."""
    ny, nx = data.shape[:2]
    
    if origin is None:
        origin_x, origin_y = nx // 2, ny // 2
    else:
        origin_x, origin_y = origin
    x, y = np.meshgrid(np.arange(120), np.arange(120))
    x -= 60
    y -= 60
    return x, y

def cart2polar(x, y):
    r = np.sqrt(x**2 + y**2)
    
    r = r % 60
    
    theta = np.arctan2(y, x)
    print(theta.max())
    return r, theta
    
def polar2cart(r, theta):
    
    x = r * np.cos(theta)
    
    y = r * np.sin(theta)
    return x, y
    

def reproject_image_into_polar(data, origin=None):

    ny, nx = data.shape[:2]
    if origin is None:
        origin = (nx//2, ny//2)
   
    x, y = index_coords(data, origin=origin)
    r, theta = cart2polar(x, y)

    # Make a regular (in polar space) grid based on the min and max r & theta
    r_i = np.linspace(r.min(), r.max(),radius)
    theta_i = np.linspace(theta.min(), theta.max(),lines)
 
           
    r_grid ,theta_grid= np.meshgrid( r_i[::-1],theta_i)
    
    # Project the r and theta grid back into pixel coordinates
    xi, yi = polar2cart(r_grid, theta_grid)
    xi += origin[0] # We need to shift the origin back to 
    yi += origin[1] # back to the lower-left corner...
   
    xi, yi = xi.flatten(), yi.flatten()
    coords = np.vstack((xi, yi)) # (map_coordinates requires a 2xn array)
    # Reproject each band individually and the restack
    # (uses less memory than reprojection the 3-dimensional array in one step)
   
    bands = []
    for band in data.T:
        zi = sp.ndimage.map_coordinates(band, coords, order=1)
        bands.append(zi.reshape((lines,radius)))
        arry=zi
    output = np.dstack(bands)
  
    return output
 
# Define functions which animate LEDs in various ways.
def colorWipe(strip, Data, wait_ms=50):
     while 1:
       print ('Starting............')
       for i in range(lines):
         for j in range(23):
            a=Color(Data[i][j][0],Data[i][j][1],Data[i][j][2])
            c=np.asscalar(a)           
            strip.setPixelColor(j,c)
         strip.show()
       print ('Round............')    

 

# Main program logic follows:
if __name__ == '__main__':
    Data=main()
    # Process arguments
'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
 
     # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
 
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
  
    try:
 
        while True:
            colorWipe(strip,Data,0)  # Red wipe
           
 
    except KeyboardInterrupt:
        if args.clear:
           colorWipe(strip, Color(0,0,0), 10)
            
            
            '''
            
            
            
            
            
            
            
            
            



