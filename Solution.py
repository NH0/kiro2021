import utils

class Solution:
    def __init__(self, file):
        self.name = file
        self.obj = utils.read_json(file)
    
    @property
    def score(self):
        return 0
