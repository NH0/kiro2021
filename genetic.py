import enum

class mutations(enum.Enum):
    ONE_POINT = 0
    TWO_POINT = 1
    CX = 2
    PMX = 3

class individual:
    def __init__(self, genome):
        self.chromose = genome

    @property
    def fit(self):
        return 0
    

class population:
    def __init__(self, individuals):
        self.pop = individuals

    def evaluation(self):
        self.evaluations = [indiv.fit for indiv in self.pop]
    
    def _weight_population(self):
        total_evaluation = sum(self.evaluations)
        self.weights = [self.evaluations[i] / total_evaluation for i in range(len(pop))]

    def selection(self):
        self._weight_population()

    def crossover(self, selected, type = mutations.PMX)
        pass

    def mutations(self):
        pass

    def evolve(self):
        offsprings = []
        while(true):
            self.evaluation()
            selected = self.selection()
            offsprings = crossover(selected)
            offsprings = mutations(offsprings)
        return offsprings