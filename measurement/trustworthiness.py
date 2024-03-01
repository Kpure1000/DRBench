from sklearn import manifold
from measure import Measure

class Trustworthiness(Measure):
    def __init__(self, n_neighbors=10):
        self.neighbors = n_neighbors

    def measure(self, data, proj):
        return manifold.trustworthiness(data, proj, n_neighbors=self.neighbors)