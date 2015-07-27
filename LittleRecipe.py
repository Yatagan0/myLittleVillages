
class LittleRecipe:
    def __init__(self, name):
        self.name = name
        self.timeMin = 1
        self.timeMax = 1
        self.transforming = []
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
r.transforming.append(["bed", "clean", "dirty"])
r.description = "dort"
allRecipes["sleep"] = r

r = LittleRecipe("eat")
r.timeMin = 30
r.timeMax = 60
r.description = "mange"
allRecipes["eat"] = r


r = LittleRecipe("work")
r.timeMin = 30
r.timeMax = 60
r.description = "travaille"
allRecipes["work"] = r

class workSlotType:
    def __init__(self, name):
        self.name = name

workSlotTypes = {}
