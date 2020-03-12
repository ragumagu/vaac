import sqlite3
import csv

def __docs__():
	'''
	This is the classifier module. You can use this to classify commands, and get their translated key events.

	Usage:
		1. First populate the vaac.db with the input file. Use vaac/data/input for linux and vaac/data/input_windows for windows.
			By default, the db will have linux keyboard commands. You can pass any csv file to populate() with appropriate to fill the 				db.
		2. Translator class can be used to translate commands to keys.
	TODO:
		# Add classifier class. Should be initialized with input text, and should return translated text with classification.
	'''

def populate(fileName="./vaac/data/input"): #Hardcoded default. 
	"""Fills the vaac.db file with command, keys pairs in commands table."""
	connection = sqlite3.connect('./vaac/data/vaac.db') #Hardcoded.
	c = connection.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS commands(command text, key text)''')
	
	inputFile = open(fileName,'r')
	reader = csv.reader(inputFile)

	for line in reader:		
		c.execute('''INSERT INTO commands VALUES ('{0}','{1}')'''.format(line[0],line[1]))

	connection.commit()
	connection.close()

class translator():	
	"""Translator object to translate commands to keys."""
	def __init__(self):
		"""On initialization, a connection to the local Sqlite3 db is set up."""
		self.connection = sqlite3.connect('./vaac/data/vaac.db') #Hardcoded.
		self.c = self.connection.cursor()	
	
	def translate(self, inputString): 		
		"""Translates the commands to keys, by searching for inputString in vaac.db."""
		query = '''SELECT * from commands where command = '{0}' '''.format (inputString)	
		self.c.execute(query)
		data = self.c.fetchone()
		if data:				
			return data[1]
		else:
			return "?"		
