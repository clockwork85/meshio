"""
I/O for ERDC 2dm / 3dm file format
"""

import numpy as np 

from .._files import open_file
from .._helpers import register
from .._mesh import CellBlock, Mesh



def read(filename):
    with open_file(filename, "r") as f: 
        mesh = read_buffer(f)
    return mesh

def read_buffer(f):
    points = []
    facets = []
    mats = []

    while True:
        line = f.readline()

        if not line:
            # EOF
            break

        strip = line.strip()

        if len(strip) == 0 or strip[0] == "#":
            continue

        split = strip.split()

        if split[0] == "ND":
            # vertex
            points.append([float(x) for x in split])
        elif split[0] == "E3T":
            # triangle
            data = [int(x) for x in split[2:]]
            facets.append(data[0:3])
            mats.append(data[3])
        elif split[0] == "E4T":
            # tetrahedron
            data = [int(x) for x in split[2:]]
            facets.append(data[0:4])
            mats.append(data[4])
        else:
            continue
        
        # Turn into numpy arrays
        points = np.array(points)
        facets = np.array(facets)
        mats = np.array(mats)
