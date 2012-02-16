#!/usr/bin/env python
# encoding: utf-8
"""
foxelgfx.py - draw from foxel data

Created by Maximillian Dornseif on 2012-02-16.
Copyright (c) 2012 Dr. Maximillian Dornseif. All rights reserved.
"""

import sys
import os
import json
import pygame
import time
from pygame.locals import *
import foxellib
import cairo
import math

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

def distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return math.sqrt((float(x2-x1) ** 2) + (float(y2-y1) ** 2))


def flaeche(data):
    # Fläche berechnen:
    # You can use something known as Hero's (or Heron's) Formula, which uses the semi-perimeter (half of the perimeter) in the following formula: Area = sq rt{s(s - a)(s - b)(s - c)}
    # Find the semiperimeter --- in other words, add the three sides, then divide by 2. This is s.
    # Subtract (semiperim.) - side A
    # Subtract (semiperim.) - side B
    # Subtract (semiperim.) - side C
    # Multiply steps 2 through 4
    # Multiply step 5 by the semiperim.
    # Take the square root of that result.
    
    # copy input
    data = data[:]
    vorheriger = data.pop()
    flaeche = 0
    while data:
        a = vorheriger
        b = data.pop()
        c = (0, 0)
        sidea = distance(b, c)
        sideb = distance(a, c)
        # Seite c ist in der regel zu kurz fuer sinnvolle berechungen
        sidec = distance(a, b)
        #sidec *= 10
        semiperimeter = (sidea + sideb + sidec) / 2.0
        tmp = semiperimeter * (semiperimeter - sidea) * (semiperimeter - sideb) * (semiperimeter - sidec)
        if tmp > 0:
            flaeche += math.sqrt(tmp)
        vorheriger = b
    return flaeche

paper_width = 210
paper_height = 297
margin = 20
point_to_milimeter = 72/25.4
CANVASX = int(paper_width*point_to_milimeter)
CANVASY = int(paper_height*point_to_milimeter)
def draw(data, fname):
    # Maximale ausdehnung der Daten
    WIDTH, HEIGHT = 4100*2, 4100*2
    
    surface = cairo.PDFSurface ('%s.pdf' % fname, CANVASX, CANVASY)
    #surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, CANVASX, CANVASY)
    ctx = cairo.Context (surface)
    # Koordinatenursprung ist in der Mitte
    ctx.translate (CANVASX/2.5, CANVASY/2)
    # Masstab 4 cm => 1 m
    ctx.scale (0.04*point_to_milimeter, 0.04*point_to_milimeter)

    # schwarze hintergrundfarbe
    #ctx.rectangle(-WIDTH, -HEIGHT, WIDTH*2, HEIGHT*2)
    #ctx.set_source_rgb(0, 0, 0)
    #ctx.fill()

    minx, maxx, miny, maxy = 0, 0, 0, 0
    outline = []
    # die einzelnen laserstralen zeichnen
    ctx.set_source_rgb (1.0, 0.2, 0.2);
    ctx.set_line_width (1)
    for point in data:
        x, y = point
        minx = min([minx, x])
        maxx = max([maxx, x])
        miny = min([miny, y])
        maxy = max([maxy, y])
        ctx.move_to(0, 0)
        ctx.line_to (x, y)
        ctx.stroke()
        outline.append((x, y))
    ctx.stroke ()

    # Profil zeichnen
    ctx.set_source_rgb (0.0, 0.0, 0.0);
    ctx.set_line_width (10)
    ctx.move_to(outline[0][0], outline[0][1])
    for x, y in outline:
        ctx.line_to (x, y)
    ctx.close_path()
    ctx.stroke()

    # Beschriftung
    ctx.select_font_face('Sans')
    ctx.set_font_size(120) # em-square height is 180 pixels
    ctx.set_source_rgb(0.0, 0.0, 0.0) 
    ctx.set_line_width (2)

    # Masstab zeichnen
    ctx.save()
    ctx.translate (minx + 10, maxy + 100)
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width (1)
    for i in range(3):
        y = 0
        x = i * 1000
        ctx.set_source_rgb (0.0, 0.0, 0.0);
        ctx.move_to(x+950, y-10)
        ctx.show_text("%d m" % (i+1))
        ctx.rectangle(x, y, 500, 40)
        ctx.fill_preserve()
        ctx.stroke()
        ctx.set_source_rgb (1.0, 1.0, 1.0);
        ctx.rectangle(x+500, y, 500, 40)
        ctx.fill_preserve()
        ctx.set_source_rgb (0.0, 0.0, 0.0);
        ctx.stroke()
    ctx.restore()

    # von oben nach unten
    ctx.save()
    ctx.translate (minx - 50, miny + 10)
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width (1)
    for i in range(3):
        x = 0
        y = i * 1000
        ctx.set_source_rgb (0.0, 0.0, 0.0);
        #ctx.move_to(x+950, y-10)
        #ctx.show_text("%d m" % (i+1))
        ctx.rectangle(x, y, 40, 500)
        ctx.fill_preserve()
        ctx.stroke()
        ctx.set_source_rgb (1.0, 1.0, 1.0);
        ctx.rectangle(x, y+500, 40, 500)
        ctx.fill_preserve()
        ctx.set_source_rgb (0.0, 0.0, 0.0);
        ctx.stroke()
    ctx.restore()

    # Beschriftung oben
    ctx.save()
    ctx.translate (0, miny-70)
    ctx.move_to(0, -10)
    ctx.show_text("%d mm" % (maxx - minx))
    # Pfeil
    ctx.move_to(minx+50, 50)
    ctx.line_to (minx, 0)
    ctx.line_to (maxx, 0)
    ctx.line_to (maxx-50, 50)

    ctx.move_to(minx+50, -50)
    ctx.line_to (minx, 0)
    ctx.line_to (maxx, 0)
    ctx.line_to (maxx-50, -50)
    ctx.stroke()
    ctx.restore()

    # Beschriftung rechts
    ctx.save()
    ctx.translate (maxx+50, 0)
    ctx.move_to(20, 0)
    ctx.show_text("%d mm" % (maxy - miny))
    # Pfeil
    ctx.move_to(50, miny+50)
    ctx.line_to (0, miny)
    ctx.line_to (0, maxy)
    ctx.line_to (50, maxy-50)

    ctx.move_to(-50, miny+50)
    ctx.line_to (0, miny)
    ctx.line_to (0, maxy)
    ctx.line_to (-50, maxy-50)
    ctx.stroke()
    ctx.restore()

    ctx.save()
    m2 = flaeche(data)/1000.0/1000.0
    ctx.move_to(0, 500)
    ctx.show_text("Oeffnung: %.4f qm" % m2)
    ctx.stroke()
    ctx.restore()


    surface.write_to_png ('%s.png' % fname) # Output to PNG
    surface.show_page()
    surface.finish()


def main():
    for fn in os.listdir('.'):
        if fn.startswith('scan') and fn.endswith('data'):
            newname = os.path.basename(fn).split('.')[0]
            print newname
            data = json.loads(open(fn).read())
            draw(data, newname)

                  
if __name__ == '__main__':
    main()

