import altair as alt
import json
from src.implementation.Helpers.helper import remove_underscore_change_toupper, \
    format_string_caps
from src.implementation.exceptions.AxisExceptions import AxisException
from src.implementation.exceptions.NotFoundOnList import NotFoundOnList
from src.implementation.exceptions.TagDoesnotExist import TagDoesnotExist

class Graph:

    def __init__(self, data, axis:list = [], labels:str = "", selection_avenue_default:list = [], selection_type_default:list = []):
        self.data = data
        self.x = None
        self.y = None
        self.z = None # for multi dimension
        self.w = None # for multi dimension
        self.altair_obj = None
        self.selection_avenue = "drag"
        self.encoded_x = None
        self.encoded_y = None

        self.axis   = axis
        self.labels = labels
        # defaults
        self.selection_avenue_default   = selection_avenue_default
        self.selection_type_default     = selection_type_default

        # acceptable tags
        self.acceptable_encoding_tags = ["norminal", "temporal", "quantitative", "ordinal"]


    def set_properties(self, axis:list = [], labels:str = "", selection_avenue_default:list = [], selection_type_default:list = []):
        self.axis   = axis
        self.labels = labels
        # defaults
        self.selection_avenue_default   = selection_avenue_default
        self.selection_type_default     = selection_type_default
        
        return self

    def encoding_tags(self, encoding_tags:list=[], tooltips:list = []):
        if (len(self.axis) == len(encoding_tags) or len(encoding_tags) == 0):
            """
                This implementation can still be optimized.
            """
            # Title label
            title_x = remove_underscore_change_toupper(tooltips[0])
            title_y = remove_underscore_change_toupper(tooltips[1])

            # check with default tags if exist
            if(len(encoding_tags) > 0):
                x_tag, y_tag = encoding_tags
                my_x_axis = self.x+":"+str(x_tag[0]).capitalize()
                my_y_axis = self.y+":"+str(y_tag[0]).capitalize()
                
                if x_tag in self.acceptable_encoding_tags and y_tag in self.acceptable_encoding_tags:
                    self.encoded_x = alt.X(my_x_axis, title = title_x)
                    self.encoded_y = alt.Y(my_y_axis, title = title_y)
                else:
                    raise TagDoesnotExist("This tag with the name "+x_tag+" or "+y_tag+" does not exist. Acceptable tags includes: "+", ".join(self.acceptable_encoding_tags))
            else:
                my_x_axis = self.x
                my_y_axis = self.y
                self.encoded_x = alt.X(my_x_axis, title = title_x)
                self.encoded_y = alt.Y(my_y_axis, title = title_y)
        else:
            raise AxisException("Axis specified is not equal to the selected encoding tags.")


    def scatter_plot(self):
        if (len(self.axis) != 2):
            raise AxisException("Axis specified is not equal to the selected dimension.")
        
        self.x, self.y = self.axis
        self.altair_obj = alt.Chart(self.data).mark_point()
        return self
    
    def line_plot(self):
        self.x, self.y = self.axis
        self.altair_obj = alt.Chart(self.data).mark_line()
        return self
    
    def area_plot(self):
        self.x, self.y = self.axis
        self.altair_obj = alt.Chart(self.data).mark_area()
        return self
    
    def bar_plot(self):
        self.x, self.y = self.axis
        self.altair_obj = alt.Chart(self.data).mark_bar()
        return self
    
    def circle_plot(self):
        self.x, self.y = self.axis
        self.altair_obj = alt.Chart(self.data).mark_circle()
        return self
    
    def rect_plot(self):
        self.x, self.y = self.axis
        self.altair_obj = alt.Chart(self.data).mark_rect()
        return self
    
    def box_plot(self):
        self.x, self.y = self.axis
        self.altair_obj = alt.Chart(self.data).mark_boxplot()
        return self
    
    def pie_plot(self):
        self.x, self.y = self.axis
        self.altair_obj = alt.Chart(self.data).mark_pie()
        return self
    
    
    def violin_plot(self):
        self.x, self.y = self.axis
        self.altair_obj = alt.Chart(self.data).transform_density(
            self.x,
            as_=[self.x, self.y],
            extent=[5, 50],
            groupby=['Origin']
        ).mark_area(orient='horizontal')
        return self
    
    def point_plot(self):
        self.x, self.y = self.axis
        self.altair_obj = alt.Chart(self.data).mark_point()
        return self

    
    def encoding(self, tooltips:list = [], encoding_tags:list = []):

        # manage color patterns
        # selection = alt.selection_point(fields=[self.y])
        # color = alt.condition(
        #     selection,
        #     alt.Y(self.y).legend(None),
        #     alt.value('lightgray')
        # )
        color = self.labels+':N' if (len(self.labels) > 0) else alt.Color(scale=alt.Scale(scheme='category20'))
        # set tooltips

        tooltip_list = [alt.Tooltip(tooltip, title=format_string_caps(tooltip.capitalize())) for tooltip in tooltips]

        # setting encoding tags

        self.encoding_tags(encoding_tags, tooltips)
        if (len(self.axis) == 2):
            self.altair_obj = self.altair_obj.encode(
                self.encoded_x,
                self.encoded_y,
                color=color,
                tooltip=tooltip_list,
                # shape=self.encoded_x
            )

        elif(len(self.axis) == 3):
            """Possible we might encounter cases like this 3D"""
            self.altair_obj = self.altair_obj.encode(
                alt.X(self.x),
                alt.Y(self.y),
                alt.Z(self.z),
                color=color,
                tooltip=tooltip_list,
                # shape=self.encoded_x
            )

        elif(len(self.axis) == 4):
            """Possible we might encounter cases like this 4D"""
            self.altair_obj = self.altair_obj.encode(
                alt.X(self.x),
                alt.Y(self.y),
                alt.Z(self.z),
                alt.W(self.w),
                color=color,
                tooltip=tooltip_list,
                # shape=self.encoded_x
            )
        else:
            self.altair_obj = self.altair_obj.encode(
                alt.X(self.x),
                alt.Y(self.y),
                color=color,
                tooltip=tooltip_list,
                # shape=self.encoded_x
            )

        return self
    
    def get_selection_avenue(self, selection_avenue = "drag"):
        if(selection_avenue not in self.selection_avenue_default):
            raise NotFoundOnList("selected option is not on the list")
        self.selection_avenue = selection_avenue
        return self
    
    def add_selection(self, type:str = 'single'):
        if(type not in self.selection_type_default):
            raise NotFoundOnList("selected option is not on the list")
        
        if(type == 'single'):
            selection = alt.selection_single(on=self.selection_avenue, name='MySelection')
        elif(type == 'multiple'):
            selection = alt.selection_multi(on=self.selection_avenue, name='MySelection')
        elif(type == 'interval'):
            selection = alt.selection_interval(on=self.selection_avenue, name='MySelection')
        else:
            selection = alt.selection_single(on=self.selection_avenue, encodings=['x'], name='MySelection')

        self.altair_obj = self.altair_obj.add_selection(selection)

        return self
    
    def properties(self, width=200, height = None, title = ""):
        # Set the width and height of the chart
        self.altair_obj = self.altair_obj.properties(
            title=title,
            # width=width,  # Set the width
            # height=height # set the height of the graph
        )
        return self


    def config(self, label_font_size=12, title_font_size=14, font_size=16, font_weight='bold', conf='{"color": "#a855f7", "opacity": 0.9}'):

        self.altair_obj = self.altair_obj.configure_axis(
            labelFontSize=label_font_size,
            titleFontSize=title_font_size
        ).configure_title(
            fontSize=font_size,
            fontWeight=font_weight
        )
        
        self.configure_mark(conf["color"], float(conf["opacity"]))

        return self
    
    def merge_charts(self, chart_list:list=[]):
        # Combine the two charts
        combined_chart = alt.layer(
            *chart_list
        ).resolve_scale(color='independent')

        return combined_chart
    
    def merge_charts_horizontally(self, chart_list:list=[]):
        # Combine the two charts
        combined_chart = alt.hconcat(
            *chart_list
        ).resolve_scale(color='independent')

        return combined_chart

        
    def merge_charts_vertically(self, chart_list:list=[]):
        # Combine the two charts
        combined_chart = alt.vconcat(
            *chart_list
        ).resolve_scale(color='independent')

        return combined_chart
    
    def configure_mark(self, color='#a855f7', opacity=1):
        self.altair_obj = self.altair_obj.configure_mark(
            opacity=opacity,
            color= color
        )
        return self
    
    def legend_config(self):
        # self.altair_obj = self.altair_obj.configure_legend(
        #     strokeColor='gray',
        #     fillColor='#EEEEEE',
        #     padding=10,
        #     cornerRadius=10,
        #     orient='top-right'
        # )
        return self
    

    def interactive(self):
        self.altair_obj = self.altair_obj.interactive()  # Make the chart interactive

        return self

    def return_obj(self):
        return self.altair_obj
    
    def return_dict_obj(self):
        return self.altair_obj.to_dict()
    
    def show(self):
        return self.altair_obj.show()
    
    @staticmethod
    def correlation_matrix(data, variables:list = ['variable2:O', 'variable:O'], correlation_col:str = "correlation:Q", correlation_label:str = "correlation_label", display_value_text:bool = False):
        base = alt.Chart(data).encode(
            x=variables[0],
            y=variables[1]    
        )

        # Text layer with correlation labels
        # Colors are for easier readability
        if (display_value_text):
            text = base.mark_text().encode(
                text=correlation_label,
                color=alt.condition(
                    alt.datum.correlation > 0.5, 
                    alt.value('white'),
                    alt.value('black')
                )
            )

        # The correlation heatmap itself
        cor_plot = base.mark_rect().encode(
            color=correlation_col
        )

        if(display_value_text):
            chart = cor_plot + text
        else:
            chart = cor_plot

        return chart


    @staticmethod
    def outlier_visualization(df):
        # Melt the DataFrame to convert it to long format
        df_melted = df.melt(var_name='Column', value_name='Value')

        # Create a box plot with Altair
        box_plot = alt.Chart(df_melted).mark_boxplot().encode(
            x='Column:O',
            y='Value:Q'
        )

        # Create a scatter plot with Altair
        scatter_plot = alt.Chart(df_melted).mark_circle().encode(
            x='Column:O',
            y='Value:Q'
        )

        # Combine both plots
        combined_plot = box_plot + scatter_plot

        # Display the combined plot
        return combined_plot
    

    @staticmethod
    def plot_bar_chat(df, x_axis = "", conf={}):
        # Create an Altair bar chart with sorting based on 'Value'
        return alt.Chart(df).mark_bar().encode(
            y=alt.X(x_axis+':N', sort="-x"),
            x=alt.Y('Values:Q'),
            tooltip=[alt.Tooltip(tooltip, title=format_string_caps(tooltip.capitalize())) for tooltip in [x_axis, 'Values']]
        ).configure_mark(
            opacity= conf["opacity"],
            color= conf["color"]
        )