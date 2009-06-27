#
# TiddlyWiki.py
#
# A Python implementation of the Twee compiler.
#
# This code was written by Chris Klimas <klimas@gmail.com>
# It is licensed under the GNU General Public License v2
# http://creativecommons.org/licenses/GPL/2.0/
#
# This file defines two classes: Tiddler and TiddlyWiki. These match what
# you'd normally see in a TiddlyWiki; the goal here is to provide classes
# that translate between Twee and TiddlyWiki output seamlessly.
#

import re
import datetime
import time
import PyRSS2Gen as rss

#
# TiddlyWiki class
#

class TiddlyWiki:
	"represents an entire TiddlyWiki"
	
	def __init__ (self, author = 'twee'):
		"constructor; optionally pass an author name"
		self.author = author
		self.tiddlers = {}


	def try_getting (self, names, default = ''):
		"tries retrieving the text of several tiddlers by name; returns default if none exist"
		for name in names:
			if name in self.tiddlers:
				return self.tiddlers[name].text
				
		return default
		
		
	def to_twee (self):
		"returns Twee source code for this TiddlyWiki"
		output = ''
		
		for i in self.tiddlers:
			output += self.tiddlers[i].to_twee()
		
		return output
		
	
	def to_html (self):
		"returns HTML code for this TiddlyWiki"
		output = ''
		
		for i in self.tiddlers:
			output += self.tiddlers[i].to_html(self.author)
			
		return output
		
		
	def to_rss (self, num_items = 5):
		"returns an RSS2 object of recently changed tiddlers"
		url = self.try_getting(['StoryUrl', 'SiteUrl'])
		title = self.try_getting(['StoryTitle', 'SiteTitle'], 'Untitled Story')
		subtitle = self.try_getting(['StorySubtitle', 'SiteSubtitle'])
		
		# build a date-sorted list of tiddler titles
		
		sorted_keys = self.tiddlers.keys()
		sorted_keys.sort(key = lambda i: self.tiddlers[i].modified)
				
		# and then generate our items
		
		rss_items = []
		
		for i in sorted_keys[:num_items]:
			rss_items.append(self.tiddlers[i].to_rss())
				
		return rss.RSS2(
			title = title,
			link = url,
			description = subtitle,
			pubDate = datetime.datetime.now(),
			items = rss_items
			)
		
	
	def add_twee (self, source):
		"converts Twee source code to tiddlers in this TiddlyWiki"
		source = source.replace("\r\n", "\n")
		tiddlers = source.split('\n::')
		
		for i in tiddlers:
			self.add_tiddler(Tiddler('::' + i))
			
	
	def add_html (self, source):
		"converts HTML source code to tiddlers in this TiddlyWiki"
		divs_re = re.compile(r'<div id="storeArea">(.*)</div>\s*</html>',
												 re.DOTALL)
		divs = divs_re.search(source)

		if divs:
			for div in divs.group(1).split('<div'):
				self.add_tiddler(Tiddler('<div' + div, 'html'))
		

	def add_tiddler (self, tiddler):
		"adds a tiddler to this TiddlyWiki"
		
		if tiddler.title in self.tiddlers:
			if (tiddler == self.tiddlers[tiddler.title]) and \
				 (tiddler.modified > self.tiddlers[tiddler.title].modified):
				self.tiddlers[tiddler.title] = tiddler
		else:
			self.tiddlers[tiddler.title] = tiddler

		
#
# Tiddler class
#

		
class Tiddler:
	"represents a single tiddler in a TiddlyWiki"
	
	def __init__ (self, source, type = 'twee'):
		"constructor; pass source code, and optionally 'twee' or 'html'"
		if type == 'twee':
			self.init_twee(source)
		else:
			self.init_html(source)


	def __cmp__ (self, other):
		"compares a Tiddler to another"
		return self.text == other.text
		

			
	def init_twee (self, source):
		"initializes a Tiddler from Twee source code"
	
		# we were just born
		
		self.created = self.modified = time.localtime()
		
		# figure out our title
				
		lines = source.strip().split('\n')
				
		meta_bits = lines[0].split('[')
		self.title = meta_bits[0].strip(' :')
				
		# find tags

		self.tags = []
		
		if len(meta_bits) > 1:
			tag_bits = meta_bits[1].split(' ')
		
			for tag in tag_bits:
				self.tags.append(tag.strip('[]'))
				
		# and then the body text
		
		self.text = ''
		
		for line in lines[1:]:
			self.text += line + "\n"
			
		self.text = self.text.strip()
		
		
	def init_html (self, source):
		"initializes a Tiddler from HTML source code"
	
		# title
		
		self.title = 'untitled passage'
		title_re = re.compile(r'tiddler="(.*?)"')
		title = title_re.search(source)
		if title:
			self.title = title.group(1)
					
		# tags
		
		self.tags = []
		tags_re = re.compile(r'tags="(.*?)"')
		tags = tags_re.search(source)
		if tags and tags.group(1) != '':
			self.tags = tags.group(1).split(' ')
					
		# creation date
		
		self.created = time.localtime()
		created_re = re.compile(r'created="(.*?)"')
		created = created_re.search(source)
		if created:
			self.created = decode_date(created.group(1))
		
		# modification date
		
		self.modified = time.localtime()
		modified_re = re.compile(r'modified="(.*?)"')
		modified = modified_re.search(source)
		if (modified):
			self.modified = decode_date(modified.group(1))
		
		# body text
		
		self.text = ''
		text_re = re.compile(r'<div.*?>(.*)</div>')
		text = text_re.search(source)
		if (text):
			self.text = decode_text(text.group(1))
				
		
	def to_html (self, author = 'twee'):
		"returns an HTML representation of this tiddler"
			
		now = time.localtime()
		output = '<div tiddler="' + self.title + '" tags="'
		
		for tag in self.tags:
			output += tag + ' '
			
		output = output.strip()
		output += '" modified="' + encode_date(self.modified) + '"'
		output += ' created="' + encode_date(self.created) + '"' 
		output += ' modifier="' + author + '">'
		output += encode_text(self.text) + '</div>'
		
		return output
		
		
	def to_twee (self):
		"returns a Twee representation of this tiddler"
		output = ':: ' + self.title
		
		if len(self.tags) > 0:
			output += ' ['
			for tag in self.tags:
				output += tag + ' '
			output = output.trim()
			
		output += "\n" + self.text + "\n\n\n"
		return output
		
		
	def to_rss (self, author = 'twee'):
		"returns an RSS representation of this tiddler"
		return rss.RSSItem(
			title = self.title,
			link = '',
			description = self.text,
			pubDate = datetime.datetime.now()
		)

		
#
# Helper functions
#


def encode_text (text):
	output = text
	output = output.replace('\\', '\s')
	output = output.replace('\n', '\\n')
	output = output.replace('<', '&lt;')
	output = output.replace('>', '&gt;')
	output = output.replace('"', '&quot;')
	
	return output

	
def decode_text (text):
	output = text
	output = output.replace('\\n', '\n')
	output = output.replace('\s', '\\')
	output = output.replace('&lt;', '<')
	output = output.replace('&gt;', '>')
	output = output.replace('&quot;', '"')
	
	return output
	
	
def encode_date (date):
	return time.strftime('%Y%m%d%H%M', date)
	

def decode_date (date):
	return time.strptime(date, '%Y%m%d%H%M')	