from src.implementation.Helpers.machine_learning_al.UnsupervisedMachineLearning import MachineLearning

class MachineLearningClustering:

    def __init__(self, filter:dict = {}, data):
        self.eps = filter.get('eps')
        self.n_clusters = filter.get('n_clusters')
        self.n_components = filter.get('n_components')
        self.min_samples = filter.get('min_samples')
        self.method = filter.get('machine_learning_selection')
        self.dr_data = data

    def preprocessings(self):
        pass


    def cluster(self):
        # Stage 3
        mls = MachineLearning(X=self.dr_data, eps=self.eps, min_samples=self.min_samples, n_clusters=self.n_clusters, n_components=self.n_components)
        classified_, params = getattr(mls, str(self.method).replace(' ', '_'))()
        # st.write(params)
        # Stage 4
        processed_df = self.dr_data.concat([self.dr_data[label_data].reset_index(drop=True), self.dr_data.reset_index(drop=True), classified_.reset_index(drop=True)], axis=1)
        # st.write(processed_df.head())
        processed_df.to_csv("PCA_combine.csv")

        # Stage 5
        if (not processed_df.empty):
            ml_label = str(machine_learning_selection).replace(' ', '_')
            st.write(pca_columns)
            try:
                graph_ml = Graph(processed_df)
                graph_ml = graph_ml.set_properties(pca_columns, ml_label, selection_avenue_default, selection_type_default)
                altair_graph_obj_ml = getattr(graph_ml, str(graph_dimension_selection).replace(' ', '_'))()
                altair_graph_objj_ml = altair_graph_obj_ml\
                    .encoding(label_data)\
                    .get_selection_avenue(selection_avenue)\
                    .add_selection(selection_type).config()\
                    .properties(width=800).interactive().legend_config().return_obj()
                # Display the chart in Streamlit
                st.altair_chart(altair_graph_objj_ml, use_container_width=True)
            except (AxisException, ValueError) as ex:
                st.write(str(ex))
