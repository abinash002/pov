import numpy as np
import scipy as sp
import scipy.ndimage

import Image

import matplotlib.pyplot as plt
lines=200
radius=60
def main():
    im = Image.open('bb.jpg')
    im = im.convert('RGB')
    data = np.array(im)

    plot_polar_image(data, origin=None)
    

    plt.show()

def plot_polar_image(data, origin=None):
    """Plots an image reprojected into polar coordinages with the origin
    at "origin" (a tuple of (x0, y0), defaults to the center of the image)"""
    polar_grid = reproject_image_into_polar(data, origin)
    plt.imsave("a.jpg",polar_grid)
   
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
    theta_grid, r_grid = np.meshgrid(theta_i, r_i)
    print(r_i)
    # Project the r and theta grid back into pixel coordinates
    xi, yi = polar2cart(r_grid, theta_grid)
    xi += origin[0] # We need to shift the origin back to 
    yi += origin[1] # back to the lower-left corner...
    se=0
    sett=lines//2
    t=[]
    xii=[]
    yii=[]
    for i in range (0,lines):
         if(i%2==0): 
             t.append(se)
             se=se+1
         else:
             t.append(sett)
             sett=sett+1 
    
                
    xi, yi = xi.flatten(), yi.flatten()
    
    coords = np.vstack((xi, yi)) # (map_coordinates requires a 2xn array)
    # Reproject each band individually and the restack
    # (uses less memory than reprojection the 3-dimensional array in one step)
   
    bands = []
    for band in data.T:
        zi = sp.ndimage.map_coordinates(band, coords, order=1)
        bands.append(zi.reshape((radius,lines)))
        arry=zi
    output = np.dstack(bands)
  
    return output

if __name__ == '__main__':
    main()
