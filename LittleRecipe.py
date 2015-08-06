
class LittleRecipe:
    def __init__(self, name):
        self.name = name
        self.timeMin = 1
        self.timeMax = 1
        self.transformingStart = []
        self.transformingEnd = []
        self.description = name
        
        
allRecipes = {}

r = LittleRecipe("do nothing")
r.timeMin = 30
r.timeMax = 60
r.description = "ne fait rien"
allRecipes["do nothing"] = r

r = LittleRecipe("sleep")
r.timeMin = 6*60
r.timeMax = 9*60
r.transformingStart.append(["bed", "clean", "dirty"])
#~ r.transformingEnd.append(["bed", "used", "dirty"])
r.description = "dort"
allRecipes["sleep"] = r

r = LittleRecipe("clean_room")
r.timeMin = 15
r.timeMax = 30
r.transformingStart.append(["bed", "dirty", "clean"])
r.description = "nettoie une chambre"
allRecipes[r.name] = r


r = LittleRecipe("eat")
r.timeMin = 30
r.timeMax = 60
r.description = "mange"
r.transformingStart.append(["table", "served", "dirty"])
allRecipes[r.name] = r

r = LittleRecipe("cook")
r.timeMin = 20
r.timeMax = 40
r.description = "cuisine"
r.transformingStart.append(["table", "clean","served"])
allRecipes[r.name] = r

r = LittleRecipe("clean_table")
r.timeMin = 5
r.timeMax = 15
r.description = "nettoie une table"
r.transformingStart.append(["table",  "dirty", "clean"])
allRecipes[r.name] = r


r = LittleRecipe("work")
r.timeMin = 30
r.timeMax = 60
r.description = "travaille"
allRecipes["work"] = r


r = LittleRecipe("move")
r.timeMin = 0
r.timeMax = 0
r.description = ""
allRecipes[r.name] = r

r = LittleRecipe("manage")
r.timeMin = 60
r.timeMax = 2*60
r.description = ""
allRecipes[r.name] = r

r = LittleRecipe("build")
r.timeMin = 30
r.timeMax = 90
r.description = "construit un batiment"
allRecipes[r.name] = r


r = LittleRecipe("plant_potatoes")
r.timeMin = 60
r.timeMax = 2*60
r.description = "plante des patates"
r.transformingStart.append(["field",  "clear", "planted-potatoes"])
allRecipes[r.name] = r

r = LittleRecipe("weed_potatoes")
r.timeMin = 60
r.timeMax = 2*60
r.description = "desherbe des patates"
r.transformingStart.append(["field", "planted-potatoes", "weeded-potatoes"])
allRecipes[r.name] = r


r = LittleRecipe("reweed_potatoes")
r.timeMin = 60
r.timeMax = 2*60
r.description = "desherbe des patates"
r.transformingStart.append(["field", "weeded-potatoes", "re-weeded-potatoes"])
allRecipes[r.name] = r

r = LittleRecipe("recolt_potatoes")
r.timeMin = 60
r.timeMax = 2*60
r.description = "recolte des patates"
r.transformingStart.append(["field","re-weeded-potatoes", "clear"])
r.transformingEnd.append(["potatoes","new", ""])
allRecipes[r.name] = r


class workSlotType:
    def __init__(self, name):
        self.name = name
        self.recipes=[]
        self.objects = []

workSlotTypes = {}

t = workSlotType("room")
t.recipes = ["sleep", "clean_room"]
#~ t.objects = [["bed", "clean"]]
workSlotTypes [t.name] = t

t = workSlotType("table")
t.recipes = ["eat", "cook", "clean_table"]
#~ t.objects = ["table", "clean"]
workSlotTypes [t.name] = t

t = workSlotType("field")
t.recipes = ["plant_potatoes", "weed_potatoes", "reweed_potatoes", "recolt_potatoes"]
#~ t.objects = ["table", "clean"]
workSlotTypes [t.name] = t
