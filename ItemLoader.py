import os, json, glob

#Defines
items = []
#end defines

#Item classes

#end Item classes

# begin fill Items
jsonFiles = glob.glob("*Items.json")
for file in jsonFiles:
    fr = open(file, 'r')
    jsonData = json.loads(fr.read())
    for item in jsonData["Items"]:
        pass
    fr.close()

# end fill Items

# begin create verse

with open('ItemLoader.verse','w') as f:
    f.write("item_loader<public> := class{var Items<public> : []item = array{};GetItems<public>():[]item={return Items};Init<public>():void={")
    for item in items:
        pass
    f.write('}')
    f.write('}')

# end create verse