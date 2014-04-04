import random, utils

from LittleVillager import *
from LittlePlace import *
from LittleTask import *

class LittleVillage:
    def __init__(self):
        self.toDoList = []
        self.villagers = []
        self.places=[]
        self.buildings=[]
        self.globalPosition = [0.,0.]
        self.name = "defaultVillageName"
        
    def readVillage(self, file):
        print "bla"
        
    def writeVillage(self, file):
        print "bla"
        
    def createRandomVillage(self, num):
        startName = utils.allU # ['Ba', 'Be', 'Bi', 'Bo', 'Bu', 'Bon', 'Bou', 'Bai', 'Ca', 'Ce', 'Ci', 'Co', 'Cu', 'Con', 'Cou', 'Cai', 'Da', 'De', 'Di', 'Do', 'Du', 'Don', 'Dou', 'Dai', 'Fa', 'Fe', 'Fi', 'Fo', 'Fu', 'Fon', 'Fou', 'Fai', 'Ga', 'Ge', 'Gi', 'Go', 'Gu', 'Gon', 'Gou', 'Gai', 'Ha', 'He', 'Hi', 'Ho', 'Hu', 'Hon', 'Hou', 'Hai', 'Ja', 'Je', 'Ji', 'Jo', 'Ju', 'Jon', 'Jou', 'Jai', 'La', 'Le', 'Li', 'Lo', 'Lu', 'Lon', 'Lou', 'Lai', 'Ma', 'Me', 'Mi', 'Mo', 'Mu', 'Mon', 'Mou', 'Mai', 'Na', 'Ne', 'Ni', 'No', 'Nu', 'Non', 'Nou', 'Nai', 'Pa', 'Pe', 'Pi', 'Po', 'Pu', 'Pon', 'Pou', 'Pai', 'Ra', 'Re', 'Ri', 'Ro', 'Ru', 'Ron', 'Rou', 'Rai', 'Sa', 'Se', 'Si', 'So', 'Su', 'Son', 'Sou', 'Sai', 'Ta', 'Te', 'Ti', 'To', 'Tu', 'Ton', 'Tou', 'Tai', 'Va', 'Ve', 'Vi', 'Vo', 'Vu', 'Von', 'Vou', 'Vai']
        middleName = utils.allL #['ba', 'be', 'bi', 'bo', 'bu', 'bon', 'bou', 'bai', 'ca', 'ce', 'ci', 'co', 'cu', 'con', 'cou', 'cai', 'da', 'de', 'di', 'do', 'du', 'don', 'dou', 'dai', 'fa', 'fe', 'fi', 'fo', 'fu', 'fon', 'fou', 'fai', 'ga', 'ge', 'gi', 'go', 'gu', 'gon', 'gou', 'gai', 'ha', 'he', 'hi', 'ho', 'hu', 'hon', 'hou', 'hai', 'ja', 'je', 'ji', 'jo', 'ju', 'jon', 'jou', 'jai', 'la', 'le', 'li', 'lo', 'lu', 'lon', 'lou', 'lai', 'ma', 'me', 'mi', 'mo', 'mu', 'mon', 'mou', 'mai', 'na', 'ne', 'ni', 'no', 'nu', 'non', 'nou', 'nai', 'pa', 'pe', 'pi', 'po', 'pu', 'pon', 'pou', 'pai', 'ra', 're', 'ri', 'ro', 'ru', 'ron', 'rou', 'rai', 'sa', 'se', 'si', 'so', 'su', 'son', 'sou', 'sai', 'ta', 'te', 'ti', 'to', 'tu', 'ton', 'tou', 'tai', 'va', 've', 'vi', 'vo', 'vu', 'von', 'vou', 'vai']
        endName = ["touille", "mont", "vert", "gny", "leaux", "rrand"]
        self.name= startName[random.randint(0, len(startName)-1)]+middleName[random.randint(0, len(middleName)-1)]+endName[random.randint(0, len(endName)-1)]

        for i in range(num):
            lv = LittleVillager()
            lv.generate()
            self.villagers.append(lv)
            
        entrepot = LittleBuilding()
        entrepot.name = "Warehouse"
        self.buildings.append(entrepot)
        
    def __str__(self):
        s = "This is the village of "+self.name
        s += "\ninhabitants :"
        for v in self.villagers:
            s += "\n"+v.name+ " "+ str(v.gender)
        return s
        
    def iterate(self):
        for p in self.villagers:
            if not p.busy:
                #~ print "test"
                p.selectTask(self.toDoList)
            else:
                p.performTask()
        inds = range(len(self.toDoList))
        inds.reverse()
        for i in inds:
            if self.toDoList[i].status == "done":
                print self.toDoList[i].name, " finished"
                self.toDoList.pop(i)
            

if __name__ == '__main__':
    lv = LittleVillage()
    lv.createRandomVillage(10)
    print lv
    lbt = LittleBuildTask("warehouse")
    lv.toDoList.append(lbt)
    lbt = LittleBuildTask("warehouse")
    lv.toDoList.append(lbt)
    lbt = LittleBuildTask("warehouse")
    lv.toDoList.append(lbt)
    for i in range(25):
        lv.iterate()
