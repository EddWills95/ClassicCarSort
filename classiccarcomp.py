import urllib2
import json
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from BeautifulSoup import BeautifulSoup


def hagertyextract(urlstring):
    try:
        raw = urllib2.urlopen(urlstring)
        rawJson = ""
        for line in raw:
            rawJson += line

        rawJson = rawJson[31: len(rawJson) - 2]

        JSON = json.loads(rawJson)

        hagertyList = []

        for item in JSON:
            hagertyList.append(item)

        return hagertyList

    except urllib2.HTTPError as err:
        print err

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

def mercFix(acaDict):
    for key in acaDict:
        if "Mercedes" in key:
            string = key
            # print string
            string = string.replace("-Benz", "")
            string = string.replace("Benz ", "")
            string = string.replace("Mercedes", "Mercedes-Benz")
            acaDict[string] = acaDict.pop(key)
def vwFix(acaDict):
    for key in acaDict:
        if "VW" in key:
            string = key
            string = string.replace("VW", "Volkswagen")
            acaDict[string] = acaDict.pop(key)

    def cycleHag(car, listIn):
        if any(word in car.split() for word in listIn):
            print "In"
# def bmwFix(acaDict):
#     for key in acaDict:
#         if "M635 CSi" in key:
#             string = key
#             string = string.replace("M635 CSi", "M635CSi")
#             acaDict[string] = acaDict.pop(key)

hagString = 'http://apps.hagerty.com/ukvaluation/data/index.json'

makeList = hagertyextract(hagString)

auctionDict = acaFind()

mercFix(auctionDict)
vwFix(auctionDict)

def messWithString(step):
    addString = step
    addString = addString.replace("-", "")
    addString = addString.replace(" ", "")
    return addString

def loopThrough(queryList, item, carry=""):
    print ""
    print queryList
    print item
    print carry
    print ""
    if len(queryList) != 1:
        # Go through the initial Makes from Hagerty
        for query in queryList:
            # Check to see if any of the makes are in the Name(items)
            if query in item:
                if carry != "":
                    carry += "/"
                stringAdd = "%s" % (carry + messWithString(query))
                stringURL = "http://apps.hagerty.com/ukvaluation/data/%s/index.json" % stringAdd
                print stringURL
                returnThing = hagertyextract(stringURL)
                if returnThing == "None":
                    "Not Sure"
                else:
                    return returnThing, stringAdd.replace(" ", "")
    else:
        if carry != "":
            carry += "/"
        stringAdd = "%s" % (carry + queryList[0])
        stringURL = "http://apps.hagerty.com/ukvaluation/data/%s/index.json" % stringAdd
        print stringURL
        returnThing = hagertyextract(stringURL)
        if returnThing == "None":
            "Not Sure"
        else:
            return returnThing, stringAdd.replace(" ", "")


auctionList = []

for keys in auctionDict:
    auctionList.append(keys)

models, carry = loopThrough(makeList, auctionList[1])

def bmwFiX(listChange):
    for item in listChange:
        index = listChange.index(item)
        if item == "3.0CS":
            listChange[index] = "3.0 CS"
        if item == "3.0CSi":
            listChange[index] = "3.0 CSi"
        if item == "M635CSi":
            listChange[index] =  "M635 CSi"
        if item == "3.0CSL":
            listChange[index] = "3.0 CSL"
bmwFiX(models)

spec, carry = loopThrough(models, auctionList[1], carry)

spec2, carry = loopThrough(spec, auctionList[1], carry)

year = loopThrough(spec2, auctionList[1], carry)

print loopThrough(year, auctionList[1], carry)





