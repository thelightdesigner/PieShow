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

LED_COUNT = 262     
LED_PIN = 18          
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def renderPieShowFile(strip, img, fps):
    pixels = img.load()
    width, height = img.size
    
    print('Pixel Count: ',width)
    print('Frames: ', height)
    print('FPS: ', fps)
    
    durationSeconds = height/fps

    startTimeSeconds = time.time()
    now = 0
    frameCount = 0

    while (now <= durationSeconds):
        for led in range(width):
            frame = math.floor(now * fps)
            (r,g,b)  = pixels[led,frame]
            strip.setPixelColor(led, Color(r, g, b))

        strip.show()

        frameCount += 1
        print("Frame ", frame, ", FPS: ", (frameCount / now) if now > 0.5 else 0)

        now = time.time() - startTimeSeconds
            
    

def setAll(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-l', '--loop', action='store_true', help='loop the file on completion')
    args = parser.parse_args()

    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    try:
        filename = 'test.png'
        print('Reading PieShow image... ['+filename+']')
        
        pieShowImage = Image.open(filename)
        
        print('Rendering show...')
        renderPieShowFile(strip, pieShowImage, 1)
        
        while args.loop:
            print('Looping show...')
            renderPieShowFile(strip, pieShowImage, 25)

    except KeyboardInterrupt:
        if args.clear:
            setAll(strip, Color(0, 0, 0))
            strip.show()
