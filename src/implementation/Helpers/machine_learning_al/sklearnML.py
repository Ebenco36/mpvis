import numpy as np
import joblib
from sklearn.cluster import DBSCAN, MeanShift, AgglomerativeClustering, OPTICS, AffinityPropagation, SpectralClustering, KMeans, SpectralClustering
from sklearn.mixture import GaussianMixture

class MachineLearning:

    def __init__(self, X, eps=0.3, min_samples=None, n_clusters=2, n_components=2, UOT = False, save_path = None):
        """
            if UOT is True then we only want to train separately first before predicting
        """
        self.UOT = UOT
        self.save_path = save_path
        self.X = X
        self.eps = eps
        self.min_samples = min_samples
        self.n_clusters = n_clusters
        self.n_components = n_components
    
    def run_clustering_algorithm(self, algorithm, **kwargs):
        clustering = algorithm(**kwargs)
        if (self.UOT is True):
            path = self.save_path if(self.save_path) else "./public/data_sessions/"
            complete_path = path + "/_" + clustering.__class__.__name__ + "_.pkl"
            labels = clustering.fit_predict(self.X)
            joblib.dump(labels, complete_path)
            params = clustering.get_params(deep=True)
            return labels, params, complete_path
        else:
            complete_path = "We are not saving anything"
            labels = clustering.fit_predict(self.X)
            params = clustering.get_params(deep=True)
            return labels, params, complete_path
        

    # DBSCAN
    def dbscan_clustering(self):
        labels, params, path = self.run_clustering_algorithm(DBSCAN, eps=self.eps, min_samples=self.min_samples)
        self.X['dbscan_clustering'] = labels
        return self.X, params, path

    # Mean Shift
    def mean_shift_clustering(self):
        labels, params, path = self.run_clustering_algorithm(MeanShift)
        self.X['mean_shift_clustering'] = labels
        return self.X, params, path

    # Agglomerative Clustering
    def agglomerative_clustering(self):
        labels, params, path = self.run_clustering_algorithm(AgglomerativeClustering, n_clusters=self.n_clusters)
        self.X['agglomerative_clustering'] = labels
        return self.X, params, path

    # OPTICS
    def optics_clustering(self):
        labels, params, path = self.run_clustering_algorithm(OPTICS, min_samples=self.min_samples)
        self.X['optics_clustering'] = labels
        return self.X, params, path

    # Affinity Propagation
    def affinity_propagation_clustering(self):
        labels, param, paths = self.run_clustering_algorithm(AffinityPropagation)
        self.X['affinity_propagation_clustering'] = labels
        return self.X, params, path 

    # SpectralClustering Propagation
    def spectral_clustering(self):
        labels, params, path = self.run_clustering_algorithm(SpectralClustering)
        self.X['spectral_clustering'] = labels
        return self.X, params, path

        # KMeans Propagation
    def kMeans_clustering(self):
        labels, params, path = self.run_clustering_algorithm(KMeans, n_clusters=self.n_clusters)
        self.X['kMeans_clustering'] = labels
        return self.X, params, path

    def gaussian_clustering(self):
        # Create an instance of the Gaussian Mixture Model algorithm
        labels, params, path = self.run_clustering_algorithm(GaussianMixture, n_components=self.n_components)
        self.X['gaussian_clustering'] = labels
        return self.X, params, path

    @staticmethod
    def make_predictions(model_path, new_data):
        # Load the model from the file
        loaded_model = joblib.load(model_path)
        # Predict clusters for new data using the loaded model
        new_predictions = loaded_model.predict(new_data)

        return new_predictions