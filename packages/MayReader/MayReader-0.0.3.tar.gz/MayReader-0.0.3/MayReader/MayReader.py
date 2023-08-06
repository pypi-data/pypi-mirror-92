# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:04:52 2021

@author: Cicko-PC
"""

from os.path import exists

def isComment(line):
    """
    This function returns true if arument is comment

    Parameters
    ----------
    line : Strig value that contains one line of tekst.

    Returns
    -------
    bool. True if argument is comment.
    
    """
    return (line[0]=="/" and line[1]=="/")

def isNode(line):
    """
    Check if line is part of Node in ma file. If node starts with string "createNode"

    Parameters
    ----------
    line : Strig value that contains one line of tekst.

    Returns
    -------
    bool. True if line starts with "createNode"

    """
    
    return line[0:10]=="createNode"


class MayReader:
    """
    This class is used fore simple reading of maya ascii files.
    """
    def __init__(self, file):
        self.file = file
        self.nodes = []
        self.parse()
        
    
    def parse(self):
        """
        Parsing throw and getting important informations from maya ascii file
        Important informations are Nodes with informations of position, name and uid
        also looking to information about type of node
        Everything else is ignored

        Returns
        -------
        None.

        """
        if (not exists(self.file)): 
            return
        self.f = open(self.file, 'r')
        while(True):
            line = self.f.readline()
            if (len(line) == 0): break
            if (isComment(line) or not isNode(line)): continue
            if (line.split()[1] == "transform"): self.addNode()
            
            
    def addNode(self):
        """
        Adding one node to list attribute nodes

        Returns
        -------
        None.

        """
        number = 0
        while (True):
            lineSplit = self.f.readline().replace('"', '').split()
            if (lineSplit[0] == "setAttr" and lineSplit[1] == '.t'):
                pos = (float(lineSplit[-4]), float(lineSplit[-3]), float(lineSplit[-2]))
                number |= 1 
            if (lineSplit[0] == "createNode" and lineSplit[1] == "mesh"):
                name = lineSplit[3]
                number |= 2
            if (lineSplit[0] == "rename" and lineSplit[1] == "-uid"):
                uid = lineSplit[2]
                number |= 4
            if (number == 7): 
                self.nodes.append({"name": name, "position": pos, "uid": uid[:-1]})
                break
            if (lineSplit[0] == "createNode" and not lineSplit[1] == "mesh"):
                if (lineSplit[1] == "transform"): self.addNode()
                break
                
        
            
    def getMashObjects(self):
        """
        This method returns list of dicts for mash objects

        Returns
        -------
        List of dict.

        """
        return self.nodes
        
    
        
        


