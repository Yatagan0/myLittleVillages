# -*- coding: utf-8 -*-

import random, math
import xml.etree.ElementTree as ET

seasonIndex = 0


consonnes = "B.C.D.F.G.H.J.L.M.N.P.R.S.T.V.Qu.Ch.St.Tr.Pr.Cr.Sc"
consonnes = consonnes.split('.')
voyelles = "a.e.i.o.u.on.ou.ai.en.in"
voyelles = voyelles.split('.')

consonnesDoubles = "ss.ll.rr.rt"
consonnesDoubles = consonnesDoubles.split('.') + consonnes
voyellesFinVille = "ac.es.art.ant.eaux.e.and.as.ard"
voyellesFinVille = voyellesFinVille.split('.')

voyellesFinNom = "es.art.ant.eaux.e.and.ot.er.ard"
voyellesFinNom = voyellesFinNom.split('.')


finVille = ["touille", "mont", "vert", "gny","lieu", "guen", "fort", "puy"]
finNom = [ "mont", "vert",  "leaux", "lieu", "guen"]
prenoms = ["Ahmed","Albert","Alexandre","Andre","Antoine","Arnaud","Augustin", "Basile", "Benoit",
"Bertrand","Charles", "Christophe","Claude","Clement","Damien","Denis","Dominique",
"Edouard","Emile","Etienne","Fabrice","Ferdinand", "Fernand","Florent", "Florian", "Francois", "Gabriel", 
"Gautier","Germain","Georges","Gregoire","Guillaume", "Guy", "Henri","Jacques","Jean", 
"Joel", "Jonas","Joseph", "Julien","Laurent","Leon","Louis","Luc","Lucas","Manuel", "Matthieu", "Martin", 
"Mickael","Michel","Nicolas", "Olivier","Paul","Pierre","Philippe", 
"Rene", "Robert", "Ronan","Sylvain", "Thimotee","Thomas", "Tristan","Vincent", "William"]

def isNameOk(name):
    if name.find("uu") > -1:
        return False
    if name.find("nll") > -1:
        return False
    if name.find("nrr") > -1:
        return False
    if name.find("nrt") > -1:
        return False
    if name.find("nss") > -1:
        return False 
    if len(name) > 12:
        return False
        
    return True

def randomName():
    s= random.choice(consonnes)+random.choice(voyelles)
    r = random.randint(0, 2)
    #~ print r
    if r == 2:
        #~ print "rare"
        r = random.randint(0,2) #very long names are rares
        #~ print r
    for i in range(0, r):
        s +=random.choice(consonnesDoubles).lower()+random.choice(voyelles)
    r = random.randint(0, 4)
    if r < 1:
        s += random.choice(finVille)
    else:
        s +=random.choice(consonnesDoubles).lower()+random.choice(voyellesFinNom)
    if(not isNameOk(s)):
        #~ print s, " not ok"
        return randomName()
    s = random.choice(prenoms)+" "+s
    return s
    
    
def randomCityName():
    s = random.choice(consonnes)+random.choice(voyelles)
    r = random.randint(0, 2)
    if r == 2:
        r = random.randint(0, 2) #very long names are rares
    for i in range(0, r):
        s +=random.choice(consonnes).lower()+random.choice(voyelles)
        
    r = random.randint(0, 2)
    if r < 1:
        s += random.choice(finVille)
    else:
        s +=random.choice(consonnesDoubles).lower()+random.choice(voyellesFinVille)
    if(not isNameOk(s)):
        return randomCityName()
    return s
    
def randomRestaurantName(owner=""):
    if owner == "":
        owner = random.choice(prenoms)
    else:
        owner = owner.split(" ")[0]
        
    names = [["jardin", "delice", "bouchon", "grill", "troquet", "rendez-vous", "diner", "cuisinier", 
    "estaminet","coutelas", "pain", "jambon", "fromage", "bistrot","regal", "gosier"],
                    ["table", "fourchette", "causerie", "marmite", "cuisine", "assiette",  "escapade",
                    "brasserie", "tartine", "reverie", "escale", "pause", "auberge", "taverne"]]
                    
    namesOwner = ["tonton", "l'oncle", "le cousin", "papy", "le capitaine", "le chef", "maitre"]
    au = ["Au ", "A la ", "A l'"]
    le = ["Le ", "La ", "L'"]
 
        
    cases = ["chez", "au", "le", "au", "le", "le"]
    case = random.choice(cases)
    if case == "chez":
        adj = ""
        if random.randint(0,1) == 0:
            adj = random.choice(namesOwner)+" "
        return "Chez "+adj+owner
        
        
    nameGenre = random.randint(0,1)
    
    myname = random.choice(names[nameGenre])
        
    if case == "au":
        if myname[0] in ["a", "e", "i", "o", "u", "y"]:
            myau = au[2]
        else: myau = au[nameGenre] 
        finalName = myau+myname
    elif case == "le":
        if myname[0] in ["a", "e", "i", "o", "u", "y"]:
            myau = le[2]
        else: myau = le[nameGenre] 
        finalName = myau+myname
        
    cases = ["de", "adjectif", "du", "rien"]
    case = random.choice(cases)
    
    if case == "de":
        adj = " de "
        if random.randint(0,1) == 0:
            no = random.choice(namesOwner)
            if no[0:3] == "le ":
                no = " du "+no[3:]
                adj = ""
            adj += no+" "
        elif owner[0] in ["A", "E", "I", "O", "U", "Y"]:
            adj= " d'"
        finalName += adj+owner
    elif case == "adjectif":
        adj = {}
        adj["merveilleux"] = "merveilleuse"
        adj["magique"] = ""
        adj["gastronomique"] = ""
        adj["enchante"] = "enchantee"
        adj["gourmand"] = "gourmande"
        adj["lointain"] = "lointaine"
        adj["traditionnel"] = "traditionnelle"
        adj["delicat"] = "delicate"
        adj["succulent"] = "succulente"
        adj["délicieux"] = "délicieuse"
        adj["juteux"] = "juteuse"
        aa = random.choice(adj.keys())
        if adj[aa] != "" and (nameGenre==1 or nameGenre==3) :
            aa = adj[aa]
        finalName += " "+aa
    elif case == "du":
        toadd = ["des lutins", "des familles", "du gourmet", "de chez nous", "d'antan", "du printemps",
        "des amis", "du port", "de la gare", "du centre", "des reves", "du pays"]
        aa = random.choice(toadd)
        finalName += " "+aa
        
    return finalName
    
    
    
def randomHotelName(owner=""):
    if owner == "":
        owner = random.choice(prenoms)
    else:
        owner = owner.split(" ")[0]
        
    names = [["jardin", "delice", "lit", "repos", "dortoir", "oreiller", "reve", "abri", "hotel", "matelas", "berceau", "drap", "couffin", "silence"],
                    ["escapade", "escale", "pause", "auberge", "auberge de jeunesse", "couette", "plume", "hotellerie"]]
                    
    namesOwner = ["tonton", "l'oncle", "le cousin", "papy", "le capitaine", "le jeune"]
    au = ["Au ", "A la ", "A l'"]
    le = ["Le ", "La ", "L'"]
 
        
    cases = ["chez", "au", "le", "au", "le", "le"]
    case = random.choice(cases)
    if case == "chez":
        adj = ""
        if random.randint(0,1) == 0:
            adj = random.choice(namesOwner)+" "
        return "Chez "+adj+owner
        
        
    nameGenre = random.randint(0,1)
    
    myname = random.choice(names[nameGenre])
        
    if case == "au":
        if myname[0] in ["a", "e", "i", "o", "u", "y", "h"]:
            myau = au[2]
        else: myau = au[nameGenre] 
        finalName = myau+myname
    elif case == "le":
        if myname[0] in ["a", "e", "i", "o", "u", "y", "h"]:
            myau = le[2]
        else: myau = le[nameGenre] 
        finalName = myau+myname
        
    cases = ["de", "adjectif", "du", "rien"]
    case = random.choice(cases)
    
    if case == "de":
        adj = " de "
        if random.randint(0,1) == 0:
            no = random.choice(namesOwner)
            if no[0:3] == "le ":
                no = " du "+no[3:]
                adj = ""
            adj += no+" "
        elif owner[0] in ["A", "E", "I", "O", "U", "Y"]:
            adj= " d'"
        finalName += adj+owner
    elif case == "adjectif":
        adj = {}
        adj["merveilleux"] = "merveilleuse"
        adj["magique"] = ""
        adj["enchante"] = "enchantee"
        adj["lointain"] = "lointaine"
    
        aa = random.choice(adj.keys())
        if adj[aa] != "" and (nameGenre==1 or nameGenre==3) :
            aa = adj[aa]
        finalName += " "+aa
    elif case == "du":
        toadd = ["des lutins", "des familles", "de chez nous", "d'antan", "du printemps",
        "des amis", "du port", "de la gare", "du centre", "des reves", "du bon Dieu"]
        aa = random.choice(toadd)
        finalName += " "+aa
        
    return finalName
    
    
#produits = ["pommes", "poires", "peches", "farine", "oeufs", "beurre", "sucre", "miel", "amandes", "raisins", "noisettes", "noix"]   
produits = ["pommes",  "farine", "oeufs", "beurre", "sucre", ]
    
def addToDict(dict, key, value):
    if key not in dict.keys():
        dict[key] = value
    else:
        dict[key] += value
    if dict[key] == 0:
        del dict[key]

def getDict(dict, key):
    if key not in dict.keys():
        return 0
    return dict[key]
    
    
def addToDictList(dict, key, value):
    if key not in dict.keys():
        dict[key] = [value]
    else:
        dict[key].append(value)

    
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])*(p1[0] - p2[0])+(p1[1] - p2[1])*(p1[1] - p2[1]))
    
def firstPart(s):
    split = s.split('-', 1)
    if len(split) == 1:
        split.append("")
    return split
    
class Time:
    def __init__(self):
        self.minute = 0
        self.hour = 0
        self.day = 1
        self.month = 1
        self.year = 0
        
    def now(self):
        return [self.minute, self.hour, self.day, self.month, self.year] 

    def addTime(self, num=1):
        [self.minute, self.hour, self.day, self.month, self.year] = self.timeIn(num)
        
    
    def durationTo(self,date, startDate = []):
        #~ min = date[0]
        #~ h = date[1]
        #~ d = date[2]
        #~ m = date[3]
        #~ y = date[4]
        
        if len(startDate)<5:
            startDate = [self.minute, self.hour, self.day, self.month, self.year] 
        
        duration = (date[4] - startDate[4])*12
        duration = (duration + date[3] - startDate[3])*30
        duration = (duration + date[2] - startDate[2])*24
        duration = (duration + date[1] - startDate[1])*60
        return duration + date[0] - startDate[0]
    
    def timeIn(self, duration, fromTime=[]):
        if len(fromTime)<5:
            fromTime = [self.minute, self.hour, self.day, self.month, self.year] 
    
        min = fromTime[0] + duration
        h = fromTime[1]
        d = fromTime[2]
        m = fromTime[3]
        y = fromTime[4]
        while min >=60:
            min -=60
            h += 1
        while min <0:
            min +=60
            h -= 1
        while h >=24:
            h -=24
            d += 1
        while h <0:
            h+=24
            d -= 1
        while d>30:
            d -= 30
            m  += 1
        while d<=0:
            d += 30
            m  -= 1
        while m > 12:
            m -= 12
            y +=1
        while m<= 0:
            m += 12
            y -=1
        return [min, h, d, m, y]
    
    def __str__(self, t=[]):
        if len(t)<5:
            t = [self.minute, self.hour, self.day, self.month, self.year] 
        monthNames = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre"]
        s = str(t[1])+" h "+str(t[0])+", le "+str(t[2])+" "+monthNames[t[3]-1]+" "+str(2000 + t[4])
        return s
 
    def write(self, root):
        subel = ET.SubElement(root, 'time')
        subel.set("minute", str(self.minute))
        subel.set("hour", str(self.hour))
        subel.set("day", str(self.day))
        subel.set("month", str(self.month))
        subel.set("year", str(self.year))
        
    def read(self, root):
        self.minute = int(root.attrib["minute"])
        self.hour = int(root.attrib["hour"])
        self.day = int(root.attrib["day"])
        self.month = int(root.attrib["month"])
        self.year = int(root.attrib["year"])
        
global globalTime
globalTime = Time()
    
if __name__ == '__main__':
    #~ for i in range(0, 10):
        #~ print randomName()
    #~ print "---"
    #~ for i in range(0, 10):
        #~ print randomCityName()
    #~ print "---"
    for i in range(0, 20):
        print randomHotelName("Guillaume")
    #~ for i in range(0, 10):
        #~ print randomCityName()      
    #~ dict = {"test":2}
    #~ print dict
    #~ addToDict(dict, "test", 3)
    #~ addToDict(dict, "test2", 3)
    #~ print dict
    #~ print getDict(dict, "test2")
    #~ print getDict(dict, "test3")
    #~ addTime()
    #~ print durationTo(10, 1, 1, 0)
    

    #~ print printTime()
    #~ t = Time()
    #~ t.addTime()
    #~ print t
    #~ [h, d, m, y] = t.timeIn(1000)
    #~ print t.__str__([h, d, m, y])

    
    
        