
class LittleRecipe:
    def __init__(self, name):
        self.name = name
        self.timeMin = 1
        self.timeMax = 1
        self.transformingStart = []
        self.transformingEnd = []
        self.description = name
        
        
specialWorks = ["move", "eat", "sleep", "manage", "buy", "sell"]
        
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

r = LittleRecipe("cook_carrots")
r.timeMin = 20
r.timeMax = 40
r.description = "cuisine une puree de carrottes"
r.transformingStart.append(["table", "clean","served"])
r.transformingStart.append(["carrots", "","delete"])
allRecipes[r.name] = r

r = LittleRecipe("cook_potatoes")
r.timeMin = 20
r.timeMax = 40
r.description = "cuisine un plat de patates"
r.transformingStart.append(["table", "clean","served"])
r.transformingStart.append(["potatoes", "","delete"])
allRecipes[r.name] = r

r = LittleRecipe("cook_salads")
r.timeMin = 20
r.timeMax = 40
r.description = "cuisine une salade"
r.transformingStart.append(["table", "clean","served"])
r.transformingStart.append(["salads", "","delete"])
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

r = LittleRecipe("buy")
r.timeMin = 10
r.timeMax = 20
r.description = ""
allRecipes[r.name] = r

r = LittleRecipe("sell")
r.timeMin = 10
r.timeMax = 20
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



r = LittleRecipe("plant_carrots")
r.timeMin = 60
r.timeMax = 2*60
r.description = "plante des carottes"
r.transformingStart.append(["field",  "clear", "planted-carrots"])
allRecipes[r.name] = r

r = LittleRecipe("weed_carrots")
r.timeMin = 60
r.timeMax = 2*60
r.description = "desherbe des carottes"
r.transformingStart.append(["field", "planted-carrots", "weeded-carrots"])
allRecipes[r.name] = r


r = LittleRecipe("reweed_carrots")
r.timeMin = 60
r.timeMax = 2*60
r.description = "desherbe des carottes"
r.transformingStart.append(["field", "weeded-carrots", "re-weeded-carrots"])
allRecipes[r.name] = r

r = LittleRecipe("recolt_carrots")
r.timeMin = 60
r.timeMax = 2*60
r.description = "recolte des carottes"
r.transformingStart.append(["field","re-weeded-carrots", "clear"])
r.transformingEnd.append(["carrots","new", ""])
allRecipes[r.name] = r


r = LittleRecipe("plant_salads")
r.timeMin = 60
r.timeMax = 2*60
r.description = "plante des salades"
r.transformingStart.append(["field",  "clear", "planted-salads"])
allRecipes[r.name] = r

r = LittleRecipe("weed_salads")
r.timeMin = 60
r.timeMax = 2*60
r.description = "desherbe des salades"
r.transformingStart.append(["field", "planted-salads", "weeded-salads"])
allRecipes[r.name] = r


r = LittleRecipe("reweed_salads")
r.timeMin = 60
r.timeMax = 2*60
r.description = "desherbe des salades"
r.transformingStart.append(["field", "weeded-salads", "re-weeded-salads"])
allRecipes[r.name] = r

r = LittleRecipe("recolt_salads")
r.timeMin = 60
r.timeMax = 2*60
r.description = "recolte des salades"
r.transformingStart.append(["field","re-weeded-salads", "clear"])
r.transformingEnd.append(["salads","new", ""])
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
t.recipes = ["eat", "cook", "clean_table", "cook_carrots", "cook_potatoes", "cook_salads"]
#~ t.objects = ["table", "clean"]
workSlotTypes [t.name] = t

t = workSlotType("field")
t.recipes = ["plant_potatoes", "weed_potatoes", "reweed_potatoes", "recolt_potatoes",
"plant_carrots", "weed_carrots", "reweed_carrots", "recolt_carrots",
"plant_salads", "weed_salads", "reweed_salads", "recolt_salads"]
#~ t.objects = ["table", "clean"]
workSlotTypes [t.name] = t

t = workSlotType("shop")
t.recipes = []#["buy", "sell"]
workSlotTypes [t.name] = t

