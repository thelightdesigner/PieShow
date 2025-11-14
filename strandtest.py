#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import PixelStrip, Color
import argparse

# LED strip configuration:
LED_COUNT = 262        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def renderPieShowFile(strip, bin)
    #parse len, fps, ect.
    print(list(bin))
    
    #loop through all leds in led len
    
    #show
    
    #end when done

def setAll(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(255,255,255))


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-l', '--loop', action='store_true', help='loop the file on completion')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        filename = 'test.bin'
        print('Reading PieShow file... ['+filename+']')
        
        pieShowBin = None
        with open(filename, mode='rb') as filestream:
            pieShowBin = filestream.read()
            
        if pieShowBin is None:
            print('Failed to read file! Exiting...')
            sys.exit(1)
        
        print('Rendering show...')
        renderPieShowFile(strip, pieShowBin)
            
        while args.loop
            print('Looping show...')
            renderPieShowFile(strip, pieShowBin)

    except KeyboardInterrupt:
        if args.clear:
            setAll(strip, Color(0, 0, 0))
