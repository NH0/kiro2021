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

    def compute_admissible(self):

        self.admissible = {}
        for group_train in self.trains:
            interdites = []
            for train in group_train:

                for inter in self.interdictions:
                    if train["voieEnLigne"] in inter["voiesEnLigne"] or intersection(inter["typesMateriels"], train["typesMateriels"])>0 or train["typeCirculation"] in inter["typesCirculation"]:
                        interdites.extend(inter["voiesAQuaiInterdites"])
            interdites = list(set(interdites))

            for train in group_train:
                self.admissible[train["id"]] = []
                for itin in self.itineraires:
                    if itin["sensDepart"] == train["sensDepart"]:
                        if itin["voieEnLigne"] == train["voieEnLigne"]:
                            if itin["voieAQuai"] not in interdites:

                                self.admissible[train["id"]].append(itin["id"])



    def export(self):

        with open('A.json', 'w') as outfile:
            json.dump(self.solution, outfile)

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]

    return len(lst3)

sol = Solution(CONF.file)
sol.compute_admissible()

