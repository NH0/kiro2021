import numpy as np

from configuration import PATH, NAME

from scipy.spatial.distance import cdist

class Instance:

    def __init__(self, name,  path=PATH):

        self.name = name
        self.data = []
        self.read_instance(name, path)

    def read_instance(self, name, path=PATH):

        with open(path + name, "r") as f:
            Dat = f.readlines()

            for i, line in enumerate(Dat):
                line = line.replace(";", "")
                line = line.split()
                line = list(map(float, line))
                self.data.append(line)

            self.data = np.array(self.data)

            self.dist_mat = cdist(self.data, self.data)

            self.data_x = self.data[self.data[:, 0].argsort()]
            self.data_y = self.data[self.data[:, 1].argsort()]
            self.data_z = self.data[self.data[:, 2].argsort()]
            self._n = len(self.data)

test = Instance(NAME, PATH)




