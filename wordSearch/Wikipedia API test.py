import wikipediaapi

wikiResult = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)

word = input("Enter a word for search: ")

print("Word entered:", word)
print("")

wikiPage = wikiResult.page(word)
print("Page - Exists: %s" % wikiPage.exists())
print("")

print("Page - Title: %s" % wikiPage.title)
print("")

print("Page - Summary: %s" % wikiPage.summary)
print("")

print("Full URL:", wikiPage.fullurl)
print("")

print("Canonical URL:", wikiPage.canonicalurl)
print("")

print(wikiPage.text)

wikiHTML = wikipediaapi.Wikipedia(language='en',extract_format=wikipediaapi.ExtractFormat.HTML)

wikiHTMLPage = wikiHTML.page(word)
print(wikiHTMLPage.text)
