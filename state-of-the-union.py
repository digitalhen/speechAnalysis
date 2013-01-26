# Project 1 for JMSC6041
# Copyright Henry Williams 2013
# All Rights Reserved
# Sunday 20th January 2013

import csv, re, string, math
from collections import Counter
from optparse import OptionParser

# Read command line options
parser = OptionParser()
parser.add_option("-y", "--year", dest="yearToPrint", help="print data for YEAR only", metavar="YEAR")
parser.add_option("-d", "--startDecade", dest="startDecade", help="begin printing result with the DECADE decade", metavar="DECADE")
parser.add_option("-t", "--top", dest="topTermsNumber", help="return the NUMBER results", metavar="NUMBER")
(options, args) = parser.parse_args()

# This calculates the TF-IDF for a group of objects. It prefers the TF dictionary is in 
# position 2 in the group.
def calcTfIdf ( tfGroup, idfDict ):
	for tfMember in tfGroup:
		tfData = tfGroup[tfMember]
		tfDict = tfData[2]
		
		for key in tfDict:
			tfDict[key] = tfDict[key] * idfDict[key]
		
	return

# This calculates the IDF for a given dictionary against a provided document count.
# idfDict is essentially a master word list for a number of documents.
def calcIdf ( documentCount, idfDict ):
	for key in idfDict:
		idfDict[key] = math.log(documentCount / idfDict[key])
		
# This method takes a bunch of text and returns it all in lower case, with no weird
# characters and tokenised in to a list based on spaces.
def cleanTokenizeText ( text ):
	lowerText = text.lower()
	cleanText = re.sub('[^A-Za-z\n ]+', '', lowerText)
	wordList = re.split('\W+', cleanText)
	
	return wordList
	
	
# This is a dictionary wrapper that allow you to increment the value if the key already
# else it adds it with a value of 1.
def addOrIncrementDict ( key, myDict ):
	if key in myDict:
		myDict[key] += 1
	else:
		myDict[key] = 1
	
	return
	
# This is a dictionary wrapper that allows for summing the values of dictionaries without
# overwriting values
def addOrSumDict ( dictA, dictB ):
	for key in dictB:
		if key in dictA:
			dictA[key] += dictB[key]
		else:
			dictA[key] = dictB[key]
	
	return
	
def sort_nicely( l ): 
  # Python is pretty poor at sorting numerics stored as text, so I've used this handy
  # human sorting method from: http://nedbatchelder.com/blog/200712/human_sorting.html#comments 
  convert = lambda text: int(text) if text.isdigit() else text 
  alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
  l.sort( key=alphanum_key ) 

# handle large data - the speeches
csv.field_size_limit(1000000)

#list to hold a list for each year
years = {};

#list to hold master list of words
masterDict = {}

#total document count
docCount = 0

with open('state-of-the-union.csv', 'rb') as csvfile:
	unionreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in unionreader:
		# Increment doc count
		docCount += 1
	
		# This section, by way of functions, does the following for each speech:
		# 	1. Lowers the case
		#	2. Cleans the punctuation away
		#	3. Regexs the text to remove white space to tokenize it
		#	4. Creates a set - a unique list of words
		
		wordList = cleanTokenizeText ( row[1] )
		uniqueWordList = set(wordList)
		
		# Then we create a dictionary and process each word in the unique list and get its count
				
		wordDict = dict()
		
		for word in uniqueWordList:
			# Count the instances in this speech, divide it by the number of words = term frequency
			
			wordDict[word] = float(wordList.count(word)) / len(wordList)
			
			addOrIncrementDict ( word, masterDict )
		
		# This section captures the year, the word count, and the counted word list for each year
		year = row[0]
		yearData = [row[0], len(row[1]), wordDict]
		
		# And then appends it to the "years" master list.
		# Since some years have multiple speeches - eg. 1790 - we need to check if we already have a year first.
		# If it does, we append a version number to the year, so we don't lose the old data.
		if year in years:
			i = 1
			year = year + '-' + str(i)
			while year in years:
				i += 1
				
		years[year] = yearData

# Now process the final document count in to IDF
calcIdf ( docCount, masterDict )

# Now process it against the years, and calculate the TF-IDF
calcTfIdf ( years, masterDict )

# Read a command line parameter for an individual year, else think about decades
if options.yearToPrint:
	year = options.yearToPrint
	
	if year in years:
		yearData = years[options.yearToPrint]
		yearDict = yearData[2]
	
		# sort the items based on the dictionary values (not key)
		sortedYearItems = sorted(yearDict.iteritems(), key=lambda item: -item[1])
	
		# variable to control how many top items to print
		if options.topTermsNumber:
			# TODO: This should check if it's an int, but for now will presume it is
			topN = int(options.topTermsNumber)
		else:
			topN = 20
	
		# get on with printing
		print "Top " + str(topN) + " terms for " + str(year)
	 
		for item in sortedYearItems[:topN]:
			print item
	else:
		print year + " was not found!"
else:
	# read the command line variable for the year & decade to begin with
	if options.startDecade:
		startDecade = options.startDecade
	else:
		startDecade = "0"

	# Group by decade and print out total results
	sortedYears = sorted(years, key=years.get)
	
	# Begin processing the decades and summing the dictionary results
	decade = "0"
	decades = {}
	decadeDict = {}
	for year in sortedYears:
		if int(year[:3]) < int(startDecade[:3]):
			#TODO: Possible needs to be made numeric with modulo.
			continue			
		if year[:3] != decade[:3]:
			# It's a new decade so start new calculations. 
			decade = year[:3] + "0"
			decadeDict = {}
	
		# Merge the dictionaries.
		yearData = years[year]
		yearDict = yearData[2]
	
		addOrSumDict ( decadeDict, yearDict )
		decades[decade] = decadeDict
	
	# Sort the decades, then sort them nicely in to human readable order.
	sortedDecades = sorted(decades, key=decades.get)
	sort_nicely(sortedDecades)
		
	# Process each decade, sort the contents and figure out what are the top 20 items.
	for decade in sortedDecades:
		decadeDict = decades[decade]
		sortedDecadeItems = sorted(decadeDict.iteritems(), key=lambda item: -item[1])
	
		# variable to control how many top items to print
		if options.topTermsNumber:
			# TODO: This should check if it's an int, but for now will presume it is
			topN = int(options.topTermsNumber)
		else:
			topN = 20
	
		# Get on with printing
		print "Top " + str(topN) + " terms for " + decade + "s"
	 
		for item in sortedDecadeItems[:topN]:
			print item 
