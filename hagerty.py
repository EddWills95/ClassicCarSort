import urllib2
import json
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from BeautifulSoup import BeautifulSoup

# Ebay Scraper (Needs Keywords) - Returns Av for results
def ebayScrape(keywords):
	try:
		api = Finding(siteid='EBAY-GB', appid='EddWilli-classicc-PRD-6246ab0a7-20318a15', config_file=None)
		api_request = {
			'keywords': '',
			'categoryId': '9801',
			'itemFilter': [
				{'name': 'Condition',
				 'value': 'Used'},
				{'name': 'Model Year',
				 'value': ''}
			],
			'sortOrder': 'CountryDescending',
		}

		api_request['keywords'] = keywords
		api_request['itemFilter'] = "{'name': 'Condition', 'value' : 'Used'}, { 'name' : 'ListingType', 'Value' : 'Classified' }"

		response = api.execute('findItemsAdvanced', api_request)

		# print type(response.reply.paginationOutput.totalEntries)

		average = 0
		amount = 0

		if int(response.reply.paginationOutput.totalEntries) > 0:
			# print dir(response.reply.searchResult.item)
			for i in response.reply.searchResult.item:
				# print "Title: %s // Price: %s" % (i.title, i.sellingStatus.currentPrice.value)
				average += float(i.sellingStatus.currentPrice.value)
				amount += 1
				return average / amount
		else:
			print "Nothing found on eBay"

	except ConnectionError as e:
		print(e)
		print(e.response.dict())

# Get data from Hagerty Insurance (Needs user input from hagInput)
def getDataFromHag(additional, t_f):

	string = 'http://apps.hagerty.com/ukvaluation/data/%s/index.json' % additional
	data = urllib2.urlopen(string)
	jsonData = ""
	for line in data:
		jsonData += line

	jsonData = jsonData[31: len(jsonData) - 2]

	tempJSON = json.loads(jsonData)

	hagFinalPrices = {}

	return tempJSON

# Much simpler Version to pull data from Hagerty. Returns JSON from URL
def hagertyExtract(urlString):
	try:
		raw = urllib2.urlopen(urlString)
		rawJson = ""
		for line in raw:
			rawJson += line

		rawJson = rawJson[31: len(rawJson) - 2]

		JSON = json.loads(rawJson)

		return JSON
	except urllib2.HTTPError as err:
		print "404 // Not Found"

# Extract Integer Values from acaFind. Returns High and Low Value
# def acaGetValues(x):
# 	stringTest = x
#
# 	stringTestNoComma = stringTest.replace(",", "")
#
# 	# stringTestNoDash = stringTestNoComma.replace(" - ", " ")
#
# 	index = stringTestNoComma.index(" - ")
#
# 	lowerNumber = stringTestNoComma[0 : index]
# 	higherNumber = stringTestNoComma[index+3 : len(stringTestNoComma)]
# 	return [int(lowerNumber), int(higherNumber)]

# Get data from Anglia Car Auction. Returns namesAndValues dictionary
def acaFind():

	acaRaw = urllib2.urlopen("http://www.angliacarauctions.co.uk/en/classic-auctions/latest-classic-car-catalogue/")

	soup = BeautifulSoup(acaRaw)

	namesAndValues = {}

	for x in soup.findAll("div", { "class" : "vehicle" } ):
		for y in x.findChildren("a", { "class" : "bottom" }):
			for k, j in zip(y.findChildren("h3"), y.findChildren("span", { "class" : "estimateValue" })):
				namesAndValues[k.text] = j.text

	# Removes Useless Ones
	for x in namesAndValues.keys():
		if namesAndValues[x] == []:
			del namesAndValues[x]

	# Only changing the length of the values that aren't Reserves
	for items in namesAndValues.keys():
		if namesAndValues[items] == "No Reserve" or namesAndValues[items] == "Tbc":
			pass
		else:
			namesAndValues[items] = namesAndValues[items][6:(len(namesAndValues[items]))]

	return namesAndValues

def getHagOptions(option):
	hagertyExtract(option)



# acaResults = acaFind()



# modelNames = hagertyExtract(modelsString)


# Compare Auction site with Hagerty Price

# This returns the two strings that match. It works!


hagString = 'http://apps.hagerty.com/ukvaluation/data/index.json'
rawModels = hagertyExtract(hagString)

acaList = []
for key in acaFind():
	acaList.append(key)

hagModelsList = []
for key in rawModels:
	hagModelsList.append(key)




# hagertyList = []
# for items in hagertyExtract(modelsString):
# 	hagertyList.append(items)

# for x in hagertyList:
# 	string = str(x)
# 	for y in acaList:
# 		if string in y:
# 			print "%s & %s" % (x, y)

# for key in acaFind():
# 	for x in hagertyExtract(hagString):
# 		string = x
# 		if string in key:
# 			print key
# 			noSpaceString = string.replace(" ", "")
# 			makeString = 'http://apps.hagerty.com/ukvaluation/data/%s/index.json' % noSpaceString
# 			print makeString
# 			newData = hagertyExtract(makeString)
# 			carry = noSpaceString + "/"
# 			for y in newData:
# 				string = y
# 				if string in key:
# 					noSpaceString = carry + string.replace(" ", "")
# 					modelString = 'http://apps.hagerty.com/ukvaluation/data/%s/index.json' % noSpaceString
# 					print modelString
# 					newData = hagertyExtract(modelString)
# 					carry = noSpaceString + "/"
# 					print newData
# 				elif string not in key:
# 					# modelString = 'http://apps.hagerty.com/ukvaluation/data/%sstandard/index.json' % carry
# 					# print modelString
# 					# newData = hagertyExtract(modelString)
# 					# carry = noSpaceString + "/"
# 					print "Not Sure"
# 				else:
# 					print "Not Found"

# def acaVhag(vehicle):
#
#
# for item in acaList:
# 	acaVhag(item)




# for key in acaFind():
# 	acaVhag(key)

				# else:
				# 	standard = "Standard"
				# 	noSpaceString = carry + standard
				# 	modelString = 'http://apps.hagerty.com/ukvaluation/data/%s/index.json' % noSpaceString
				# 	newData = hagertyExtract(modelString)
				# 	carry = noSpaceString + "/"
				# 	print newData
					# for j in newData:
					# 	string = j
					# 	if string in key:
					# 		print key
					# 		print "--"
					# 		print string
					# 		noSpaceString = carry + string.replace(" ", "")
					# 		noSpaceString = noSpaceString.replace(".", "")
					# 		modelString = 'http://apps.hagerty.com/ukvaluation/data/%s/index.json' % noSpaceString
					# 		newData = hagertyExtract(modelString)
					# 		carry = noSpaceString + "/"
					# 		print newData






# for items in acaResults:
# 	print "Item: %s \n Auction Price: %s \n eBay average: %s" % (items, acaResults[items], ebayScrape(items[4 : len(items)]))


