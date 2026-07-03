#!/usr/bin/env python3

# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import os
import time
import math
from rpi_ws281x import PixelStrip, Color
from PIL import Image
import argparse

class LEDTape:
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10          # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
    
    def __init__(self, lightID, DMAChannel, GPIO, pixelCount, name):
        self.lightID = lightID
        self.name = name
        self.GPIO = GPIO
        self.pixelCount = pixelCount
        self.DMAChannel = DMAChannel
        self.strip = PixelStrip(self.pixelCount, self.GPIO, self.LED_FREQ_HZ, DMAChannel, self.LED_INVERT, self.LED_BRIGHTNESS, self.DMAChannel)
        self.strip.begin()

    def renderPieShowFile(self, img, fps, sysstarttime, lock):
        print("[",self.name,"] DMA: ", DMA)
        pixels = img.load()
        width, height = img.size
        
        print('Pixel Count: ',width)
        print('Frames: ', height)
        print('FPS: ', fps)
        
        durationSeconds = height/fps

        startTimeSeconds = sysstarttime
        now = time.time() - startTimeSeconds
        frameCount = 0

        while (now <= 0):
            now = time.time() - startTimeSeconds
            #busy wait until its time to start

        while (now <= durationSeconds):
            print('now', now)
            frame = max(0, math.floor(now * fps))
            
            
            for led in range(width):
                (r,g,b) = pixels[led,frame]
                self.strip.setPixelColor(led, Color(r,g,b))


#            lock.acquire()
            self.strip.show()
#            lock.release()

            frameCount += 1
            print("[", self.name, "] Frame ", frame, ", FPS: ", (frameCount / now) if now > 0.5 else 0, " Skipped: ", frame - frameCount)

            now = time.time() - startTimeSeconds


    def setAll(self, color):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)

    def show(self):
        self.strip.show()

    def snake(self):
        black = Color(0,0,0)
        white = Color(255, 255, 255)
        index = 0
        while True:
            if (index >= LED_COUNT-15):
                index = 0
            setAll(strip, black)
            self.strip.setPixelColor(index, white)
            self.strip.show()
            index += 1
