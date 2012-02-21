#! /usr/bin/python

"""

CAP 5626 AI - Preliminary Project 1

A* Algorithm on Graphs

Carlos Ezequiel

"""

import sys
from math import sqrt
from optparse import OptionParser


INPUT_DIR='../input'

class Node:

    def __init__(self, name, attr={}):
        self.attr = {'name': name}
        self.attr.update(attr)

    def __repr__(self):
        return self.attr['name']
    
    def __str__(self):
        return self.attr['name']

class Graph:

    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_edge(self, u, v, label=None):
        uNode = self.get_node(u)
        vNode = self.get_node(v)
        try:
            self.edges[uNode].append(vNode)
        except KeyError:
            self.edges[uNode] = [vNode]

        try:
            self.edges[vNode].append(uNode)
        except KeyError:
            self.edges[vNode] = [uNode]

    def add_node(self, u, *args, **attr):
        self.nodes[u] = Node(u, attr)

    def neighbors(self, u):
        return self.edges[u]
        
    def get_node(self, u):
        try:
            return self.nodes[u]
        except KeyError:
            return None

    def parseLocations(self, filename):
        """Parse a locations file."""

        f = open(filename, "r")
        lines = f.readlines()
        f.close()
        
        # Iterate through each line except last (END marker)
        assert(lines[-1] == 'END')
        for line in lines[:-1]:
            try:
                (name, yPos, xPos) = line.split()
            except ValueError, e:
                print e
                if line != 'END':
                    print "Invalid input -> %s" % line
                    sys.exit(1)

            pos = "%s, %s" % (xPos, yPos)

            # Note: all node attributes are stored as strings
            self.add_node(name, pos=pos, h=0, g=0, f=0, parent=None)

    def parseConnections(self, filename):
        """Parse a connections file."""

        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        # Iterate through each line except last (END marker)
        assert(lines[-1] == 'END')
        for line in lines[:-1]:
            tokens = line.split()
            uName = tokens[0]
            nNeighbors = int(tokens[1])
            neighbors = tokens[2:]
            assert nNeighbors == len(neighbors)
            for vName in neighbors:
                u = self.get_node(uName)
                v = self.get_node(vName)
                self.add_edge(uName, vName, label="%4.2f" % dist(u, v))
                
def dist(u, v):
    """Get straight line distance between nodes u and v."""
    
    (uX, uY) = [float(num) for num in u.attr['pos'].split(", ")]
    (vX, vY) = [float(num) for num in v.attr['pos'].split(", ")]
    dX = abs(uX - vX)
    dY = abs(uY - vY)

    return float(sqrt(pow(dX, 2) + pow(dY, 2)))

def heuristicCostEstimate(u, v):
    """Get heuristic cost estimate from node u to node v."""

    return dist(u, v)

def reconstructPath(G, s, e):
    """Reconstruct the path from the end node to the start."""

    u = e
    path = [str(e)]

    while u != None:
        u = G.get_node(str(u.attr['parent']))
        path.insert(0, str(u))
        if u == s:
            return path

    # Couldn't find start, this is an error
    return None

def aStar(G, start, end, exclude=None):
    """A* algorithm implementation for graphs."""

    s = G.get_node(start)
    e = G.get_node(end)
    x = None
    if exclude:
        x = G.get_node(exclude)

    closedSet = [x]
    openSet = [s]

    s.attr['g'] = 0
    s.attr['h'] = heuristicCostEstimate(s, e)

    while len(openSet) != 0:
        # Get minimum 'f' value
        u = min(openSet, key=lambda u: float(u.attr['f']))
        if u == e:
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

            elif tmpG < float(v.attr['g']):
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
    path = aStar(g, start, end, exclude)
    print path
    print "Shortest path: " + "->".join(path)


