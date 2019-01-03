import time
import argparse
import numpy as np
import scipy as sp
import scipy.ndimage
import Image
import matplotlib.pyplot as plt
from threading import Thread
import socket
from SocketServer import ThreadingMixIn
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1'importerror no module named for GPIOs 13, 19, 41, 45 or 53
lines=200
radius=37
ny=80
nx=80
Coord=[[[]]]
TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024
Array=[[[]]]
class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print " New thread started for "+ip+":"+str(port)

    def run(self):
      with open('a.png', 'wb') as f:
        print 'file opened'
        while True:
          #print('receiving data...')
          data = self.sock.recv(BUFFER_SIZE)
          if not data:
            f.close()
            print 'file close()'
            break
            # write data to a file
          f.write(data)
      print('Successfully get the file')
      print(main())
      return 
def main():
    img = Image.open('a.png')
    width, height = img.size
    img = img.resize((80,80))
    im = img.convert('RGB')
    data = np.array(im)
    bands = []
    for band in data.T:
        zi = sp.ndimage.map_coordinates(band, Coord, order=1)
        bands.append(zi.reshape((lines,radius)))
        arry=zi
    output = np.dstack(bands)
    for i in range(lines):
       for j in range(37):
           Array[i][j]=Color(output[i][j][0],output[i][j][1],output[i][j][2])
                                                                                                                                                                                                                                                    
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
def recieve():
 threads = []
  try:
    while True:
        print "Waiting for incoming connections..."
        tcpsock.listen(5)
        
        (conn, (ip,port)) = tcpsock.accept()
        print 'Got connection from ', (ip,port)
        newthread = ClientThread(ip,port,conn)
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join()

  except KeyboardInterrupt:
       exit()
def colorWipe(strip, Data, wait_ms=50):
    """Wipe color across display a pixel at a time."""
   print ('Starting............')
   for i in range(lines):
       for j in range(strip.numPixels()):
           strip.setPixelColor(j,Array[i][j])
       strip.show()
   print ('Round............')         
if __name__ == '__main__':
    Coord=reproject_image_into_polar()
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((TCP_IP, TCP_PORT)) 
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    Thread(target = recieve).start()
    Thread(target = colorWipe).start()
    
   
    
            
            
            
            
            
            



