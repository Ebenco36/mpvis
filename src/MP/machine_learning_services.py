import numpy as np
import joblib
from sklearn.cluster import DBSCAN, MeanShift, AgglomerativeClustering, OPTICS, AffinityPropagation, SpectralClustering, KMeans, SpectralClustering
from sklearn.mixture import GaussianMixture
from src.services.Helpers.Regressors.index import Regressors
from src.services.Helpers.machine_learning_al.UnsupervisedMachineLearning import MachineLearning
from src.services.Helpers.machine_learning_al.dimensionality_reduction import DimensionalityReduction

from src.services.Helpers.machine_learning_al.normalization import Normalization

class UnsupervisedPipeline:

    def __init__(self, data_frame):
        self.data_frame = data_frame

    def apply_normalization(self, normalization_method='min_max'):
        normalization = Normalization(self.data_frame)

        if normalization_method == 'min_max':
            return normalization.min_max_normalization()
        elif normalization_method == 'robust_scaler':
            return normalization.robust_scaler_normalization()
        elif normalization_method == 'max_abs_scaler':
            return normalization.max_abs_scaler_normalization()
        elif normalization_method == 'standard_scaler':
            return normalization.standard_scaler_normalization()
        else:
            raise ValueError("Invalid normalization method. Choose from 'min_max', 'robust_scaler', 'max_abs_scaler', 'standard_scaler'.")

    def apply_dimensionality_reduction(self, reduction_method='pca', n_features=2, dr_columns=[]):
        dimensionality_reduction = DimensionalityReduction(self.data_frame, n_features=n_features, pca_columns=dr_columns)

        if reduction_method == 'pca':
            return dimensionality_reduction.pca_algorithm()
        elif reduction_method == 'truncated_svd':
            return dimensionality_reduction.TruncatedSVD_algorithm()
        elif reduction_method == 'nmf':
            return dimensionality_reduction.NMF_algorithm()
        elif reduction_method == 'factor_analysis':
            return dimensionality_reduction.FactorAnalysis_algorithm()
        elif reduction_method == 'ica':
            return dimensionality_reduction.ica_algorithm()
        elif reduction_method == 'gaussian_random_proj':
            return dimensionality_reduction.gaussian_random_proj_algorithm()
        elif reduction_method == 'tsne':
            return dimensionality_reduction.tsne_algorithm()
        elif reduction_method == 'isomap':
            return dimensionality_reduction.isomap_algorithm()
        elif reduction_method == 'ile':
            return dimensionality_reduction.ile_algorithm()
        else:
            raise ValueError("Invalid dimensionality reduction method. Choose from 'pca', 'truncated_svd', 'nmf', 'factor_analysis', 'ica', 'gaussian_random_proj', 'tsne', 'isomap', 'ile'.")

    def apply_imputation(self, imputation_method='knn', remove_by_percent=90):
        if imputation_method == 'knn':
            imputer = Regressors(self.data_frame, remove_by_percent)
            return imputer.KNN_imputer_regressor()
        elif imputation_method == 'simple':
            imputer = Regressors(self.data_frame, remove_by_percent)
            return imputer.simple_regressor()
        else:
            raise ValueError("Invalid imputation method. Choose from 'knn', 'simple'.")

    def apply_clustering(self, method='kmeans', n_clusters=3):
        clustering = MachineLearning(self.data_frame, n_clusters=n_clusters)

        if method == 'dbscan':
            return clustering.dbscan_clustering()
        elif method == 'mean_shift':
            return clustering.mean_shift_clustering()
        elif method == 'agglomerative':
            return clustering.agglomerative_clustering()
        elif method == 'optics':
            return clustering.optics_clustering()
        elif method == 'affinity_propagation':
            return clustering.affinity_propagation_clustering()
        elif method == 'spectral':
            return clustering.spectral_clustering()
        elif method == 'kmeans':
            return clustering.kMeans_clustering()
        elif method == 'gaussian':
            return clustering.gaussian_clustering()
        else:
            raise ValueError("Invalid clustering method. Choose from 'dbscan', 'mean_shift', 'agglomerative', 'optics', 'affinity_propagation', 'spectral', 'kmeans', 'gaussian'.")

# Example Usage:
# Replace 'your_data_frame' with the actual variable holding your DataFrame
data_frame = your_data_frame

# Step 1: Apply Normalization
normalized_data = UnsupervisedPipeline(data_frame).apply_normalization(normalization_method='min_max')

# Step 2: Apply Dimensionality Reduction
reduced_data, explainable_info = UnsupervisedPipeline(normalized_data).apply_dimensionality_reduction(reduction_method='pca', n_features=2, dr_columns=['PC1', 'PC2'])

# Step 3: Apply Imputation (if needed)
imputed_data = UnsupervisedPipeline(reduced_data).apply_imputation(imputation_method='knn', remove_by_percent=90)

# Step 4: Apply Clustering
clustered_data, clustering_params, clustering_path = UnsupervisedPipeline(imputed_data).apply_clustering(method='kmeans', n_clusters=3)
