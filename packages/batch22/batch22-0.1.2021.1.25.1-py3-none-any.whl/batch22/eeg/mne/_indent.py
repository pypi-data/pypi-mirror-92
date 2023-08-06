#!/usr/bin/env python
# -*- coding: utf-8 -*

from collections import OrderedDict

def indS(indent=0):
    return ("  "*indent)

def indD(indent=0):
    return ("  "*indent)+"- "

def indN(indent=0):
    return "\n"+("  "*indent)

def indB(indent=0):
    return "\n"+("  "*indent)+"- "
