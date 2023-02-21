from udpy import UrbanClient

client = UrbanClient()

word = input("Enter a word for search:")
print("Word entered:", word)
print("")

definitions = client.get_definition(word)

i = 0
for lexis in definitions:
    i = i + 1
    print("Definition " + str(i) + ":")
    print(lexis.definition)
    print("")
    
    print("Example " + str(i) + ":")
    print(lexis.example)
    print("")

print("Link for the results searched:", "https://www.urbandictionary.com/define.php?term="+word)
