# -*- coding: UTF-8 -*-
import sys

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if(len(sys.argv)==1):
	import gameGui
	gameGui.MathemaGridsApp().run()
elif(sys.argv[1] == "--console"):
	print "execute console version"