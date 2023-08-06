# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:24:26 2021

@author: Cicko-PC
"""
from MayReader import *
mr = MayReader("example_files//example_file_1.ma")
ma = mr.getMashObjects()
print((ma))
