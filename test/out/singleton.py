# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 23:39:30 2021

@author: josep
"""

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kw_args):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, val):
        self.val = val
        
    def prnt_val(self):
        print(self.val)
        
if __name__ == "__main__":
    s = Singleton(15)
    t = Singleton(20)
    s.prnt_val()
    t.prnt_val()