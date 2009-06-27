#
# Project
#
# A project is a collection of source files, a target, and a destination file.
#

import sys, os, pickle, re
from tiddlywiki import TiddlyWiki

class Project:

	def __init__ (self, path = ''):
		if path == '':
			self.sources = []
			self.target = 'sugarcane'
			self.destination = ''
		else:
			file = open(path, 'r')
			saved = pickle.load(file)
			self.sources = saved.sources
			self.target = saved.target
			self.destination = saved.destination
			file.close()
		
	def build (self):
		tw = TiddlyWiki('twee')
		
		dest = open(self.destination, 'w')
		
		for source in self.sources:
			file = open(source)		
			tw.add_twee(file.read())
			file.close()

		header = open(self.getTargetPath() + self.target + os.sep + 'header.html')
		dest.write(header.read())
		header.close()
		
		dest.write(tw.to_html())
		dest.write('</div></html>')
		dest.close()
		
		return True


	def proof (self):		
		# preamble
		
		output = r'{\rtf1\ansi\ansicpg1251' + '\n'
		output += r'{\fonttbl\f0\fswiss\fcharset0 Arial;}' + '\n'
		output += r'{\colortbl;\red128\green128\blue128;}' + '\n'
		output += r'\margl1440\margr1440\vieww9000\viewh8400\viewkind0' + '\n'
		output += r'\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx792' + '\n'
		output += r'\tx8640\ql\qnatural\pardirnatural\pgnx720\pgny720' + '\n'
		
		# individual source files
		
		for source in self.sources:
			file = open(source)		
			lines = file.read().split('\n')
			
			output += r'\f0\b\fs32' + os.path.basename(source) + r'\b0\fs20' + '\\\n\\\n' 
			
			for line in lines:
				if line[:2] == '::':
					output += r'\fs24\b' + line[2:] + r'\b0\fs20' + '\\\n'		
				else:
					line = re.sub(r'\[\[(.*?)\]\]', r'\ul \1\ulnone ', line)
					line = re.sub(r'\/\/(.*?)\/\/', r'\i \1\i0 ', line)
					line = re.sub(r'(\<\<.*?\>\>)', r'\cf1 \i \1\i0 \cf0', line)
			
					output += line + '\\\n'
			
			if source != self.sources[-1]:
				output += '\\\n\\\n\\\n\page'
			file.close()
			
		output += '}'
		
		# save it
		
		proofDest = re.sub(r'\..*$', '.rtf', self.destination)
		dest = open(proofDest, 'w')
		dest.write(output)
		dest.close()
		
		return True


	def save (self, path):
		file = open(path, 'w')
		pickle.dump(self, file)
		file.close()


	def getTargetPath(self):
		scriptPath = os.path.realpath(sys.path[0])
		
		# OS X py2app'd apps will direct us right into the app bundle
		
		appRe = re.compile('[^/]+.app/Contents/Resources')
		scriptPath = appRe.sub('', scriptPath)
		
		# Windows py2exe'd apps add an extraneous library.zip at the end
		
		scriptPath = scriptPath.replace('\\library.zip', '')
		
		scriptPath += os.sep + 'targets' + os.sep
		print scriptPath
		return scriptPath