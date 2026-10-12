# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

"""
UTILITY TO START A LOCAL SERVER

Copyright (c) 2015 __Michele Pasin__ <http://www.michelepasin.org>. All rights reserved.

Shows local repo within a server

"""

MODULE_VERSION = 0.1
USAGE = "@todo"


import time, optparse, os, rdflib, sys, webbrowser
import SimpleHTTPServer, SocketServer

from .. import main
from ..core.ontospy import Ontospy
from ..core.utils import *

DEFAULT_PORT = 7899




# in order to avoid waiting for a minute after restar
class NoBrokenServer(SocketServer.TCPServer):
	"""
	> utility class
	solve the bug with server restart
	http://stackoverflow.com/questions/10613977/a-simple-python-server-using-simplehttpserver-and-socketserver-how-do-i-close-t
	"""
	allow_reuse_address = True




def startServer(port=DEFAULT_PORT, location=None, openbrowser=True):
	""" """
	if location:
		os.chdir(location)
	Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	httpd = NoBrokenServer(("", port), Handler)

	if openbrowser:
		webbrowser.open('http://127.0.0.1:' + str(port))

	print("serving at port", port)
	httpd.serve_forever()





def parse_options():
	"""
	parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.

	https://docs.python.org/2/library/optparse.html

	"""

	parser = optparse.OptionParser(usage=USAGE, version=ontospy.VERSION)

	parser.add_option("-p", "--port",
			action="store", type="int", default=DEFAULT_PORT, dest="port",
			help="A number specifying which port to use for the server.")

	opts, args = parser.parse_args()

	# if not opts.all and not opts.query:
	#	parser.print_help()
	#	sys.exit(0)

	return opts, args




def main():
	""" command line script """
	# boilerplate
	print("Ontospy " + ontospy.VERSION)
	ontospy.get_or_create_home_repo()
	ONTOSPY_LOCAL_MODELS = ontospy.get_home_location()

	opts, args = parse_options()
	sTime = time.time()

	# switch dir and start server
	startServer(port=DEFAULT_PORT, location=ONTOSPY_LOCAL_MODELS)

	# finally:
	# print some stats....
	eTime = time.time()
	tTime = eTime - sTime
	printDebug("-" * 10)
	printDebug("Time:	   %0.2fs" %  tTime)






if __name__ == '__main__':

	# from .. import main
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt as e: # Ctrl-C
		raise e
