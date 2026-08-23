#!/usr/bin/env python3

# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import random
import os
import time
import math
from multi_ws281x import mPixelStrip, mRGBW
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
        print('Args: ', C1_GPIO, C2_GPIO, C1_LEN, C2_LEN)
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
                c = mRGBW(r,g,b)
                if (led < self.C1_LEN):
                    self.strip.setPixelColor(0, led, c)
                else:
                    self.strip.setPixelColor(1, led-self.C1_LEN, c)

            self.strip.show()
            frameCount += 1
            print("[", self.name, "] Frame ", frame, ", FPS: ", (frameCount / now) if now > 0.5 else 0, " DeltaT: ", (time.time() - startTimeSeconds) - (frame / fps))

            now = time.time() - startTimeSeconds


    def setAll(self, color):
        for i in range(self.C1_LEN):
            self.strip.setPixelColor(0, i, color)
        for i in range(self.C2_LEN):
            self.strip.setPixelColor(1, i, color)


    def set(self, ch, led, color):
        self.strip.setPixelColor(ch, led, color)

    def christmasLight(self):
        for i in range(self.C1_LEN):
            self.set(0, i, mRGBW(27, 14, 4) if random.random() > 0.8 else mRGBW(0,0,0))
        for i in range(self.C2_LEN):
            self.set(1, i, mRGBW(27, 14, 4) if random.random() > 0.8 else mRGBW(0,0,0))
        self.strip.show()


    def show(self):
        self.strip.show()
