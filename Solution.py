import json
import utils
import config as CONF
import numpy as np
import json

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

        # print(self.voiesAQuai)
        # print(self.solution)

    @property
    def score(self):
        score = 0
        self.pire_trains = []
        self.unassigned = []
        for sol in self.solution:
            if self.solution[sol]["voieAQuai"] == "notAffected":
                score += CONF.C0
                self.unassigned.append(sol)
            if int(sol) in self.contraintes_par_train:
                for contrainte in self.contraintes_par_train[int(sol)]:
                    if str(contrainte[0]) == sol and str(contrainte[1]) == self.solution[sol]["itineraire"]:
                        if str(contrainte[3]) == self.solution[str(contrainte[2])]["itineraire"]:
                            score += contrainte[4]
                            self.pire_trains.append([sol, str(contrainte[3]), contrainte[4]])
        self.pire_trains.sort(key=lambda x:x[2])
        # print(self.pire_trains)
        return score

    def compute_admissible(self):

        self.admissible = {}
        self.train_quai = {}
        for group_train in self.trains:
            interdites = []
            for train in group_train:

                for inter in self.interdictions:
                    if train["voieEnLigne"] in inter["voiesEnLigne"] \
                    or len(intersection(inter["typesMateriels"], train["typesMateriels"]))>0 \
                    or train["typeCirculation"] in inter["typesCirculation"]:
                        interdites.extend(inter["voiesAQuaiInterdites"])
            interdites = list(set(interdites))

            for train in group_train:
                self.admissible[train["id"]] = []
                self.train_quai[train["id"]] = []

                for itin in self.itineraires:
                    if itin["sensDepart"] == train["sensDepart"]:
                        if itin["voieEnLigne"] == train["voieEnLigne"]:
                            if itin["voieAQuai"] not in interdites:
                                self.admissible[train["id"]].append(itin["id"])
                                self.train_quai[train["id"]].append(itin["voieAQuai"])

                self.train_quai[train["id"]] = list(set(self.train_quai[train["id"]]))

                #print(train["id"], len(self.train_quai[train["id"]]))

            inter_quai = self.train_quai[group_train[0]["id"]]
            for train in group_train[1:]:
                inter_quai = intersection(inter_quai, self.train_quai[train["id"]])
            for train in group_train:

                for itin in self.admissible[train["id"]]:

                    if self.itineraires[itin]["voieAQuai"] not in inter_quai:
                        self.admissible[train["id"]].remove(itin)

                #print(train["id"], len(self.train_quai[train["id"]]))


    def contrainte_par_itin(self):
        self.contraintes_par_itineraire = [[] for i in range(len(self.itineraires))]
        self.contraintes_par_train = {}
        for c in range(len(self.contraintes)):
            self.contraintes_par_itineraire[self.contraintes[c][1]].append(c)
            self.contraintes_par_itineraire[self.contraintes[c][3]].append(c)
            if self.contraintes[c][0] in self.contraintes_par_train:
                self.contraintes_par_train[self.contraintes[c][0]].append(c)
            else:
                self.contraintes_par_train[self.contraintes[c][0]] = []
            if self.contraintes[c][2] in self.contraintes_par_train:
                self.contraintes_par_train[self.contraintes[c][2]].append(c)
            else:
                self.contraintes_par_train[self.contraintes[c][0]] = []


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
            for t in range(len(train)):
                for itin in itin_sorted:
                    if np.isin(itin,self.admissible[train[t]["id"]]):
                        q = self.itineraires[itin]["voieAQuai"]
                        if np.isin(q,quai):
                            index = quai.index(q)
                        else:
                            quai.append(q)
                            quai_score.append([2000 for tr in range(len(train))])
                            index = -1
                            quai_itin.append([-1 for tr in range(len(train))])
                        cout_itin = 0
                        for c in self.contraintes_par_itineraire[itin]:
                            if self.contraintes[c][1] == itin :
                                if self.contraintes[c][0] == train[t]["id"] and self.solution[str(self.contraintes[c][2])]["itineraire"] == str(self.contraintes[c][3]):
                                    cout_itin += self.contraintes[c][4]
                                    quai_itin[index][t] = itin
                            elif self.contraintes[c][3] == itin:
                                if self.contraintes[c][2] == train[t]["id"] and self.solution[str(self.contraintes[c][0])]["itineraire"] == str(self.contraintes[c][1]):
                                    cout_itin += self.contraintes[c][4]

                        if quai_score[index][t] > cout_itin:
                            quai_score[index][t] = cout_itin
                            quai_itin[index][t] = itin

            min_sum = np.sum(quai_score[0])
            ind = 0
            for i in range(1,len(quai)):
                if min_sum > np.sum(quai_score[i]):
                    min_sum = np.sum(quai_score[i])
                    ind = i

            if min_sum <= 2000*len(train):
                for tr in range(len(train)):
                    self.solution[str(train[tr]["id"])] = {"voieAQuai" : quai[ind], "itineraire" : str(quai_itin[ind][tr])}


    def greedy_2(self):

        appearance_itin = [0 for i in range(len(self.itineraires))]
        for c in self.contraintes:
            appearance_itin[c[1]] += c[4]
            appearance_itin[c[3]] += c[4]

        for group_train in self.trains:
            quai = []
            quai_score = []
            quai_itin = []

            for train in range(len(group_train)):

                for itin in self.admissible[group_train[train]["id"]]:
                    q = self.itineraires[itin]["voieAQuai"]
                    if np.isin(q,quai):
                        index = quai.index(q)
                    else:
                        quai.append(q)
                        quai_score.append([np.inf for tr in range(len(group_train))])
                        index = -1
                        quai_itin.append([-1 for tr in range(len(group_train))])

                    if quai_score[index][train] > appearance_itin[itin]:
                        quai_score[index][train] = appearance_itin[itin]
                        quai_itin[index][train] = itin

            if len(quai_score)>0:
                min_sum = np.sum(quai_score[0])
                ind = 0
                for i in range(1,len(quai)):
                    if min_sum > np.sum(quai_score[i]):
                        min_sum = np.sum(quai_score[i])
                        ind = i

                for tr in range(len(group_train)):
                    self.solution[str(group_train[tr]["id"])] = {"voieAQuai" : quai[ind], "itineraire" : str(quai_itin[ind][tr])}


    def read_sol(self, file):
        self.solution = utils.read_json(file)

    def export(self):

        with open("sol_"+CONF.filename, 'w') as outfile:
            json.dump(self.solution, outfile)

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]

    return lst3









