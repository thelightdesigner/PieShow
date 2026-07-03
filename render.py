#!/usr/bin/env python3

# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import os
import time
import math
from multi_ws281x import mPixelStrip, mColor
from PIL import Image
import argparse

class LEDTape:
    
    def __init__(self, lightID, name, C1_GPIO, C2_GPIO, C1_LEN, C2_LEN):
        self.lightID = lightID
        self.name = name
        self.C1_GPIO = C1_GPIO
        self.C2_GPIO = C2_GPIO
        self.C1_LEN = C1_LEN
        self.C2_LEN = C2_LEN
        self.strip = mPixelStrip(C1_GPIO, C2_GPIO, C1_LEN, C2_LEN)
        self.strip.begin()

    def renderPieShowFile(self, img, fps):
        pixels = img.load()
        width, height = img.size
        
        print('Pixel Count: ',width)
        print('Frames: ', height)
        print('FPS: ', fps)
        
        durationSeconds = height/fps

        startTimeSeconds = time.time()
        now = time.time() - startTimeSeconds
        frameCount = 0

        while (now <= durationSeconds):
            frame = max(0, math.floor(now * fps))
            
            for led in range(width):
                (r,g,b) = pixels[led,frame]
                self.strip.setPixelColor(0, led, mColor(r,g,b))

            self.strip.show()
            frameCount += 1
            print("[", self.name, "] Frame ", frame, ", FPS: ", (frameCount / now) if now > 0.5 else 0, " Skipped: ", frame - frameCount)

            now = time.time() - startTimeSeconds


    def setAll(self, color):
        for ch in range(2):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(ch, i, color)

    def show(self):
        self.strip.show()
