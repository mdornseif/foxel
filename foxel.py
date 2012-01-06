#!/usr/bin/env python
# encoding: utf-8
"""
foxel.py - userinterface for scanning range finder

Created by Maximillian Dornseif on 2011-07-17.
Copyright (c) 2011 HUDORA. All rights reserved.
"""

import sys
import os
import json
import pygame
import time
from pygame.locals import *
import foxellib


factor = (767/360.0)*1.3
scale = 6.0

def find_dimensions():
    data = foxellib.read_walls()
    minx = maxx = miny = maxy = 0
    for point in data:
        x, y = point
        minx = min([minx, x])
        maxx = max([maxx, x])
        miny = min([miny, y])
        maxy = max([maxy, y])
    return (minx, maxx, miny, maxy)


def setup_screen():
    wunschgroesse = 800
    minx, maxx, miny, maxy = find_dimensions()
    datenbreitex = int(max([abs(minx), abs(maxx)]) * 2) + 400
    datenbreitey = int(max([abs(miny), abs(maxy)]) * 2)
    scale = float(wunschgroesse) / float(datenbreitex)
    #print datenbreitex, datenbreitey, scale
    centerx = datenbreitex / 2 * scale
    centery = datenbreitey / 2 * scale
    # 20 Pixel Rahmen
    centerx, centery = centerx + 20, centery + 20
    screen = pygame.display.set_mode((int(datenbreitex * scale) + 40, int(datenbreitey * scale) + 40), 0, 32)
    pygame.display.set_caption('Foxel - Gangprofilmessung')
    #print screen, scale, centerx, centery
    return screen, scale, centerx, centery

# Fläche berechnen:
# You can use something known as Hero's (or Heron's) Formula, which uses the semi-perimeter (half of the perimeter) in the following formula: Area = sq rt{s(s - a)(s - b)(s - c)}
# Find the semiperimeter --- in other words, add the three sides, then divide by 2. This is s.
# Subtract (semiperim.) - side A
# Subtract (semiperim.) - side B
# Subtract (semiperim.) - side C
# Multiply steps 2 through 4
# Multiply step 5 by the semiperim.
# Take the square root of that result.


def main():
    screen, scale, centerx, centery = setup_screen()
    # pygame.display.update()
    pygame.init()
    pygame.font.init()
    while 1:
        data = foxellib.read_walls()
        scanner_surface = pygame.Surface((centerx*2, centery*2))
        line = []
        minx, maxx, miny, maxy = 0, 0, 0, 0
        for point in data:
            x, y = point
            x = x * scale
            y = y * scale
            minx = min([minx, x])
            maxx = max([maxx, x])
            miny = min([miny, y])
            maxy = max([maxy, y])
            pygame.draw.line(scanner_surface, (100, 0, 0), (centerx, centery), (x+centerx, y+centery), 1)
            line.append((x+centerx, y+centery))
            #print (centerx, centery), (x+centerx, y+centery)
        lol = pygame.draw.lines(scanner_surface, (255,255,255), False, line, 1)

        font = pygame.font.Font(None, 24)
        color = (200, 200, 200)
        # Beschriftung unten
        right = maxx + centerx # scanner_surface.get_width()-20
        left = minx + centerx # 20
        y = centery+80
        # Pfeil
        pygame.draw.line(scanner_surface, color, (left, y), (right, y), 1)
        pygame.draw.line(scanner_surface, color, (left, y+10), (left, y-10), 1)
        pygame.draw.line(scanner_surface, color, (right, y+10), (right, y-10), 1)
        text = font.render("%d mm" % ((right-left)/scale), 1, (255, 255, 255))
        textpos = text.get_rect(center=((right + left) / 2, y))
        scanner_surface.blit(text, textpos)
        # Beschriftung rechts
        bottom = maxy + centery # scanner_surface.get_width()-20
        top = miny + centery # 20
        x = right + 40
        pygame.draw.line(scanner_surface, color, (x, top), (x, bottom), 1)
        pygame.draw.line(scanner_surface, color, (x+10, top), (x-10, top), 1)
        pygame.draw.line(scanner_surface, color, (x+10, bottom), (x-10, bottom), 1)
        text = font.render("%d mm" % ((bottom-top)/scale), 1, (255, 255, 255))
        textpos = text.get_rect(center=(x, (top + bottom) / 2))
        scanner_surface.blit(text, textpos)
        
        # Masstab zeichnen
        y = centery + 120
        pygame.draw.line(scanner_surface, color, (20, y), (20+(1000*scale), y), 10)
        for i in range(5):
            shift = (i * 200) * scale
            pygame.draw.line(scanner_surface, (0,0,0), (21+shift, y), (21+shift+(100*scale), y), 8)
        
        screen.blit(scanner_surface, (0,0))
        pygame.display.flip()
        time.sleep(0.3)
        for event in pygame.event.get():
           if (event.type == KEYDOWN):
              if (event.key == K_ESCAPE):
                 sys.exit(0)
              if (event.key == K_SPACE):
                  startname = 0
                  while os.path.exists('scan%03d.data' % startname):
                      startname += 1
                  fd = open('scan%03d.data' % startname, 'w')
                  fd.write(json.dumps(data))
                  fd.close()
                  print 'scan%03d.data' % startname
                  pygame.display.set_caption('scan%03d.data' % startname)
                  
if __name__ == '__main__':
    main()

