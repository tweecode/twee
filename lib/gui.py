#
# gui.py
#
# This handles the project window and menus.
#

import os, sys, wx, urllib
from project import Project
import tiddlywiki

ID_HELP = 101
ID_GOOGLE_GROUP = 102

ID_NEW_PROJECT = 103
ID_OPEN_PROJECT = 104
ID_SAVE_PROJECT = 105
ID_SAVE_PROJECT_AS = 106

ID_ADD_SOURCE = 107
ID_REMOVE_SOURCE = 108
ID_BUILD = 109
ID_PROOF = 110

ID_TARGET_CHOICE = 201
ID_SAVEAS_BUTTON = 202
ID_BUILD_BUTTON = 203
ID_ADD_BUTTON = 204


class ProjectWindow (wx.Frame):

	#
	# constructors
	#

	def __init__ (self, parent):
	
		# restore our config and recently-opened files
		
		self.config = wx.Config('Tweebox')
		self.recentFiles = wx.FileHistory(5)
		self.recentFiles.Load(self.config)
	
		# get a new Project object
		
		self.project = Project()
		self.fileName = ''
		self.dirty = False

		# create the window

		wx.Frame.__init__(self, parent, wx.ID_ANY, 'Untitled Project', \
						  size = (550, 250), style = wx.CLOSE_BOX | wx.CAPTION | wx.SYSTEM_MENU | wx.MINIMIZE_BOX)
		self.addMenus()		
		self.addControls()
		self.CreateStatusBar()
				
		# show our window
	
		self.Centre()
		self.Show(True)
		
		# try opening the most recent project
		
		if self.recentFiles.GetCount() > 0:
			self.fileName = self.recentFiles.GetHistoryFile(0)
			self.loadFile(failLoudly = False)
			
		
	def addMenus (self):
	
		# create menus

		helpMenu = wx.Menu()
		helpMenu.Append(wx.ID_ABOUT, '&About Tweebox')
		helpMenu.Append(ID_HELP, 'Tweebox &Help')
		helpMenu.Append(ID_GOOGLE_GROUP, 'Discuss Twee Online')
		
		fileMenu = wx.Menu()
		self.fileNewItem = fileMenu.Append(ID_NEW_PROJECT, '&New Project\tCtrl-N')
		self.fileOpenItem = fileMenu.Append(ID_OPEN_PROJECT, '&Open Project...\tCtrl-O')
		fileMenu.AppendSeparator()
		self.fileSaveItem = fileMenu.Append(ID_SAVE_PROJECT, '&Save Project\tCtrl-S')
		self.fileSaveAsItem = fileMenu.Append(ID_SAVE_PROJECT_AS, 'S&ave Project As...')
		fileMenu.AppendSeparator()
		self.fileQuitItem = fileMenu.Append(wx.ID_EXIT, '&Exit\tCtrl-Q')
		self.recentFiles.UseMenu(fileMenu)
		self.recentFiles.AddFilesToMenu()

		projectMenu = wx.Menu()
		self.projectAddItem = projectMenu.Append(ID_ADD_SOURCE, 'Add Source File...')
		self.projectRemoveItem = projectMenu.Append(ID_REMOVE_SOURCE, 'Remove Source File')
		projectMenu.AppendSeparator()
		self.projectBuildItem = projectMenu.Append(ID_BUILD, '&Build Story\tCtrl-B')
		self.projectProofItem = projectMenu.Append(ID_PROOF, '&Proof Story\tCtrl-P')
		
		# create menu bar
		
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu, '&File')
		menuBar.Append(projectMenu, '&Project')
		menuBar.Append(helpMenu, '&Help')
		self.SetMenuBar(menuBar)		

		# add menu events
		
		wx.EVT_UPDATE_UI(self, -1, self.updateUI)
		
		wx.EVT_MENU(self, wx.ID_ABOUT, self.onAbout)
		wx.EVT_MENU(self, ID_HELP, self.onHelp)
		wx.EVT_MENU(self, ID_GOOGLE_GROUP, self.onGoogleGroup)
		wx.EVT_MENU(self, ID_NEW_PROJECT, self.onNew)
		wx.EVT_MENU(self, ID_OPEN_PROJECT, self.onOpen)
		wx.EVT_MENU(self, ID_SAVE_PROJECT, self.onSave)
		wx.EVT_MENU(self, ID_SAVE_PROJECT_AS, self.onSaveAs)
		wx.EVT_MENU(self, wx.ID_EXIT, self.onQuit)
		wx.EVT_MENU(self, wx.ID_FILE1, self.onOpenRecent)
		wx.EVT_MENU(self, wx.ID_FILE2, self.onOpenRecent)
		wx.EVT_MENU(self, wx.ID_FILE3, self.onOpenRecent)
		wx.EVT_MENU(self, wx.ID_FILE4, self.onOpenRecent)
		wx.EVT_MENU(self, wx.ID_FILE5, self.onOpenRecent)
		wx.EVT_MENU(self, ID_ADD_SOURCE, self.onAddSource)
		wx.EVT_MENU(self, ID_REMOVE_SOURCE, self.onRemoveSource)
		wx.EVT_MENU(self, ID_BUILD, self.onBuild)
		wx.EVT_MENU(self, ID_PROOF, self.onProof)


	def addControls (self):
		panel = wx.Panel(self)
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		panel.SetSizer(mainSizer)
		
		# sources on the left half
		
		sourcesPanel = wx.Panel(panel)
		sourcesBox = wx.StaticBox(sourcesPanel, wx.ID_ANY, 'Source Files')
		sourcesSizer = wx.StaticBoxSizer(sourcesBox, wx.VERTICAL)
		sourcesPanel.SetSizer(sourcesSizer)
		
		self.sourcesList = wx.ListBox(sourcesPanel)
		self.addButton = wx.Button(sourcesPanel, ID_ADD_BUTTON, 'Add')
		wx.EVT_BUTTON(self, ID_ADD_BUTTON, self.onAddSource)
		
		sourcesSizer.Add(self.sourcesList, 1, wx.EXPAND)
		sourcesSizer.Add(self.addButton, 0, wx.TOP | wx.ALIGN_RIGHT, 8)
		
		# story file stuff on the right half
		
		storyPanel = wx.Panel(panel)
		storyBox = wx.StaticBox(storyPanel, wx.ID_ANY, 'Story File')
		storySizer = wx.StaticBoxSizer(storyBox, wx.VERTICAL)
		storyPanel.SetSizer(storySizer)
		
		# file destination row
		
		saveAsPanel = wx.Panel(storyPanel)
		saveAsSizer = wx.BoxSizer(wx.HORIZONTAL)
		saveAsPanel.SetSizer(saveAsSizer)
		
		self.saveAsText = wx.StaticText(saveAsPanel, wx.ID_ANY, 'Save As:')																			
		self.saveAsButton = wx.Button(saveAsPanel, ID_SAVEAS_BUTTON, 'Set')								 
		wx.EVT_BUTTON(self, ID_SAVEAS_BUTTON, self.onSetDestination)
		
		saveAsSizer.Add(self.saveAsText, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)
		saveAsSizer.Add(self.saveAsButton, 0, wx.TOP | wx.BOTTOM, 8)

		storySizer.Add(saveAsPanel, 0, wx.EXPAND, 0)
		
		# target row

		targetPanel = wx.Panel(storyPanel)
		targetSizer = wx.BoxSizer(wx.HORIZONTAL)
		targetPanel.SetSizer(targetSizer)
		
		self.targetLabel = wx.StaticText(targetPanel, wx.ID_ANY, 'Story Format:')

		self.targetChoice = wx.Choice(targetPanel, ID_TARGET_CHOICE, \
									  choices = ('Sugarcane', 'Jonah', 'TiddlyWiki 2', 'TiddlyWiki 1.2'))
		self.targetChoice.SetSelection(0)
																																
		wx.EVT_CHOICE(self, ID_TARGET_CHOICE, self.onChangeTarget)
		
		targetSizer.Add(self.targetLabel, 1, wx.TOP | wx.BOTTOM, 10)
		targetSizer.Add(self.targetChoice, 1, wx.TOP | wx.BOTTOM, 8)
		
		storySizer.Add(targetPanel, 0, wx.ALL | wx.EXPAND, 0)
		
		# add our halves to the main panel
		
		mainSizer.Add(sourcesPanel, 1, wx.ALL | wx.EXPAND, 8)
		mainSizer.Add(storyPanel, 1, wx.ALL | wx.EXPAND, 8)
				
	#
	# utility functions
	#

	def updateUI (self, event):		
		if self.sourcesList.GetSelection() == wx.NOT_FOUND:
			self.projectRemoveItem.Enable(False)
		else:
			self.projectRemoveItem.Enable(True)
			
		if self.sourcesList.IsEmpty():
			self.projectBuildItem.Enable(False)
			self.projectProofItem.Enable(False)
		else:
			self.projectBuildItem.Enable(True)
			self.projectProofItem.Enable(True)
			
			
	def updateTitle (self):
		if self.fileName == '':
			title = 'Untitled Project'
		else:
			bits = os.path.splitext(self.fileName)
			title = os.path.basename(bits[0])
			
		self.SetTitle('Tweebox - ' + title)
		
	
	def updateDestination (self):
		label = 'Save As: '
		
		if self.project.destination != '':
			label += os.path.basename(self.project.destination)
		
		self.saveAsText.SetLabel(label)
		
		
	def closeProject (self):
		if self.dirty:
			bits = os.path.splitext(self.fileName)
			title = os.path.basename(bits[0])

			message = 'Close ' + title + ' without saving changes?'
			dialog = wx.MessageDialog(self, message, 'Save Changes', \
									  wx.ICON_QUESTION | wx.YES_NO | wx.NO_DEFAULT)
			return (dialog.ShowModal() == wx.ID_YES)
		else:
			return True
			

	def targetToReadable (self, target):
		if target == 'sugarcane':
			return 'Sugarcane'
		
		if target == 'jonah':
			return 'Jonah'
			
		if target == 'tw2':
			return 'TiddlyWiki 2'
			
		if target == 'tw':
			return 'TiddlyWiki 1.2'
		
	
	def readableToTarget (self, readable):
		if readable == 'Sugarcane':
			return 'sugarcane'
		
		if readable == 'Jonah':
			return 'jonah'
			
		if readable == 'TiddlyWiki 2':
			return 'tw2'
			
		if readable == 'TiddlyWiki 1.2':
			return 'tw'
			
	#
	# event handlers
	#

	def onAbout (self, event):
		info = wx.AboutDialogInfo()
		info.SetName('Tweebox')
		info.SetVersion('2.1')
		info.SetDescription('\nA tool for creating interactive stories\nwritten by Chris Klimas\n\nhttp://gimcrackd.com/etc/src/')
		info.SetCopyright('The Twee compiler and associated JavaScript files in this application are released under the GNU Public License.\n\nThe files in the targets directory are derivative works of Jeremy Ruston\'s TiddlyWiki project and are used under the terms of its license.')
		wx.AboutBox(info)

		
	def onHelp (self, event):
		wx.LaunchDefaultBrowser('http://gimcrackd.com/etc/doc/')

		
	def onGoogleGroup (self, event):
		wx.LaunchDefaultBrowser('http://groups.google.com/group/tweecode')


	def onNew (self, event):
		if (self.closeProject()):
			self.project = Project()
			self.fileName = ''
			self.dirty = True
			self.updateTitle()
			self.updateDestination()
			self.sourcesList.Clear()
			
			
	def onOpen (self, event):
		if (self.closeProject()):
			dialog = wx.FileDialog(self, 'Open Project', os.getcwd(), "", \
								   "Tweebox Project (*.twp)|*.twp", \
								   wx.OPEN | wx.FD_CHANGE_DIR)
													 	 
			if dialog.ShowModal() == wx.ID_OK:
				self.fileName = dialog.GetPath()
				self.loadFile()
				self.recentFiles.AddFileToHistory(self.fileName)
				
			dialog.Destroy()
				
	def onOpenRecent (self, event):		
		if event.GetId() == wx.ID_FILE1:
		  index = 0
		elif event.GetId() == wx.ID_FILE2:
		  index = 1
		elif event.GetId() == wx.ID_FILE3:
		  index = 2
		elif event.getId() == wx.ID_FILE4:
		  index = 3
		elif event.getId() == wx.ID_FILE5:
		  index = 4
			 
		self.fileName = self.recentFiles.GetHistoryFile(index)
		self.loadFile()

	def loadFile (self, failLoudly = True):
		try:
			self.project = Project(self.fileName)
		except:
			if failLoudly:
				wx.MessageBox('Can\'t open ' + self.fileName + '. Make sure this file has not been moved ' + \
				  		      'or deleted, and that you are able to read files in this location.', \
							  'Can\'t Open File', wx.ICON_ERROR)
			return
				
		self.dirty = False
		
		# sync UI to file contents
						
		self.updateTitle()
		self.updateDestination()
		self.sourcesList.Clear()
		
		for source in self.project.sources:
			self.sourcesList.Append(os.path.basename(source))
		
		target = self.targetToReadable(self.project.target)
		self.targetChoice.SetStringSelection(target)		


	def displayError (self, activity):
		exception = sys.exc_info()
		text = 'An error occurred while ' + activity + ' ('
		text += str(exception[1]) + ').'
		
		error = wx.MessageDialog(self, text, 'Error', wx.OK | wx.ICON_ERROR)
		error.ShowModal()
		

	def onSaveAs (self, event):
		dialog = wx.FileDialog(self, 'Save Project', os.getcwd(), "", \
							   "Tweebox Project (*.twp)|*.twp", \
		 					   wx.SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_CHANGE_DIR)
		
		if dialog.ShowModal() == wx.ID_OK:
			self.fileName = dialog.GetPath()
			self.updateTitle()
			self.onSave(event)
			
		dialog.Destroy()
			

	def onSave (self, event):
		if self.fileName != '':
			try:
				self.project.save(self.fileName)
				self.dirty = False
			except:
				self.displayError('saving your project')
		else:
			self.onSaveAs(event)


	def onQuit (self, event):
		if self.closeProject():
			self.recentFiles.Save(self.config)
			self.Close(True)
		

	def onAddSource (self, event):
		dialog = wx.FileDialog(self, 'Add Source File', os.getcwd(), "", \
							   "Twee source code (*.tw)|*.tw|Plain text files (*.txt)|*.txt", wx.OPEN | wx.FD_CHANGE_DIR)
		
		if dialog.ShowModal() == wx.ID_OK:
			path = dialog.GetPath()
			self.project.sources.append(path)
			self.sourcesList.Append(os.path.basename(path))
			self.dirty = True
			
		dialog.Destroy()


	def onRemoveSource (self, event):
		index = self.sourcesList.GetSelection()
		self.project.sources.pop(index)
		self.sourcesList.Delete(index)
		self.dirty = True
		
		
	def onChangeTarget (self, event):
		target = self.targetChoice.GetStringSelection()
		self.project.target = self.readableToTarget(target)
		self.dirty = True
		

	def onSetDestination (self, event):
		dialog = wx.FileDialog(self, 'Save Story As', os.getcwd(), "", \
	  						   "Web Page (*.html)|*.html", \
							   wx.SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_CHANGE_DIR)
		
		if dialog.ShowModal() == wx.ID_OK:
			path = dialog.GetPath()
			self.project.destination = path
			self.dirty = True
			self.updateDestination()
			dialog.Destroy()
			return True
			
		dialog.Destroy()
		return False		

				
	def onBuild (self, event):	
		if self.project.destination == '':
			if not self.onSetDestination(event):
				return
				
		self.SetStatusText('Building your story...')
	
		try:
			if self.project.build():
				path = 'file://' + urllib.pathname2url(self.project.destination)
				path = path.replace('file://///', 'file:///')
				wx.LaunchDefaultBrowser(path)	
				self.SetStatusText('Your story has been successfully built.')
		except:
			 self.displayError('building your story')
			 self.SetStatusText('')

	def onProof (self, event):	
		if self.project.destination == '':
			if not self.onSetDestination(event):
				return
				
		self.SetStatusText('Building proofing copy...')
	
		try:
			if self.project.proof():	
				self.SetStatusText('Your proofing copy has been successfully built.')
		except:
			 self.displayError('building a proofing copy of your story')
			 self.SetStatusText('')