import math

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
    
    
    
    
prestigeObjects = {}

cabane = {"prestige":10, "price":10}
prestigeObjects["hut"] = cabane

maison = {"prestige":40, "price":30}
prestigeObjects["house"] = maison
