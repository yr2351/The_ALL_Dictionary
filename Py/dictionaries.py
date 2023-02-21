import json
import requests
from apiclient import discovery
from GoogleNews import GoogleNews
from udpy import UrbanClient
import wikipediaapi
from youtubesearchpython import VideosSearch
import asyncio
import time


async def youtubeDict(word):
    # print("start youtube")

    await asyncio.sleep(0)

    output = ""

    videosSearch = VideosSearch(word)

    results = videosSearch.result()

    resultList = results['result']

    titles = [sub['title'] for sub in resultList]


    """
    These parts are not needed.
    It may cause errors if the channel did not set its profile picture.
    channelPictureInfoList = [sub['thumbnails'] for sub in channels]
    channelPictureInfo = channelPictureInfoList[0]
    channelPictureURLs = [sub['url'] for sub in channelPictureInfo]
    """

    links = [sub['link'] for sub in resultList]

    for i in range(0, 3):
        link = links[i].replace("watch?v=", "embed/", 1)
        output +="<h5>Title: " + titles[i] + "</h5>"
        output += "<iframe width=\'50%\' height=\'250px\' src=\"" + link +"\"></iframe></br></br>"
    
    # print("fin youtube")

    return output

async def mwcDict(word):
    # print("start mwc")

    await asyncio.sleep(0)

    output = ""

    apiKey  = "c33d59f0-4576-4dfc-a389-918e5316421b"
    
    wordURL = "https://dictionaryapi.com/api/v3/references/collegiate/json/"+ word + "?key=" + apiKey

    result = requests.get(wordURL)

    jsonResult = json.dumps(result.json())

    dictionaryResult = json.loads(jsonResult)

    stems = [] #lists all of the entry's headwords, variants, inflections, undefined entry words, and defined run-on phrases. Each stem string is a valid search term that should match this entry.
    partOfSpeeches = []
    definitionResults = []
    shortDefinitionResults = []

    try:
        stemList = dictionaryResult[0].get('meta').get('stems')
            
        partOfSpeech = dictionaryResult[0].get('fl')
        output +="Part of speech: " + partOfSpeech  + "</br>"
        partOfSpeeches.append(partOfSpeech)
        
        shortdefList = dictionaryResult[0].get('shortdef')
        output +="Short definitons: " + "</br>"
        for j in range(0, len(shortdefList)):
            output += str(j+1) + ". " + shortdefList[j] + "</br>"
            shortDefinitionResults.append(shortdefList[j])
    except:
        return "No result"
    
    # print("fin mwc")

    return output

async def mwlDict(word):
    # print("start mwl")

    await asyncio.sleep(0)

    output = ""

    apiKey  = "c0fe6dc9-3217-4825-b6ad-fac424c7d7b3"

    wordURL = "https://dictionaryapi.com/api/v3/references/learners/json/"+ word + "?key=" + apiKey
    result = requests.get(wordURL)

    jsonResult = json.dumps(result.json())

    dictionaryResult = json.loads(jsonResult)

    stems = [] #lists all of the entry's headwords, variants, inflections, undefined entry words, and defined run-on phrases. Each stem string is a valid search term that should match this entry.
    partOfSpeeches = []
    definitionResults = []
    shortDefinitionResults = []

    try:
        stemList = dictionaryResult[0].get('meta').get('stems')
            
        partOfSpeech = dictionaryResult[0].get('fl')
        output +="Part of speech: " + partOfSpeech  + "</br>"
        partOfSpeeches.append(partOfSpeech)
        
        shortdefList = dictionaryResult[0].get('shortdef')
        output +="Short definitons: " + "</br>"
        for j in range(0, len(shortdefList)):
            output += str(j+1) + ". " + shortdefList[j] + "</br>"
            shortDefinitionResults.append(shortdefList[j])
    except:
        return "No result"
    
    # print("fin mwl")

    return output

async def googleImageDict(word):
    # print("start google image")

    await asyncio.sleep(0)

    output = ""
    apiKey = "AIzaSyCB-M_Z2BlLfWgAMOuhLmNHHmoBoRCme50"
    searchEngineID = "4c4e5dd8e9cf81ff8"

    resource = discovery.build("customsearch", "v1", developerKey=apiKey).cse()
    results = resource.list(q=word, cx=searchEngineID, searchType='image').execute()

    imageDataSet = results.get('items')

    # 페이스북 자료만 안나옴

    for i in range(0, 3):
        title = imageDataSet[i].get('title')
        image = imageDataSet[i].get('image')
        
        if title[-10:] == '| Facebook':
            link = image.get('thumbnailLink')
            width = '30%'
        else:
            link = imageDataSet[i].get('link')
            width = '50%'
        contextLink = image.get('contextLink')
        output += "<h5>"+ title +"</h5>"
        output += "<a href=\'" + contextLink + "\' height=\'5\' width=\'10\'><img src=\' "+ link +" \' alt=\'context link.\' width = "+ width +" height=\'auto\'></a></br></br>"
    
    # output += "Full URL: <a href = \"" + resultURL + "\">" + resultURL + "</a><br>"
    # print("fin google image")

    return output

async def googleNewsDict(word):
    # print("start google news")

    await asyncio.sleep(0)
    output = ''

    googlenews = GoogleNews(lang='en')
    
    googlenews.search(word)

    result = googlenews.result()

    if len(result) == 0:
        return "No result"
    elif len(result) > 5:
        n = 5
    else:
        n = len(result)

    for i in range(n):
        res = result[i]
        link = res['link']
        title = res['title']
        output += '<a href=\'' + link + '\'>' + title + '</a><br>'
    
    # print("fin google news")

    return output[:-1]

async def oxfordDict(word):
    # print("start oxford")

    await asyncio.sleep(0)
    output = ""
    appID  = "501e439d"
    appKey  = "f7bd8a4c25db428d6b1f972d3acc85d7"
    endPoint = "entries"
    languageCode = "en-us"

    wordURL = "https://od-api.oxforddictionaries.com/api/v2/" + endPoint + "/" + languageCode + "/" + word.lower()

    try:
        result = requests.get(wordURL, headers = {"app_ID": appID, "app_Key": appKey})


        jsonResult = json.dumps(result.json())

        dictionaryResult = json.loads(jsonResult)

        realResultList = dictionaryResult["results"]
        realResultDict = realResultList[0]

        resultInfoList = realResultDict["lexicalEntries"]
        resultInfoDict = resultInfoList[0]
        resultDataList = resultInfoDict["entries"]
        resultDataDict = resultDataList[0]


        wordSensesList = resultDataDict["senses"]

        wordResult = {}
        for dict in wordSensesList:
            for list in dict:
                if list in wordResult:
                    wordResult[list] += (dict[list])
                else:
                    wordResult[list] = dict[list]

        output += "Definitions:"+ "<br>"
        definitionList = wordResult.get("definitions")
        
        if definitionList == None:
            return "No result"

        for i in range(0, len(definitionList)):
            output += str(i+1) + ". " + definitionList[i] + "<br>"
        output += "<br>"

        output += "Examples: "+ "<br>"
        exampleList = wordResult.get("examples")
        if exampleList == None:
            output += "No example" + "<br>"
        else:
            for i in range(0, len(exampleList)):
                output += str(i+1) + ". " + exampleList[i].get("text") +"<br>"
        
        # print('fin oxford')
        
        return output[:-1]
    except:
        return "No result"

async def urbanDict(word):
    # print("start urban ")

    await asyncio.sleep(0)
    try:
        output = ""
        client = UrbanClient()
        definitions = client.get_definition(word)

        if len(definitions) == 0:
            return "No result"
        elif len(definitions) > 3:
            n = 3
        else:
            n = len(definitions)

        for i in range(0, n):
            lexis = definitions[i]
            output += "Definition " + str(i + 1) + ":<br>"
            output += lexis.definition + "<br>"
            
            output += "Example " + str(i + 1) + ": <br>"
            output += lexis.example + "<br>"
        output += "<br>"
        link = "https://www.urbandictionary.com/define.php?term="+word
        output += "Full URL: <a href = \"" + link + "\">" + link + "</a><br>"

        return output

    except:
        return "No result"
    
    # print("fin urban")

async def wikiDict(word):
    # print("start wiki")
    await asyncio.sleep(0)
    output = ""

    wikiResult = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)
    wikiPage = wikiResult.page(word)
    if wikiPage.summary == "":
        return "No result"

    output += "Page - Summary: " + wikiPage.summary +"<br>"
    output += "<br>"
    output += "Full URL: <a href = \"" + wikiPage.fullurl + "\">" + wikiPage.fullurl + "</a><br>"

    # print("fin wiki")
    return output

# def hello(word):
#     start = time.time()
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     tasks = mwlDict(word), mwcDict(word), oxfordDict(word), googleImageDict(word), googleNewsDict(word), urbanDict(word), wikiDict(word), youtubeDict(word)
#     mwl, mwc, oxford, googleImage, googleNews, urban, wiki, youtube = loop.run_until_complete(asyncio.gather(*tasks))
#     loop.close()
#     fin = time.time()
#     print(googleImage)
#     return fin-start

# print(hello('info'))
