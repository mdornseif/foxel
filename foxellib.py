#!/usr/bin/env python
# encoding: utf-8
"""
foxellib.py - interfacing with a Hokuyo-URG04 SCIP 1.0 LIDAR

See http://www.hokuyo-aut.jp/02sensor/07scanner/download/urg_programs_en/ 
http://svn.sourceforge.jp/svnroot/qrobosdk/ http://www.ros.org/wiki/hokuyo_node
and http://correll.cs.colorado.edu/pmwiki/index.php/Main/LaserScanner
for other approaches of interfacing with the hardware.


Created by Maximillian Dornseif on 2011-07-14, based on his code from 2008.
Copyright (c) 2011, 2012 Dr. Maximillian Dornseif. All rights reserved.
"""

import math
import fcntl
import os, sys
import time

def read_untilempty(fd):
    """Simple minded approach to read a Hokuyo Answer from an USB connection"""
    data = []
    while 1:
        time.sleep(0.05)
        try:
            data.append(fd.read())
        except IOError:
            if data:
                break
    return ''.join(data)


# Protocil specification is at http://static.23.nu/md/Pictures/hokuyo-URG-04LX-SCIP1-com-spec.pdf
def aquire_scan():
    """Aquire data from the scanner."""
    fd = open("/dev/cu.usbmodemfd121", 'r+')
    fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)
    # request version info,
    fd.write('V\r')
    versioninfo = read_untilempty(fd)
    
    # request svan over full range
    fd.write('G00076801\r')
    data = read_untilempty(fd)
    # remove command echo 'G00076801\n0\n'
    data = data[12:].replace('\n', '')
    fd.close()
    # typical reply looks like
    # 0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0CQSQ>Q>Q>Q?QEQX
    # Q]R7RfRiS=S=Ri1h1g1b1g1e1b1e1gMTMYM^M^M^0000000007060@1i1g1g1i1j2525251l1l1j1i1i1i1k1n1o2:HTHTH^H^H]H]
    # H]HVHOHLHBH=H8H7H3H3H7H9HOHgI;IUIiJPJoKMKeLKL`MGMbNQNjOYP1P4P4P1P0OhOdO\O[OYOMOGOBO1NnNnNnOMOPOUOPOP4V
    # 423g3e3e3e3e3e3e3e3`3_3_3^3^3Y3X3X3X3X3^3^3\3\3^3\3Y3Y3Y3Y3V3Y3Z3Y3Y3Y3Y3X3X3Y3[3Y3Y3W3T3T3T3T3R3R3R3R
    # 3R3R3S3S3S3S3S3S3T3T3T3R3P3P3POAOBOBOBODOFOHOMOOOROWOZOjOjOmOnP1P7P<PAPFPKPZP[P\P\P_PhQ5Q:Q=QEQQQQQQQQ
    # QQ00Q90007OdNmNVN6M]M4LlLlLFLFLePBP0P0P0OkOeOeOkPTPaPbPnQ5Q=QCQ[QcR9R9R9R9R9R83=3=3=3=3@3B3B3C3C3G3G3G
    # 3C3G3G3G3G3G3G3N3N3N3F3C3@3@3>3:363637373;3;3;3;373636363L3P000000000000000000000000004d4d4d4m4m5F4m4m
    # 070@0@00000000000000000000QEQEQ@Q@Q9PSPSPSPYPYPYPMPMPMPTP_PgPgQ2Q;QlT]T]T]T8T5SfSeSZSYSYSYToU2U2U2U0Tf
    # TaTXTSTMTMTETDT?T?T:T:T=T:T0DTDTDTE8ShShShShSZSLSLSLDVDVDVSb07SbD6D6D6DkDkDkD6D6D6D6D6C^CLCLCLC>CaCaCa
    # CaTT07TTCMCMCMCMCFCFC5C4C4B`B`86848486888888888888UJUPURURUVUYU^UcUlV1V3V5V@VC00000000@R@R@R@R060706?;
    # @5@5@5A;000700000000W0VnVnVnB6B2B2B6BIBLBLBLBLBL[U[U[UBWBWBW\_07\_B_B_B__:07_:BiBiBiBi]9]X_K_K_[000000
    # :O:O:N:O:P[k]b00000000000000000007837F7:79797979777774747475767:7@7@7E7C7D7D7H7K7O7O7O6h6`6\6>605o5g5g
    # 5o636H6X00000000000000;j;j;j;j;o?;m>000000001o1l1l1o22000000000000000000000000000000000000000000000000
    # 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000>Y
    # >Y>n?4?4?4?8?;?;?<?=?<?@0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C0C
    # 0C0C0C0C
    y = list(data)
    d = []
    while y:
        # decode two bytes into one value
        a = y.pop(0)
        b = y.pop(0)
        d.append(((ord(a)-0x30)<<6)+(ord(b)-0x30))
    # d now contains the list of measured distance
    return d


def read_walls():
    """Gibt die gemessene Position der Wände als Ploygonzug in mm zurück.

    >>> read_walls()
    [(41, 28), (44, 30), ..., (-48, 30)]
    """
    polygon = []
    steps = 767
    factor = (767/360.0)*1.3
    d = aquire_scan()
    for step in range(steps):
        data = d[step]
        # the scanner has a 40 degree "blind spot" at the beginning
        deg = (step / factor) + 40
        # values of 19 and lower are error codes
        if data < 20:
            data = 19
            # so far we simply ignore all errors
        else:
            rdeg = deg * (3.14159 / 180.0)
            y = int(data * math.cos(rdeg))
            x = int(data * math.sin(rdeg))
            polygon.append((x,y))
    return polygon


if __name__ == '__main__':
    print read_walls()
