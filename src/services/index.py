
from src.services.basic_plots import home_page_graph

def home():
    heading = "Welcome to MPVIS"
    sub_heading = "Membrane Protein Visualization"
    body = "Membrane protein visualization is a crucial aspect of structural \
            biology that aims to understand the structure, function, and \
            interactions of proteins embedded in cellular membranes. \
            It involves the use of specialized software tools and techniques \
            to generate visual representations of membrane proteins, enabling \
            researchers to explore their three-dimensional structures and gain \
            insights into their biological roles.."
    
    other_content = "Key points to highlight in a summary of membrane protein visualization include:"
    basic = "In summary, membrane protein visualization is a multidisciplinary field that \
            combines experimental and computational approaches to generate visual \
            representations of membrane proteins. It enables researchers to explore protein \
            structures, study their interactions, and contribute to our understanding of \
            cellular processes and disease mechanisms."
    home_page_graph()