from PIL import Image
import os.path
import sys
import os
import argparse

def main():
    try:
         #Relative Path
        img = Image.open("aaa.png")
        width, height = img.size
  
        img = img.resize((80,80))
         
        #Saved in the same relative location
        img.save("a.png") 
    except IOError:
        pass
 
if __name__ == "__main__":
    main()
