#! /usr/bin/python

"""

CAP 5626 AI - Preliminary Project 1

A* Algorithm on Graphs

Carlos Ezequiel

"""

import sys
from optparse import OptionParser

import pygraphviz as pgv


class CityNode:

    def __init__(self, name, xPos, yPos):
        self.name = name
        self.xPos = xPos
        self.yPos = yPos

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class CityGraph(pgv.AGraph):

    def parseLocations(self, filename):
        """Parse a locations file."""

        f = open(filename, "r")
        lines = f.readlines()
        f.close()
        
        for line in lines:
            (name, xPos, yPos) = line.split()
            xPos = int(xPos)
            yPos = int(yPos)
            node = CityNode(name, xPos, yPos)
            self.add_node(node)

    def parseConnections(self, filename):
        """Parse a connections file."""

        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        for line in lines:
            tokens = line.split()
            uName = tokens[0]
            nNeighbors = int(tokens[1])
            neighbors = tokens[2:]
            assert nNeighbors == len(neighbors)
            for vName in neighbors:
                u = self.get_node(uName)
                v = self.get_node(vName)
                self.add_edge(uName, vName)


if __name__ == '__main__':

    # Parse arguments
    usage = "usage: %prog [options] <start city> <end city> " +\
            "[city to exclude from path]"
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--connections", action="store", dest="conFile",
            default = "connections.txt")
    parser.add_option("-l", "--locations", action="store", dest="locFile",
            default="locations.txt")

    (options, args) = parser.parse_args()

    exclude = ""
    nArgs = len(args)
    if nArgs < 2:
        parser.error("Invalid number of arguments.")

    elif nArgs == 3:
        exclude = args[2]

    startCity = args[0]
    endCity = args[1]

    # Parse files
    c = CityGraph()
    c.parseLocations(options.locFile)
    c.parseConnections(options.conFile)

    # DEBUG: check graph
    c.write("graph.dot")
    c.layout(prog='dot')
    c.draw('graph.png')


