def __docs__():
	'''
	This is the extractor module. When given a string, it will extract the command and application name, and return them as a list.
	It assumes some basic settings:
		Default browser: Mozilla Firefox.
		Text editor: Gedit.
		IDE: Visual Studio Code.
		Terminal: Gnome-terminal.
	'''
import csv
from fuzzywuzzy import fuzz

class extractor():
	'''This is the extractor class.'''
	def __init__(self):
		self.applications = [['firefox','browser','mozilla-firefox','mozilla'],['gedit','text-editor'],['code','ide','visual-studio-code','vs-code'],['gnome-terminal','terminal']]
		code_shortcuts_file = open("./vaac/data/code_keyboard_shortcuts.csv") #Hardcoded string
		self.code_keyboard_shortcuts = list(csv.reader(code_shortcuts_file))
		firefox_shortcuts_file = open("./vaac/data/firefox_keyboard_shortcuts.csv") #Hardcoded string
		self.firefox_keyboard_shortcuts = list(csv.reader(firefox_shortcuts_file))
		gedit_shortcuts_file = open("./vaac/data/gedit_keyboard_shortcuts.csv") #Hardcoded string
		self.gedit_keyboard_shortcuts = list(csv.reader(gedit_shortcuts_file))
		terminal_shortcuts_file = open("./vaac/data/terminal_keyboard_shortcuts.csv") #Hardcoded string
		self.terminal_keyboard_shortcuts = list(csv.reader(terminal_shortcuts_file))
		self.map = {"code":self.code_keyboard_shortcuts,"firefox":self.firefox_keyboard_shortcuts,"gedit":self.gedit_keyboard_shortcuts,"terminal":self.terminal_keyboard_shortcuts}

	def extract(self,string,current_app):
		new_app = "?"
		for i in range(len(self.applications)):
			for app in self.applications[i]:
				if app in string:
					new_app = self.applications[i][0]					
					string = string.replace(app,'')					
					break
		
		print("current",current_app,"new",new_app)
		if new_app != "?" or current_app == "":
			current_app = new_app
		max_ratio = 0
		i = 0
		n = 0
		for line in self.map[current_app]:
			r = fuzz.ratio(string,line[0])			
			pr = fuzz.partial_ratio(string,line[0])			
			tr = fuzz.token_sort_ratio(string,line[0])			
			tsr = fuzz.token_set_ratio(string,line[0])			

			current_match_ratio = max(r,pr,tr,tsr)
			if current_match_ratio > max_ratio:							
				max_ratio = current_match_ratio
				n = i
			
			i+=1		
		
		return current_app,self.map[current_app][n]



