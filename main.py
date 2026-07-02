
import os
import json
import time
import math
import argparse

from rpi_ws281x import PixelStrip, Color
from PIL import Image
from render import LEDTape

from rpi_ws281x import PixelStrip, Color

LEDStrips = []
SmartBulbs = []

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-l', '--loop', action='store_true', help='loop the file on completion')       
    parser.add_argument('-w','--white', action='store_true', help='make the whole strip white')
    parser.add_argument('-s','--snake', action='store_true', help='')
    parser.add_argument('-t','--two', action='store_true', help='')
    args = parser.parse_args()
    
    print('Loading config.json')

    config = {}
    with open("config.json", "r") as file:
        config = json.load(file)
    
    print(config)
    
    print('Initializing LEDTapes')
    for ledTapeInfo in config['devices']['LEDTape']:
        LEDStrips.append(LEDTape(ledTapeInfo['lightID'], ledTapeInfo['channel'], ledTapeInfo['GPIO'], ledTapeInfo['pixels'], ledTapeInfo['name']))
    
    print('Reading maps')
    mapFiles = os.listdir('maps')
    print('Map files: ', mapFiles)
    
    mapIdx = 0
    mapPath = os.path.join('maps', mapFiles[mapIdx])

    print('Loading map ', mapPath)
    mapInfo = {}
    with open(os.path.join(mapPath, "info.json"), "r") as file:
        mapInfo = json.load(file)
    
    print(mapInfo)
    pieShowImagePath = os.path.join(mapPath, mapInfo["mapFileName"])
    
    print('Reading PieShow image... ['+pieShowImagePath+']')
    
    pieShowImage = Image.open(pieShowImagePath)
    
    print('Rendering show...')
    timeToStart = time.time() + 5
    LEDStrips[0].renderPieShowFile(pieShowImage, mapInfo['FPS'], timeToStart)
    
    LEDStrips[0].setAll(Color(0,0,0))
    LEDStrips[0].show()
    
    LEDStrips[1].renderPieShowFile(pieShowImage, mapInfo['FPS'], time.time())
    
    LEDStrips[1].setAll(Color(0,0,0))
    LEDStrips[1].show()


