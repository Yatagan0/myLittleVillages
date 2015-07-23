import utils, random
import xml.etree.ElementTree as ET



class LittleNewAction:
    def __init__(self, root=None, workslot = None, type="do nothing", price=0.):
        self.workslot = workslot
        self.type = type
        self.price = price
        if root is not None:
            self.read(root)