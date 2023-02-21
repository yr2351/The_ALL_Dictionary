from apiclient.discovery import build

apiKey = "AIzaSyCB-M_Z2BlLfWgAMOuhLmNHHmoBoRCme50"
searchEngineID = "4c4e5dd8e9cf81ff8"

resource = build("customsearch", "v1", developerKey=apiKey).cse()

word = input("Enter a word for search:")
print("Word entered:", word)
print("")

results = resource.list(q=word, cx=searchEngineID, searchType='image').execute()

resultURL = results.get('url').get('template')

print('URL of searched results:')
print(resultURL)
print("")

imageDataSet = results.get('items')

print("-------------------------------------")
print("Items:")

for i in range(0, len(imageDataSet)):
    print("About image", str(i+1) + ":")
    print("")
    
    print('Kind:')
    print(imageDataSet[i].get('kind'))
    print("")

    print('Title:')
    print(imageDataSet[i].get('title'))
    print("")

    print('HTML Title:')
    print(imageDataSet[i].get('htmlTitle'))
    print("")

    print('Link:')
    print(imageDataSet[i].get('link'))
    print("")

    print('Display Link:')
    print(imageDataSet[i].get('displayLink'))
    print("")

    print('Snippet:')
    print(imageDataSet[i].get('snippet'))
    print("")

    print('HTML snippet:')
    print(imageDataSet[i].get('htmlSnippet'))
    print("")

    print('Mime:')
    print(imageDataSet[i].get('mime'))
    print("")

    print('File format:')
    print(imageDataSet[i].get('fileFormat'))
    print("")

    image = imageDataSet[i].get('image')

    print('Context Link:')
    print(image.get('contextLink'))
    print("")
    
    print('Height:')
    print(image.get('height'))
    print("")

    print('Width:')
    print(image.get('width'))
    print("")

    print('Byte size:')
    print(image.get('byteSize'))
    print("")

    print('Thumbnail Link:')
    print(image.get('thumbnailLink'))

    print('Thumbnail Height')
    print(image.get('thumbnailHeight'))
    print("")

    print('ThumbnailWidth')
    print(image.get('thumbnailWidth'))
    print("")
    print("-------------------------------------")
    print("")
