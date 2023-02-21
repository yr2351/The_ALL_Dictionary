import json
import requests

appID  = "501e439d"
appKey  = "f7bd8a4c25db428d6b1f972d3acc85d7"
endPoint = "entries"
languageCode = "en-us"

word = input("Enter a word for search:")
print("Word entered:", word)
print("")

wordURL = "https://od-api.oxforddictionaries.com/api/v2/" + endPoint + "/" + languageCode + "/" + word.lower()

result = requests.get(wordURL, headers = {"app_ID": appID, "app_Key": appKey})

print("Code:", format(result.status_code))
print("")

jsonResult = json.dumps(result.json())

dictionaryResult = json.loads(jsonResult)

realResultList = dictionaryResult["results"]
realResultDict = realResultList[0]

resultInfoList = realResultDict["lexicalEntries"]
resultInfoDict = resultInfoList[0]

wordDerivativesList = resultInfoDict["derivatives"]
wordDerivativesDict = wordDerivativesList[0]
print("Derivatives:", wordDerivativesDict.get("text"))
print("")

wordCategoryList = resultInfoDict["lexicalCategory"]
print("Lexical category:", wordCategoryList.get("text"))
print("")

resultDataList = resultInfoDict["entries"]
resultDataDict = resultDataList[0]

wordEtymologiesList = resultDataDict["etymologies"]
wordEtymologies = wordEtymologiesList[0]
print("Etymologies:", wordEtymologies)
print("")

wordNotesList = resultDataDict["notes"]
wordNotesDict = wordNotesList[0]
wordNotes = wordNotesDict.get("text")
print("Notes:",wordNotes)
print("")

wordPronunciationsList = resultDataDict["pronunciations"]
wordPronunciationsDict = wordPronunciationsList[0]
wordDialects = wordPronunciationsDict.get("dialects")
print("Dialects:", wordDialects)
print("")

wordPhoneticNotation = wordPronunciationsDict.get("phoneticNotation")
print("Phonetic notation:", wordPhoneticNotation)
print("")

wordPhoneticSpelling = wordPronunciationsDict.get("phoneticSpelling")
print("Phonetic spelling:", wordPhoneticSpelling)
print("")

wordSensesList = resultDataDict["senses"]

wordResult = {}
for dict in wordSensesList:
    for list in dict:
        if list in wordResult:
            wordResult[list] += (dict[list])
        else:
            wordResult[list] = dict[list]

print("Definitions:")
definitionList = wordResult.get("definitions")
for i in range(0, len(definitionList)):
    print(str(i+1) + ".", definitionList[i])
print("")

print("Examples:")
exampleList = wordResult.get("examples")
for i in range(0, len(exampleList)):
    print(str(i+1) + ".", exampleList[i].get("text"))
print("")

print("Short Definitions:")
shortDefinitionList = wordResult.get("shortDefinitions")
for i in range(0, len(shortDefinitionList)):
    print(str(i+1) + ".", shortDefinitionList[i])
print("")

print("Subsenses:")
subSensesList = wordResult.get("subsenses")

otherResults = {}
for dict in subSensesList:
    for list in dict:
        if list in otherResults:
            otherResults[list] += (dict[list])
        else:
            otherResults[list] = dict[list]

print("Other definitions:")
otherDefinitionList = otherResults.get("definitions")
for i in range(0, len(otherDefinitionList)):
    print(str(i+1) + ".", otherDefinitionList[i])
print("")

print("Other examples:")
otherExampleList = otherResults.get("examples")
for i in range(0, len(otherExampleList)):
    print(str(i+1) + ".", otherExampleList[i].get("text"))
print("")

print("Short Definitions:")
otherShortDefinitionList = otherResults.get("shortDefinitions")
for i in range(0, len(otherShortDefinitionList)):
    print(str(i+1) + ".", otherShortDefinitionList[i])
print("")

print("")
