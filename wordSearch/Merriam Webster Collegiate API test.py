import json
import requests

apiKey  = "c33d59f0-4576-4dfc-a389-918e5316421b"

word = input("Enter a word for search:")
print("Word entered:", word)
print("")

wordURL = "https://dictionaryapi.com/api/v3/references/collegiate/json/"+ word + "?key=" + apiKey

result = requests.get(wordURL)

print("Result status Code:", format(result.status_code))
print("")

jsonResult = json.dumps(result.json())

dictionaryResult = json.loads(jsonResult)

stems = [] #lists all of the entry's headwords, variants, inflections, undefined entry words, and defined run-on phrases. Each stem string is a valid search term that should match this entry.
partOfSpeeches = []
definitionResults = []
shortDefinitionResults = []

for i in range(0, len(dictionaryResult)):
    print("--------------------------------------------------------------------")
    print("Counter:", i)
    
    stemList = dictionaryResult[i].get('meta').get('stems')
    print("List of all of the entry's headwords, variants, inflections, undefined entry words, and defined run-on phrases. Each stem string is a valid search term that should match this entry:")
    
    for j in range(0, len(stemList)):
        print(str(j+1) + ". " + stemList[j])
        stems.append(stemList[j])

    print("")
    
    partOfSpeech = dictionaryResult[i].get('fl')
    print("Part of speech:", partOfSpeech)
    partOfSpeeches.append(partOfSpeech)

    print("")

    defList = dictionaryResult[i].get('def')
    for j in range(0, len(defList)):
        sseqList = defList[j].get('sseq')
        dtList = sseqList[0][0][1].get('dt')
        print("Definitions: ")
        print(str(j+1) + ". " + dtList[0][1]) 
        definitionResults.append(dtList[0][1])

    print("")
    
    shortdefList = dictionaryResult[i].get('shortdef')
    for j in range(0, len(shortdefList)):
        print("Short definitons: ")
        print(str(j+1) + ". " + shortdefList[j])
        shortDefinitionResults.append(shortdefList[j])

    print("")
