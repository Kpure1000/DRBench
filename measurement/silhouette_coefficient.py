from measure import Measure
from sklearn import metrics

class SilhouetteCoefficient(Measure):
    def measure(self, proj, label):
        return metrics.silhouette_score(proj, label)
