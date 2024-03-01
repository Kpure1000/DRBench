import matplotlib.pyplot as plt
import numpy as np
from generate import *
import sys
sys.path.append('../methods')
from parametric_tSNE import Parametric_tSNE as PTSNE
from sklearn.decomposition import IncrementalPCA, PCA
from sklearn.manifold import Isomap
from sklearn.cluster import KMeans

def make_swiss_roll(n_samples:int, noise=0.0, y_width=21.0, circle_num=2.0):
    np.random.seed(0)

    generator = np.random.mtrand._rand

    t = 1.5 * np.pi * (1 + circle_num * generator.uniform(size=n_samples))
    y = y_width * generator.uniform(size=n_samples)

    # t = np.sort(t)

    x = t * np.cos(t)
    z = t * np.sin(t)

    X = np.vstack((x, y, z))
    X += noise * generator.standard_normal(size=(3, n_samples))
    X = X.T
    t = np.squeeze(t)

    # g = generator.uniform(size=n_samples)
    # g = np.array([0 if n < 0.5 else 1 for n in g])

    kmeans = KMeans(n_clusters=2)
    kmeans.fit(X)
    # 获取聚类结果
    g = np.array(kmeans.labels_)

    return X, t, g


if __name__ == "__main__":
    n_samples = 500
    data, t, g = make_swiss_roll(n_samples=n_samples, noise=0.0,circle_num=1.5)

    tmin = np.min(t)
    tmax = np.max(t)

    tlim1 = (2.0 * tmin + tmax) / 3.0
    data1=[]
    t1=[]

    for i, val in enumerate(t):
        if val < tlim1:
            data1.append(data[i])
            t1.append(val)

    data1=np.array(data1)

    tlim2 = (tmin + 2.0 * tmax) / 3.0
    data2=[]
    t2=[]
    for i, val in enumerate(t):
        if val < tlim2:
            data2.append(data[i])
            t2.append(val)

    data2=np.array(data2)

    data3=data
    t3=t

    pmin = -20
    pmax = 20

    # ipca = IncrementalPCA(n_components=2)
    # proj1 = ipca.fit_transform(data1)
    # proj2 = ipca.transform(data2)
    # proj3 = ipca.transform(data3)

    pca = PCA(n_components=2)
    proj = pca.fit_transform(data3)

    # ptsne = PTSNE(3, 2, 20, alpha=2 - 1.0, do_pretrain=False, batch_size=128, seed=54321)
    # ptsne.fit(data1)
    # proj1= ptsne.transform(data1)
    # proj2 = ptsne.transform(data2)
    # proj3 = ptsne.transform(data3)

    # isomap = Isomap(n_components=2)
    # proj1= isomap.fit_transform(data1)
    # proj2 = isomap.fit_transform(data2)
    # proj3 = isomap.fit_transform(data3)

    np.savetxt('../static/datasets/swissroll/swissroll.csv', np.hstack((proj, g[:, np.newaxis])), delimiter=',', header='x,y,g',encoding='UTF-8',comments='',fmt=['%.5f','%.5f','%d'])

    gen = DatasetsManager('../static/datasets/datasets.json')
    gen.generate('swissroll', 'swissroll', DT_OTHER, len(g), data3.shape[1])


