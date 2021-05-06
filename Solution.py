import utils
import config as CONF
import numpy as np

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
            if self.solution[sol]["voieAQuai"] == "notAffected":
                score += CONF.C0
            for contrainte in self.contraintes:
                if str(contrainte[0]) == sol and str(contrainte[1]) == self.solution[sol]["itineraire"]:
                    if str(contrainte[3]) == self.solution[str(contrainte[2])]["itineraire"]:
                        score += contrainte[4]
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
    
    def contrainte_par_itin(self):
        self.contraintes_par_itineraire = [[] for i in range(len(self.itineraires))]
        for c in range(len(self.contraintes)):
            self.contraintes_par_itineraire[self.contraintes[c][1]].append(c)
            self.contraintes_par_itineraire[self.contraintes[c][3]].append(c)
        

    def greedy(self):
        appearance_itin = [0 for i in range(len(self.itineraires))]
        for c in self.contraintes:
            appearance_itin[c[1]] += c[4]
            appearance_itin[c[3]] += c[4]
        itin_sorted = np.argsort(appearance_itin)
        for train in self.trains:
            quai = []
            quai_score = []
            quai_itin = []
            for t in train:
                for itin in itin_sorted:
                    if np.isin(itin,self.admissible[t["id"]]):
                        q = self.itineraires[itin]["voieAQuai"]
                        if np.isin(q,quai):
                            index = quai.index(q)
                        else:
                            quai.append(q)
                            quai_score.append([2000 for tr in range(len(train))])
                            index = -1
                            quai_itin.append([-1 for tr in range(len(train))])
                        
                        for c in self.contraintes_par_itineraire[itin]:
                            if self.contraintes[c][1] == itin :
                                if self.contraintes[c][0] == t["id"] and self.solution[str(self.contraintes[c][2])]["itineraire"] == str(self.contraintes[c][3]):
                                    quai_score[index][t] = min(self.contraintes[c][4],quai_score[t])
                                    quai_itin[index][t] = itin
                            elif self.contraintes[c][3] == itin:
                                if self.contraintes[c][2] == t["id"] and self.solution[str(self.contraintes[c][0])]["itineraire"] == str(self.contraintes[c][1]):
                                    quai_score[index][t] = min(self.contraintes[c][4],quai_score[t])
                                    quai_itin[index][t] = itin
                        
                        if quai_itin[index].count(-1) == 0 and np.sum(quai_score[index]) <= 2000*len(train):
                            for tr in train:
                                self.solution[str(tr["id"])] = {"voieAQuai" : self.itineraires[quai_itin[index][tr["id"]]]["voieAQuai"], "itineraire" : str(quai_itin[index][tr["id"]])}
                            break
                       
    def export(self):

        with open('A.json', 'w') as outfile:
            json.dump(self.solution, outfile)

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]

    return len(lst3)

