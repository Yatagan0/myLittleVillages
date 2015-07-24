
class LittleRecipe:
    def __init__(self, name):
        self.name = name
        self.timeMin = 1
        self.timeMax = 1
        self.transforming = []
        
        
allRecipes = {}

r = LittleRecipe("do nothing")
r.timeMin = 30
r.timeMax = 60
allRecipes["do nothing"] = r

r = LittleRecipe("sleep")
r.timeMin = 6*60
r.timeMax = 9*60
r.transforming.append(["bed", "clean", "dirty"])
allRecipes["sleep"] = r