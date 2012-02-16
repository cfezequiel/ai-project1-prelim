#! /usr/bin/python

"""

CAP 5626 AI - Preliminary Project 1

A* Algorithm on Graphs

Carlos Ezequiel

"""

import sys
from math import sqrt
from optparse import OptionParser

import networkx as nx
import pygraphviz as pgv

INPUT_DIR='../input'


class Graph(pgv.AGraph):

    def parseLocations(self, filename):
        """Parse a locations file."""

        f = open(filename, "r")
        lines = f.readlines()
        f.close()
        
        for line in lines[:-1]:
            try:
                (name, xPos, yPos) = line.split()
            except ValueError, e:
                print e
                if line != 'END':
                    print "Invalid input -> %s" % line
                    sys.exit(1)

            self.add_node(name, xPos=xPos, yPos=yPos, h=0, g=0, f=0, parent=None)

    def parseConnections(self, filename):
        """Parse a connections file."""

        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        for line in lines[:-1]:
            tokens = line.split()
            uName = tokens[0]
            nNeighbors = int(tokens[1])
            neighbors = tokens[2:]
            assert nNeighbors == len(neighbors)
            for vName in neighbors:
                self.add_edge(uName, vName)
                
def dist(u, v):
    """Get distance between nodes u and v."""
    
    dX = abs(float(u.attr['xPos']) - float(v.attr['xPos']))
    dY = abs(float(u.attr['yPos']) - float(v.attr['yPos']))

    return sqrt(pow(dX, 2) + pow(dY, 2))

def heuristicCostEstimate(u, v):
    """Get heuristic cost estimate from node u to node v."""

    return dist(u, v)

def reconstructPath(G, start, end):
    """Reconstruct the path from the end node to the start."""

    current = end
    path = [str(end)]

    while str(current) != start:
        path.insert(0, current.attr['parent'])
        current = G.get_node(current.attr['parent'])

    return path

def minFScore(nodes):
    """Get the node with the minimum F score."""

    g = lambda u: float(u.attr['f'])
    return min(nodes, key=g)

def aStar(G, start, end, exclude=None):
    """A* algorithm implementation for graphs."""

    s = G.get_node(start)
    e = G.get_node(end)

    closedSet = []
    openSet = [s]

    s.attr['g'] = 0
    s.attr['h'] = heuristicCostEstimate(s, e)

    while len(openSet) != 0:
        u = minFScore(openSet)
        if u == end:
            return reconstructPath(G, s, e)

        openSet.remove(u)
        closedSet.append(u)

        for v in G.neighbors(u):
            if v in closedSet:
                continue

            tmpG = float(u.attr['g']) + dist(u, v)

            if v not in openSet:
                openSet.append(v)
                v.attr['h'] = heuristicCostEstimate(v, e)
                tmpGIsBetter = True

            elif tmpG < v.attr['g']:
                tmpGIsBetter = True

            else:
                tmpGIsBetter = False

            if tmpGIsBetter:
                v.attr['parent'] = u
                v.attr['g']= tmpG
                v.attr['f'] = tmpG + float(v.attr['h'])

    return None
                
if __name__ == '__main__':

    # Defaults
    defaultLocFile = INPUT_DIR + "/locations.txt"
    defaultConFile = INPUT_DIR + "/connections.txt"

    # Parse arguments
    usage = "usage: %prog [options] <start city> <end city> " +\
            "[city to exclude from path]"
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--connections", action="store", dest="conFile",
            default = defaultConFile)
    parser.add_option("-l", "--locations", action="store", dest="locFile",
            default = defaultLocFile)

    (options, args) = parser.parse_args()

    exclude = ""
    nArgs = len(args)
    if nArgs < 2:
        parser.error("Invalid number of arguments.")

    elif nArgs == 3:
        exclude = args[2]

    start = args[0]
    end = args[1]

    # Parse files
    g = Graph()
    g.parseLocations(options.locFile)
    g.parseConnections(options.conFile)

    # Get shortest path using A* algorithm
    path = aStar(g, start, end)

    # Display graph
    g.layout(prog='dot')
    g.draw('graph.png')

    # Write 'dot' file
    g.write('graph.dot')


