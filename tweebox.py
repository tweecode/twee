#!/usr/bin/env python

import sys, os, wx
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(scriptPath + os.sep + 'lib')
import gui

app = wx.PySimpleApp()
frame = gui.ProjectWindow(None)
app.MainLoop()
