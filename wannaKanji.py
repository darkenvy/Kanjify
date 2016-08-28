# -*- coding: utf-8 -*-



#--------------Basics-----------------#

#from nltk.stem.lancaster import LancasterStemmer
#st = LancasterStemmer()
from nltk.stem.porter import PorterStemmer
import sys, os

st = PorterStemmer()

punctuation = ['.','!','?',',',')',']','"',"'",'-']
lineCount = 0
dicList = []
oneItem = []



#---Import Wordlist into Dictionary---#

def importDicFile(hddFilename):
	global dicList, oneItem
	wordfile = open(hddFilename, 'r')
	# This commend opens the user editable version
	#wordfile = open('kanji.txt', 'r')

	for line in wordfile:
		for item in line.split(','):
			oneItem.append(item.strip())
			#print item
		dicList.append(oneItem)
		oneItem = []
	
	#print dicList
	wordfile.close()



#---Export Dic Obj to file & rootify---#

def stemAndExport():
	global dicList
	exportWordfile = open('kanji-root.txt', 'w')

	for each in dicList:
		for subEach in each:
			if subEach == each[0]:
				#exportWordfile.write( st.stem(subEach.rstrip('\n')) + '\n')
				exportWordfile.write( subEach.rstrip('\n') )
			else:
				exportWordfile.write( ',' + st.stem(subEach.rstrip('\n')) )
		exportWordfile.write('\n')
	
			
	exportWordfile.close()



#-------------Convertion--------------#

def listCheck(word):
	global dicList
	# commonList Now includes ePub syntax 
	commonList = [
		'body','div','class','alt','meta','content','name','type',
		'a','an','as','at','be','by','can','do','get','go','good',
		'he','how','if','in','it','its','my','no','now','of','or',
		'see','so','take','the','to','use','we','well'
		]
	
	#############################################################
	#															#
	#						Comparison							#
	#															#
	#############################################################
	
	def checkAllSubs(current):
		for i in range(0, len(current)):
			if word.lower() == current[i].rstrip('\n').lower():
				#print word + " -> " + current[0]
				return 1

			

	
	# Check if word is in the commonList. If so, ignore it. If not, check the big list. Saves cycles.	
	if word not in commonList:
		for i in range(0, len(dicList)):
			if checkAllSubs( dicList[i] ) == 1:
				#print dicList[i][0]
				#break
				return dicList[i][0]
			if (i == len(dicList)-1) and (checkAllSubs( dicList[i] ) != 1):
				#print word
				#break
				return 0
			
				


#---------------Main----------------#

def main(fileName):
	global lineCount
	book = open( fileName[0] + "." + fileName[1] , 'r')
	outputFile = open( fileName[0] + ".kanji." + fileName[1] ,'w')




	# Strips the front punctuation if it exists. Return new word after stemming
	def frontPunctuationCheck(word):
		if word[:1] in punctuation:
			return st.stem(word)[1:]
		else:
			return st.stem(word)




	for line in book:
		cleanedWord = ""
		
		# Check the last character of the word for punctuation. Strip it!
		# If it's a regular word, simply pass it onto cleanedWord and send it on it's way
		for word in line.split():
			if word[-1] in punctuation:
			#if word[len(word)-1] in punctuation:
				cleanedWord = frontPunctuationCheck( word[:-1].decode('utf8') )
			else:
				cleanedWord = frontPunctuationCheck( word.decode('utf8') )
			
			
			#############################################################
			#															#
			#						File Output							#
			#															#
			#############################################################
			
			# Listcheck returns the Kanji OR 0 if it doesn't mind a match
			theMatchedWord = listCheck( cleanedWord )
			# Write to terminal window as well as the outputFile object
			if theMatchedWord != 0 and theMatchedWord != None:
				'''
				sys.stdout.write( str(theMatchedWord) + word + " " )
				outputFile.write( str(theMatchedWord) + word + " " )
				'''
				sys.stdout.write( str(theMatchedWord) + word + " " )
				outputFile.write( str(theMatchedWord) + word + " " )
			else:
				sys.stdout.write( word + " " )
				outputFile.write( word + " " )
		sys.stdout.write( "\n" )
		outputFile.write( "\n" )
			
				




	book.close()
	outputFile.close()

#----------------Main-----------------#

print "\n-------------"
print "Wanna-Kanjify"
print "-------------"
print "\nPlease select an option:"
print "1) Main Function\n2) Prepare Kanji Dictionary"

userInput = int(raw_input("Choice: "))



if userInput == 1:
	
	print "Note: The file needs to be in the same directory"
	print "You may drag and drop a file onto the window"
	fileName = str(raw_input("Filename (eg: book.txt): ")).rstrip(" ")
	fileName = fileName.replace('\ ', ' ')
	fileName = fileName.split('.')
	
	# Check if the input is even a file. If not, stop the script!
	if not os.path.exists( fileName[0] + "." + fileName[1] ):
		print fileName[0] + "." + fileName[1]
		print "File does not exist."
		print "Please note that filenames are case-sensitive."
		quit()
	
	# Check if the output file exists, if it does, delete it
	if os.path.exists( fileName[0] + ".kanji." + fileName[1] ):
		print "File exists; Deleting old output.txt; Proceeding"
		os.remove( fileName[0] + ".kanji." + fileName[1] )
	
	# Now the regular procedure
	importDicFile('kanji-root.txt')
	main( fileName )
	
	
	
elif userInput == 2:
	
	# This converts kanji.txt to kanji-root.txt
	importDicFile('kanji.txt')
	stemAndExport()
	print "Kanji Dictionary Stemming Complete"
	
else:
	print "You must have not typed a proper option :/"

