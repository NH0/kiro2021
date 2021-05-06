import utils
import config as CONF

class Solution:
    def __init__(self, file):
        self.name = file
        obj = utils.read_json(file)
        self.trains = obj["trains"]
        self.itineraires = obj["itineraires"]
        self.voiesAQuai = obj["voiesAQuai"]
        self.voiesEnLigne = obj["voiesEnLigne"]
        self.interdictions = obj["interdictionsQuais"]
        self.contraintes = obj["contraintes"]

        self.solution = {}
        for train in self.trains:
            for tr in train:
                self.solution[str(tr["id"])] = {"voieAQuai" : "notAffected", "itineraire" : "notAffected"}

        print(self.voiesAQuai)
        print(self.solution)
    
    @property
    def score(self):
        score = 0
        for sol in self.solution:
            if sol["voieAQuai"] == "notAffected":
                score += CONF.C0 
        return score
