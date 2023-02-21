from youtubesearchpython import VideosSearch
import json

word = input("Enter a word for search:")
print("Word entered:", word)
print("")

videosSearch = VideosSearch(word)

results = videosSearch.result()

resultList = results['result']

types = [sub['type'] for sub in resultList]
ids = [sub['id'] for sub in resultList]
titles = [sub['title'] for sub in resultList]
publishedTimes = [sub['publishedTime'] for sub in resultList]
durations = [sub['duration'] for sub in resultList]

viewCounts = [sub['viewCount'] for sub in resultList]
views = [sub['text'] for sub in viewCounts]
viewsShortened = [sub['short'] for sub in viewCounts]

thumbNails = [sub['thumbnails'] for sub in resultList]
richThumbnails = [sub['richThumbnail'] for sub in resultList]
descriptionSnippets = [sub['descriptionSnippet'] for sub in resultList]

channels = [sub['channel'] for sub in resultList]
channelNames = [sub['name'] for sub in channels]

"""
These parts are not needed.
It may cause errors if the channel did not set its profile picture.
channelPictureInfoList = [sub['thumbnails'] for sub in channels]
channelPictureInfo = channelPictureInfoList[0]
channelPictureURLs = [sub['url'] for sub in channelPictureInfo]
"""

channelLinks = [sub['link'] for sub in channels]

accessibilities = [sub['accessibility'] for sub in resultList]
links = [sub['link'] for sub in resultList]
shelfTitles = [sub['shelfTitle'] for sub in resultList]

for i in range(0, len(resultList)):
    print("Type:", types[i])
    print("ID:", ids[i])
    print("Title:", titles[i])
    print("Published Time:", publishedTimes[i])
    print("Duration:", durations[i])
    
    print("View counts:", views[i])
    print("View counts (shortened):", viewsShortened[i])
    
    print("Thumbnail:", thumbNails[i])
    print("Rich thumbnail:", richThumbnails[i])
    print("Description Snippet:", descriptionSnippets[i])
    
    print("Channel name:", channelNames[i])
    print("Channel link:", channelLinks[i])
    
    print("Accessibility:", accessibilities[i])
    print("Link:", links[i])
    print("Shelf-title:", shelfTitles[i])
    print("")
