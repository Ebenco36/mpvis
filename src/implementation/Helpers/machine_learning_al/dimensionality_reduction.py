from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.random_projection import GaussianRandomProjection
from sklearn.manifold import LocallyLinearEmbedding
from sklearn.decomposition import PCA, FastICA, TruncatedSVD, NMF, FactorAnalysis
from sklearn.manifold import TSNE
from sklearn.manifold import Isomap
import pandas as pd
import numpy as np
import json
import altair as alt

class DimensionalityReduction:
    def __init__(self, X, n_features=2, pca_columns:list=[]):
        self.X = X
        self.n_features = n_features if n_features > 1 else 2
        self.dr_columns = pca_columns

    def pca_algorithm(self):
        model = PCA(self.n_features).fit(self.X)
        model_data = model.transform(self.X)
        data = pd.DataFrame(model_data, columns=self.dr_columns)
        explainable = self.explainable(model, self.X.columns)

        return data, explainable
    
    def TruncatedSVD_algorithm(self):
        model = TruncatedSVD(self.n_features).fit(self.X)
        model_data = model.transform(self.X)
        data = pd.DataFrame(model_data, columns=self.dr_columns)
        explainable = self.explainable(model, self.X.columns)

        return data, explainable
    
    def NMF_algorithm(self):
        model = NMF(self.n_features).fit(self.X)
        model_data = model.transform(self.X)
        data = pd.DataFrame(model_data, columns=self.dr_columns)
        explainable = self.explainable(model, self.X.columns)

        return data, explainable
    
    def FactorAnalysis_algorithm(self):
        model = FactorAnalysis(self.n_features).fit(self.X)
        model_data = model.transform(self.X)
        data = pd.DataFrame(model_data, columns=self.dr_columns)
        explainable = self.explainable(model, self.X.columns)

        return data, explainable
    # def lda_algorithm(self):
    #     lda = LinearDiscriminantAnalysis(n_components=self.n_features).fit(self.X)
    #     lda_data = lda.transform(self.X)
    #     data = pd.DataFrame(lda_data, columns=self.dr_columns)

    #     return data
    
    def ica_algorithm(self):
        model = FastICA(n_components=self.n_features).fit(self.X)
        model_data = model.transform(self.X)
        data = pd.DataFrame(model_data, columns=self.dr_columns)
        explainable = self.explainable(model, self.X.columns)

        return data, explainable
    
    def gaussian_random_proj_algorithm(self):
        model = GaussianRandomProjection(n_components=self.n_features).fit(self.X)
        model_data = model.transform(self.X)
        data = pd.DataFrame(model_data, columns=self.dr_columns)
        explainable = self.explainable(model, self.X.columns)

        return data, explainable
    
    def tsne_algorithm(self):
        # Reshape the scalar to a 2D array
        # data_2d = np.array(self.X).reshape(-1, 1)
        model = TSNE(n_components=self.n_features)
        model_data = model.fit_transform(self.X)
        data = pd.DataFrame(model_data, columns=self.dr_columns)
        explainable = self.explainable(model, self.X.columns)

        return data, explainable
    
    def isomap_algorithm(self):
        model = Isomap(n_components=self.n_features)
        model_data = model.fit_transform(self.X)
        data = pd.DataFrame(model_data, columns=self.dr_columns)
        explainable = self.explainable(model, self.X.columns)

        return data, explainable
    

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


    def explainable(self, model, features:list = []):
        n_components = model.components_
        explained_variance_ratio = None

        if hasattr(model, 'explained_variance_ratio_'):
            explained_variance_ratio = model.explained_variance_ratio_

        # Given NDArray
        data_array = n_components

        # Convert the array to a Pandas DataFrame
        df = pd.DataFrame(data_array, columns=features)
        data_transformed = df.T
        data_transformed.columns = self.dr_columns

        # Create a list to store individual charts
        charts = []
        
        # Loop through the columns and create charts
        for col in self.dr_columns:
            chart = alt.Chart(data_transformed.reset_index()).mark_bar().encode(
                x='index',
                y=col,
                color=alt.value('blue')
            ).properties(
                title=f'Plot of {col} against x (Attributes)'
            )
            charts.append(chart)

        # Concatenate the charts vertically
        combined_charts = alt.hconcat(*charts)

        graph_data = combined_charts.to_dict()

        return {
            "explained_variance_ratio": explained_variance_ratio.tolist() if not explained_variance_ratio is None else [],
            "n_components": n_components.tolist(),
            "graph_data": graph_data,
        }