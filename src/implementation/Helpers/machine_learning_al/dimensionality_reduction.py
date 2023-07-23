from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.random_projection import GaussianRandomProjection
from sklearn.manifold import LocallyLinearEmbedding
from sklearn.decomposition import PCA, FastICA
from sklearn.manifold import TSNE
from sklearn.manifold import Isomap
import pandas as pd
import numpy as np

class DimensionalityReduction:
    def __init__(self, X, n_features=2, pca_columns=2):
        self.X = X
        self.n_features = n_features if n_features > 1 else 2
        self.dr_columns = pca_columns

    def pca_algorithm(self):
        pca = PCA(self.n_features).fit(self.X)
        pca_data = pca.transform(self.X)
        data = pd.DataFrame(pca_data, columns=self.dr_columns)

        return data
    
    def lda_algorithm(self):
        lda = LinearDiscriminantAnalysis(n_components=self.n_features).fit(self.X)
        lda_data = lda.transform(self.X)
        data = pd.DataFrame(lda_data, columns=self.dr_columns)

        return data
    
    def ica_algorithm(self):
        ica = FastICA(n_components=self.n_features).fit(self.X)
        ica_data = ica.transform(self.X)
        data = pd.DataFrame(ica_data, columns=self.dr_columns)

        return data
    
    def gaussian_random_proj_algorithm(self):
        grp = GaussianRandomProjection(n_components=self.n_features).fit(self.X)
        grp_data = grp.transform(self.X)
        data = pd.DataFrame(grp_data, columns=self.dr_columns)

        return data
    
    
    def tsne_algorithm(self):
        # Reshape the scalar to a 2D array
        # data_2d = np.array(self.X).reshape(-1, 1)
        tsne = TSNE(n_components=self.n_features)
        tsne_data = tsne.fit_transform(self.X)
        data = pd.DataFrame(tsne_data, columns=self.dr_columns)

        return data
    
    def isomap_algorithm(self):
        isomap = Isomap(n_components=self.n_features)
        isomap_data = isomap.fit_transform(self.X)
        data = pd.DataFrame(isomap_data, columns=self.dr_columns)

        return data
    

    def pca_contribution(self, data, data_  , n_components):
        # Access the principal components
        components = data_.components_

        # Get the variables contributing the most to each component
        contributing_variables = []

        # Iterate over the components
        for component in components:
            # Get the indices of the variables with the highest absolute values in the component
            contributing_indices = np.argsort(np.abs(component))[::-1][:n_components]
            contributing_variables.append([data.columns[i] for i in contributing_indices])

        print("Contributing Variables:")
        return contributing_variables


    def tsne_contribution(self, data, data_):
        # Get the variables in relation to the t-SNE output
        variable_contributions = []

        # Iterate over the components (only 2 in this case)
        for i in range(data_.shape[1]):
            # Get the variables' values for the given component
            component_values = data_[:, i]

            # Sort the variables based on their values for the component
            sorted_indices = np.argsort(component_values)

            # Get the names of the variables corresponding to the sorted indices
            sorted_variables = [data.columns[j] for j in sorted_indices]

            # Append the sorted variables to the variable_contributions list
            variable_contributions.append(sorted_variables)

        print("Variable Contributions:")
        return variable_contributions

    # def ile_algorithm(self):
    #     lle = LocallyLinearEmbedding(n_components=2)
    #     ile_data = lle.fit_transform(self.X)
    #     data = pd.DataFrame(ile_data, columns=self.dr_columns)

    #     return data


    def explainable():
        pass