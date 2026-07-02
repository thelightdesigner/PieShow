#!/usr/bin/env python3

# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

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
    
    def __init__(self, lightID, DMAChannel, GPIO, pixelCount):
        self.lightID = lightID
        self.strip = PixelStrip(pixelCount, GPIO, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, DMAChannel)
        self.strip.begin()

    def renderPieShowFile(self, img, fps, sysstarttime):
        pixels = img.load()
        width, height = img.size
        
        print('Pixel Count: ',width)
        print('Frames: ', height)
        print('FPS: ', fps)
        
        durationSeconds = height/fps

        startTimeSeconds = sysstarttime
        now = time.time() - startTimeSeconds
        frameCount = 0

        while (now <= durationSeconds):
            frame = math.floor(now * fps)

            for led in range(width):
                (r,g,b)  = pixels[led,frame]
                strip.setPixelColor(led, Color(r, g, b))

            strip.show()

            frameCount += 1
            print("[TID", tid, "] Frame ", frame, ", FPS: ", (frameCount / now) if now > 0.5 else 0)

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
            strip.setPixelColor(index, white)
            strip.show()
            index += 1