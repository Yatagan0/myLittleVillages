import math
import xml.etree.ElementTree as ET

start = "B.C.D.F.G.H.J.L.M.N.P.R.S.T.V.Qu.Ch.St"
start = start.split('.')
then = "a.e.i.o.u.on.ou.ai.en.in"
then = then.split('.')

allU = []
allL = []

for f in start:
    for t in then:
        allU.append((f+t))
        allL.append((f+t).lower())
        
        
def distance(p1, p2):
    #~ return 0
    return math.sqrt((p1[0] - p2[0])*(p1[0] - p2[0])+(p1[1] - p2[1])*(p1[1] - p2[1]))
    
global time
time = 0
def iterateTime():
    global time
    time += 1
    
#~ workshopName = {}
#~ workshopName["wood"] = "woodcutter"
#~ workshopName["stone"] = "stonecutter"
#~ workshopName["gold"] = "goldminer"
#~ workshopName["jewel"] = "jeweler"
#~ workshopName["warehouse"] = "warehouse"

def getMeanPos(posList):
    result = [0,0]
    if len(posList) == 0:
        return result
    
    for p in posList:
        result[0] += p[0]
        result[1] += p[1]
    result[0] = float(result[0])/len(posList)
    result[1] = float(result[1])/len(posList)
    return result
    
prestigeObjects = {}

cabane = {"prestige":10, "price":10}
prestigeObjects["hut"] = cabane

maison = {"prestige":40, "price":30}
prestigeObjects["house"] = maison

global allMaterials
allMaterials = {}

global allWorkshops
allWorkshops = {}

class productionData:
    def __init__(self, elem):
        self.produced = {}
        self.tools = {}
        self.needed = {}
        #~ self.time = int(elem.attrib["time"])
        
        for child in elem:
            if child.tag == "produced":
                self.produced[child.attrib["name"]] = int(child.attrib["quantity"])
                print "it produces ",self.produced[child.attrib["name"]] ," ", child.attrib["name"]
                

                
            if child.tag == "needed":
                self.needed[child.attrib["name"]] = int(child.attrib["quantity"])
                print "it needs ",self.needed[child.attrib["name"]] ," ", child.attrib["name"]



class workshopData:
    def __init__(self, elem):
        self.name = elem.attrib["name"]
        self.productions = []
        
        self.build = {}
        self.buildTime = 0
        
        
        for child in elem:
            if child.tag == "build":
                self.buildTime = int(child.attrib["time"])
                self.addBuild(child)
            if child.tag == "production":
                self.addProduction(child)
                
                
    def addBuild(self, elem):
        for child in elem:
            if child.tag == "material":
                self.build[child.attrib["name"]] = int(child.attrib["quantity"])
        
    def addProduction(self, elem):
        pd = productionData(elem)
        self.productions.append(pd)
        
        global allMaterials
        for p in pd.produced.keys():
            if not p in allMaterials.keys():
                allMaterials[p] = [self]
            else:
                allMaterials[p].append(self)
            
        
        
tree =  ET.parse("workshops.xml")
root = tree.getroot()
for child in root:
    wd = workshopData(child)

    global allWorkshops
    allWorkshops[wd.name] = wd
    
    #~ global allMaterial
    #~ allMaterial[wd.material] = wd
print allWorkshops

print allMaterials
