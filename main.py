
import os
import json
import time
import math
import argparse

from multi_ws281x import mPixelStrip, mRGBW
from PIL import Image
from render import LEDTape

from rpi_ws281x import PixelStrip, Color

LEDStrip = None
SmartBulbs = []

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
 #   parser.add_argument('-l', '--loop', action='store_true', help='loop the file on completion')       
 #   parser.add_argument('-w','--white', action='store_true', help='make the whole strip white')
 #   parser.add_argument('-s','--snake', action='store_true', help='')
#    parser.add_argument('-t','--two', action='store_true', help='')
    parser.add_argument('-i', '--index', action='store_true', help='')
    parser.add_argument('-r', '--rainbow', action='store_true', help='')
    parser.add_argument('-s', '--standby', action='store_true', help='')
    args = parser.parse_args()
    
    print('Loading config.json')

    config = {}
    with open("config.json", "r") as file:
        config = json.load(file)
    
    print(config)
    
    print('Initializing LEDTapes')
    
    ledTapeInfo = config['devices']['LEDTape']
    ledTapeChannels = config['devices']['LEDTape']['channels']
    if len(ledTapeChannels) != 2:
        raise Exception('Must have 2 channels TODO fix. Count=', len(ledTapeChannels))
    
    LEDStrip = LEDTape(ledTapeInfo['lightID'], ledTapeInfo['name'], ledTapeChannels[0]['GPIO'], ledTapeChannels[1]['GPIO'], ledTapeChannels[0]['pixels'], ledTapeChannels[1]['pixels'])
    
    if args.standby:
       # LEDStrip.christmasLight()
        LEDStrip.setAll(mRGBW(27, 16, 4))
        LEDStrip.show()
        exit()
    elif args.index:
        idx = 0
        ch = 0
        while True:
            print("idx=", idx, "ch=", ch)
            _in = input()
            LEDStrip.setAll(mRGBW(0,0,0))
            LEDStrip.set(ch, idx, mRGBW(100,100,100))
            LEDStrip.show()
            idx += 1
            if (idx >= ledTapeChannels[0]['pixels']):
                idx = 0
                ch = 1
            elif (idx >= ledTapeChannels[1]['pixels']):
               idx = 0
               ch = 0
    elif args.clear:
        LEDStrip.setAll(mRGBW(0,0,0))
        LEDStrip.show()
        exit()
    elif args.rainbow:
        idx = 0
        scale = 100
        while True:
            LEDStrip.setAllRainbow(idx, scale,255)
            LEDStrip.show()
            idx += 1
            if (idx >= 100): 
                idx = 0
    
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
    LEDStrip.renderPieShowFile(pieShowImage, mapInfo['FPS'])

    LEDStrips.setAll(mColor(0,0,0))
    LEDStrips.show()
