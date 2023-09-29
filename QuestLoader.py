import os, json, glob

#Defines
quests = []
monsterMap = {
    "boar":1,
    "suzy":2
}
locationMap={
    "greatrock":1,
    "daisywoods":2
}
itemMap={
    "boarmeat":1
}
giverQuestIdMap={
}
givers=["borris","chalice"]
for npc in givers:
    giverQuestIdMap[npc] = -1
#end defines

#Quest classes
class Slay:
    def __init__(self, name,giver : str,description,monster : str,count, minLevel, requires):
        self.Name = name
        self.Giver = giver.lower()
        self.GiverQuestId = giverQuestIdMap[giver]
        self.Description = description
        self.MonsterId = monsterMap[monster.lower()]
        self.Count = count
        self.MinLevel = minLevel
        self.Requires = requires

class Provide:
    def __init__(self, name, giver : str, description, item : str, count, minLevel, requires):
        self.Name = name
        self.Giver = giver.lower()
        self.GiverQuestId = giverQuestIdMap[giver]
        self.Description = description
        self.ItemId = itemMap[item.lower()]
        self.Count = count
        self.MinLevel = minLevel
        self.Requires = requires

class Travel:
    def __init__(self, name, giver : str, description, location : str, minLevel, requires):
        self.Name = name
        self.Giver = giver.lower()
        self.GiverQuestId = giverQuestIdMap[giver]
        self.Description = description
        self.LocationId = locationMap[location.lower()]
        self.MinLevel = minLevel
        self.Requires = requires
#end quest classes

# begin fill quests
jsonFiles = glob.glob("*Quests.json")
for file in jsonFiles:
    fr = open(file, 'r')
    giver = file.removesuffix("Quests.json").lower()
    jsonData = json.loads(fr.read())
    for quest in jsonData["Quests"]:
        giverQuestIdMap[giver] += 1
        if quest["Type"] == "Slay":
            quests.append(Slay(quest["Name"],giver,quest["Description"]
                               ,quest["Monster"],quest["Count"], quest["MinLevel"], quest["Requires"]))
        elif quest["Type"] == "Provide":
            quests.append(Provide(quest["Name"],giver,quest["Description"]
                                  ,quest["Item"],quest["Count"], quest["MinLevel"], quest["Requires"]))
        elif quest["Type"] == "Travel":
            quests.append(Travel(quest["Name"],giver,quest["Description"]
                                 ,quest["Location"], quest["MinLevel"], quest["Requires"]))
    fr.close()

# end fill quests

# begin create verse

with open('QuestLoader.verse','w') as f:
    f.write("quest_loader<public> := class{var Quests<public> : []quest = array{};GetQuests<public>():[]quest={return Quests};Init<public>():void={")
    for quest in quests:
        f.write("set Quests += array{")
        if isinstance(quest, Slay):
            f.write(f'''MakeBKSlayQuest("{quest.Name}","{quest.Giver}",{quest.GiverQuestId},"{quest.Description}",{quest.MonsterId},{quest.Count},{quest.MinLevel},"{quest.Requires}")''')
        elif isinstance(quest, Provide):
            f.write(f'''MakeBKProvideQuest("{quest.Name}","{quest.Giver}",{quest.GiverQuestId},"{quest.Description}",{quest.ItemId},{quest.Count},{quest.MinLevel},"{quest.Requires}")''')
        elif isinstance(quest, Travel):
            f.write(f'''MakeBKTravelQuest("{quest.Name}","{quest.Giver}",{quest.GiverQuestId},"{quest.Description}",{quest.LocationId},{quest.MinLevel},"{quest.Requires}")''')
        f.write("};")
    f.write('}')
    f.write('}')

# end create verse