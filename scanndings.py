# simple script to test Hokuyo-URG04 - tested on macosX 10.5, pygame with pythonw
# Maximillian Dornseif

import math
import fcntl
import os, sys
import time

try:
    import pygame
    from pygame.locals import *
    surfarray = pygame.surfarray
    if not surfarray: raise ImportError
except ImportError:
    raise ImportError, 'Error Importing Pygame/surfarray or Numeric'

def read_untilempty(fd):
    data = []
    while 1:
        time.sleep(0.01)
        try:
            data.append(fd.read())
        except IOError:
            if data:
                break
    return ''.join(data)
    
    
# Protocil specification is at http://static.23.nu/md/Pictures/hokuyo-URG-04LX-SCIP1-com-spec.pdf
def readdata():
    fd = open("/dev/cu.usbmodemfa131", 'r+')
    fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)
    fd.write('V\r')
    print "V\n", repr(read_untilempty(fd))
    
    fd.write('G00076801\r')
    data = read_untilempty(fd)
    # remove G00076801\n0\n
    data = data[12:].replace('\n', '')
    print repr(data)
    fd.close()
    y = list(data)
    #y = list('''0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0CQSQ>Q>Q>Q?QEQXQ]R7RfRiS=S=Ri1h1g1b1g1e1b1e1gMTMYM^M^M^0000000007060@1i1g1g1i1j2525251l1l1j1i1i1i1k1n1o2:HTHTH^H^H]H]H]HVHOHLHBH=H8H7H3H3H7H9HOHgI;IUIiJPJoKMKeLKL`MGMbNQNjOYP1P4P4P1P0OhOdO\O[OYOMOGOBO1NnNnNnOMOPOUOPOP4V423g3e3e3e3e3e3e3e3`3_3_3^3^3Y3X3X3X3X3^3^3\3\3^3\3Y3Y3Y3Y3V3Y3Z3Y3Y3Y3Y3X3X3Y3[3Y3Y3W3T3T3T3T3R3R3R3R3R3R3S3S3S3S3S3S3T3T3T3R3P3P3POAOBOBOBODOFOHOMOOOROWOZOjOjOmOnP1P7P<PAPFPKPZP[P\P\P_PhQ5Q:Q=QEQQQQQQQQQQ00Q90007OdNmNVN6M]M4LlLlLFLFLePBP0P0P0OkOeOeOkPTPaPbPnQ5Q=QCQ[QcR9R9R9R9R9R83=3=3=3=3@3B3B3C3C3G3G3G3C3G3G3G3G3G3G3N3N3N3F3C3@3@3>3:363637373;3;3;3;373636363L3P000000000000000000000000004d4d4d4m4m5F4m4m070@0@00000000000000000000QEQEQ@Q@Q9PSPSPSPYPYPYPMPMPMPTP_PgPgQ2Q;QlT]T]T]T8T5SfSeSZSYSYSYToU2U2U2U0TfTaTXTSTMTMTETDT?T?T:T:T=T:T0DTDTDTE8ShShShShSZSLSLSLDVDVDVSb07SbD6D6D6DkDkDkD6D6D6D6D6C^CLCLCLC>CaCaCaCaTT07TTCMCMCMCMCFCFC5C4C4B`B`86848486888888888888UJUPURURUVUYU^UcUlV1V3V5V@VC00000000@R@R@R@R060706?;@5@5@5A;000700000000W0VnVnVnB6B2B2B6BIBLBLBLBLBL[U[U[UBWBWBW\_07\_B_B_B__:07_:BiBiBiBi]9]X_K_K_[000000:O:O:N:O:P[k]b00000000000000000007837F7:79797979777774747475767:7@7@7E7C7D7D7H7K7O7O7O6h6`6\6>605o5g5g5o636H6X00000000000000;j;j;j;j;o?;m>000000001o1l1l1o220000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000>Y>Y>n?4?4?4?8?;?;?<?=?<?@0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C''')
    d = []
    while y:
        a = y.pop(0)
        b = y.pop(0)
        d.append(((ord(a)-0x30)<<6)+(ord(b)-0x30))
    return d

screen = pygame.display.set_mode((800, 800), 0, 32)
centerx, centery = 400, 400
# pygame.display.update()

steps = 767
factor = (767/360.0)*1.3
scale = 6.0
z = 0
while 1:
    line = []
    d = readdata()
    scanner_surface = pygame.Surface((512, 512))
    for step in range(steps):
        data = d[step]
        deg = (step/factor) + 40
        if data < 20:
            data = 19
        y = centery + int((data/scale) * math.cos(deg * (3.14159 / 180)))
        x = centerx + int((data/scale) * math.sin(deg * (3.14159 / 180)))
        if data < 20:
            pygame.draw.line(scanner_surface, (250, 0, 0), (centerx, centery), (x, y), 1)
        else:
            pygame.draw.line(scanner_surface, (250, 250, 250), (centerx, centery), (x, y), 1)
            line.append((x,y))
        #print deg, step, factor, data, x, y
    screen.blit(scanner_surface, (0,0))
    pygame.display.flip()
    fd = open('mesh.asc', 'a')
    for row in line:
        fd.write('%s %s %s \n' % (row[0], row[1], z))
    fd.close()
    z += 1
