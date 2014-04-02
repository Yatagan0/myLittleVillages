import utils, random

class LittleTask:
    def __init__(self):
        self.state = ""


class LittleBuildTask(LittleTask):
    def __init__(self):
        LittleTask.__init__(self)

class LittleCarryTask(LittleTask):
    def __init__(self):
        LittleTask.__init__(self)
        
class LittleWorkTask(LittleTask):
    def __init__(self):
        LittleTask.__init__(self)
        
if __name__ == '__main__':
    lbt = LittleBuildTask()
