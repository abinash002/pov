import time
import argparse
import numpy as np
import scipy as sp
import scipy.ndimage
import Image
import matplotlib.pyplot as plt
from threading import Thread
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
lines=200
radius=37
ny=80
nx=80
result=[[[]]]
def main(coords):
    img = Image.open('a.png')
    width, height = img.size
    img = img.resize((80,80))
    im = img.convert('RGB')
    data = np.array(im)
    bands = []
    for band in data.T:
        zi = sp.ndimage.map_coordinates(band, coords, order=1)
        bands.append(zi.reshape((lines,radius)))
        arry=zi
    output = np.dstack(bands)
    plt.imsave("b.jpg",output)
    return output 
def index_coords():
    origin_x, origin_y = nx // 2, ny // 2
    x, y = np.meshgrid(np.arange(80), np.arange(80))
    x -= 40
    y -= 40
    return x, y
def cart2polar(x, y):
    r = np.sqrt(x**2 + y**2)
    r = r % 40
    theta = np.arctan2(y, x)
    print(theta.max())
    return r, theta 
def polar2cart(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y
def reproject_image_into_polar():
    origin = (nx//2, ny//2) 
    x, y = index_coords()
    r, theta = cart2polar(x, y)
    r_i = np.linspace(r.min(), r.max(),radius)
    theta_i = np.linspace(theta.min(), theta.max(),lines)
    r_grid ,theta_grid= np.meshgrid( r_i[::-1],theta_i)
    xi, yi = polar2cart(r_grid, theta_grid)
    xi += origin[0]  
    yi += origin[1] 
    xi, yi = xi.flatten(), yi.flatten()
    coords = np.vstack((xi, yi)) 
    return coords
if __name__ == '__main__':
    coord=reproject_image_into_polar()
    result=coord
    
            
            
            
            
            
            



