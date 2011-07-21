#!/usr/bin/env python
# encoding: utf-8
"""
foxel.py

Created by Maximillian Dornseif on 2011-07-17.
Copyright (c) 2011 HUDORA. All rights reserved.
"""

import sys
import os
import pygame
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
    datenbreitex = int(max([abs(minx), abs(maxx)]) * 2)
    datenbreitey = int(max([abs(miny), abs(maxy)]) * 2)
    scale = (float(wunschgroesse)) / float(datenbreitex)
    #print datenbreitex, datenbreitey, scale
    centerx = datenbreitex / 2 * scale
    centery = datenbreitey / 2 * scale
    # 20 Pixel Rahmen
    centerx, centery = centerx + 20, centery + 20
    screen = pygame.display.set_mode(((datenbreitex * scale) + 40, (datenbreitey * scale) + 40), 0, 32)
    pygame.display.set_caption('Foxel - Gangprofilmessung')
    #print screen, scale, centerx, centery
    return screen, scale, centerx, centery

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


if __name__ == '__main__':
    main()

