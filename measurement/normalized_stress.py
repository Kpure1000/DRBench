import numpy as np
from measure import Measure

class NormalizedStress(Measure):

    def measure(self, data, proj):
        if len(data) != len(proj):
            print(f'data len {len(data)} != proj len {len(proj)}')
            return 0
        
        # distance matrix in origin space
        direction_org = data[:, np.newaxis, :] - data[np.newaxis, :, :]
        distance_org = np.linalg.norm(direction_org, axis=-1)
        
        # distance matrix in projection space
        direction_prj = proj[:, np.newaxis, :] - proj[np.newaxis, :, :]
        distance_prj = np.linalg.norm(direction_prj, axis=-1)

        delta = distance_org - distance_prj

        numerator = np.sum(np.dot(delta, delta))
        
        denominator = np.sum(np.dot(distance_org, distance_org))

        return numerator / denominator
