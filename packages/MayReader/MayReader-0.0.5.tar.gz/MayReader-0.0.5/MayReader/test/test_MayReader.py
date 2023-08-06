# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 17:22:11 2021

@author: Cicko-PC
"""

import unittest
from MayReader.MayReader import isComment, isNode, MayReader


class TestMayReader(unittest.TestCase):
    
    def test_isComment(self):
        self.assertTrue(isComment("//This is comment"))
        self.assertFalse(isComment("/This is not a comment"))
               
        
    def test_isNode(self):
        self.assertTrue(isNode("createNode transform -s -n"))
        self.assertFalse(isNode("/createNode transform -s -n"))
        
    def test_outputWithWrongInputFiile(self):
        mr = MayReader("notRealFile.txt")
        self.assertFalse(mr.getMashObjects())
        
    def test_outputWithProperInput(self):
        mr = MayReader("example_file_1.ma")
        dict1 = {'name': 'SphereShape', 'position': (1.0, 1.0, -6.0)
                 , 'uid': '13C79C5C-402E-63DE-D388-53B66872D238'}
        self.assertDictEqual(dict1, mr.getMashObjects()[0])
        dict2 =  {'name': 'CubeShape', 'position': (-3.0, 2.0, 2.0)
                  , 'uid': '8690CE34-4E5E-1275-5747-F8A21428D67B'}
        self.assertDictEqual(dict2, mr.getMashObjects()[1])
        dict3 = {'name': 'CylinderShape', 'position': (0.0, 0.0, 5.0)
                 , 'uid': 'A2B6EB5B-47BF-1D5D-EE78-DAA62EB25ABE'}
        self.assertDictEqual(dict3, mr.getMashObjects()[2])
