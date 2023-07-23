import numpy as np
from sklearn.cluster import DBSCAN, MeanShift, AgglomerativeClustering, OPTICS, AffinityPropagation, SpectralClustering, KMeans, SpectralClustering
from sklearn.mixture import GaussianMixture

class MachineLearning:

    def __init__(self, X, eps=0.3, min_samples=None, n_clusters=2, n_components=2):
        self.X = X
        self.eps = eps
        self.min_samples = min_samples
        self.n_clusters = n_clusters
        self.n_components = n_components
    
    def run_clustering_algorithm(self, algorithm, X, **kwargs):
        clustering = algorithm(**kwargs)
        labels = clustering.fit_predict(X)
        params = clustering.get_params(deep=True)
        return labels, params

    # DBSCAN
    def dbscan_clustering(self):
        labels, params = self.run_clustering_algorithm(DBSCAN, self.X, eps=self.eps, min_samples=self.min_samples)
        self.X['dbscan_clustering'] = labels
        return self.X, params

    # Mean Shift
    def mean_shift_clustering(self):
        labels, params = self.run_clustering_algorithm(MeanShift, self.X)
        self.X['mean_shift_clustering'] = labels
        return self.X, params

    # Agglomerative Clustering
    def agglomerative_clustering(self):
        labels, params = self.run_clustering_algorithm(AgglomerativeClustering, self.X, n_clusters=self.n_clusters)
        self.X['agglomerative_clustering'] = labels
        return self.X, params

    # OPTICS
    def optics_clustering(self):
        labels, params = self.run_clustering_algorithm(OPTICS, self.X, min_samples=self.min_samples)
        self.X['optics_clustering'] = labels
        return self.X, params

    # Affinity Propagation
    def affinity_propagation(self):
        labels, params = self.run_clustering_algorithm(AffinityPropagation, self.X)
        self.X['affinity_propagation'] = labels
        return self.X, params 

    # SpectralClustering Propagation
    def spectral_clustering(self):
        labels, params = self.run_clustering_algorithm(SpectralClustering, self.X)
        self.X['spectral_clustering'] = labels
        return self.X

        # KMeans Propagation
    def kMeans_clustering(self):
        labels, params = self.run_clustering_algorithm(KMeans, self.X, n_clusters=self.n_clusters)
        self.X['kMeans_clustering'] = labels
        return self.X, params

    def gaussian_clustering(self):
        # Create an instance of the Gaussian Mixture Model algorithm
        labels, params = self.run_clustering_algorithm(GaussianMixture, self.X, n_components=self.n_components)
        self.X['gaussian_clustering'] = labels
        return self.X, params
