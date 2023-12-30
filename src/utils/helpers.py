from Bio import PDB

def date_to_string(raw_date):
    return "{}".format(raw_date)


    """
    The parameters cell_angle_alpha, cell_angle_beta, cell_angle_gamma, cell_length_a, cell_length_b, cell_length_c, and cell_zpdb are typically associated with crystallographic data and describe the unit cell of a crystal structure. Here's a brief explanation of each parameter:

    Cell Angles (Alpha, Beta, Gamma):

    These represent the angles between the edges of the unit cell.
    cell_angle_alpha: The angle between the b and c axes.
    cell_angle_beta: The angle between the a and c axes.
    cell_angle_gamma: The angle between the a and b axes.
    Cell Lengths (a, b, c):

    These represent the lengths of the edges of the unit cell.
    cell_length_a: The length of the a axis.
    cell_length_b: The length of the b axis.
    cell_length_c: The length of the c axis.
    Cell Zpdb:

    This parameter is less standard and may be specific to certain datasets or databases.
    It may represent a specific attribute related to the unit cell, possibly in the context of a particular database or study.
    These parameters are crucial in crystallography, where scientists study the arrangement of atoms in crystalline materials. The unit cell is the basic repeating unit of the crystal lattice, and its dimensions and angles define the crystal structure.

    Potential analyses you can perform with these parameters include:

    Crystal System Identification:

    Analyzing these parameters can help identify the crystal system to which a crystal belongs (e.g., cubic, tetragonal, orthorhombic, etc.).
    Comparing Structures:

    You can compare the unit cell parameters of different crystal structures to identify similarities or differences.
    Quality Control:

    Checking for anomalies or outliers in these parameters may be part of quality control for crystallographic data.
    Structure Prediction:

    Predicting or validating crystal structures based on these parameters is an area of research.
    Property Correlations:

    Correlating unit cell parameters with physical or chemical properties of the material.
    It's important to note that the specific analysis depends on the context of your data and the scientific questions you are trying to answer. If you have additional information about the dataset or a specific research question, I can provide more tailored guidance.
    """
def identify_crystal_system(alpha, beta, gamma, a, b, c):
    # Define tolerance for parameter comparisons
    tolerance = 1e-5

    # Cubic system criteria
    if abs(alpha - 90) < tolerance and abs(beta - 90) < tolerance and abs(gamma - 90) < tolerance and abs(a - b) < tolerance and abs(b - c) < tolerance and abs(a - c) < tolerance:
        return "Cubic"

    # Tetragonal system criteria
    elif abs(alpha - 90) < tolerance and abs(beta - 90) < tolerance and abs(gamma - 90) < tolerance and abs(a - b) < tolerance and abs(b - c) < tolerance and abs(a - c) < tolerance:
        return "Tetragonal"

    # Orthorhombic system criteria
    elif abs(alpha - 90) < tolerance and abs(beta - 90) < tolerance and abs(gamma - 90) < tolerance and abs(a - b) < tolerance and abs(b - c) < tolerance and abs(a - c) < tolerance:
        return "Orthorhombic"

    # Rhombohedral system criteria
    elif abs(alpha - 60) < tolerance and abs(beta - 60) < tolerance and abs(gamma - 60) < tolerance and abs(a - b) < tolerance and abs(b - c) < tolerance and abs(a - c) < tolerance:
        return "Rhombohedral"

    # Monoclinic system criteria
    elif abs(alpha - 90) < tolerance and abs(beta - 90) < tolerance and abs(gamma - 90) < tolerance and abs(a - c) < tolerance and abs(alpha - 90) >= tolerance and abs(beta - 90) >= tolerance and abs(gamma - 90) >= tolerance:
        return "Monoclinic"

    # Triclinic system criteria
    else:
        return "Triclinic"
    
    
def kyte_doolittle(sequence):
    # Define the Kyte-Doolittle hydrophobicity scale
    hydrophobicity_scale = {
        'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5,
        'C': 2.5, 'Q': -3.5, 'E': -3.5, 'G': -0.4,
        'H': -3.2, 'I': 4.5, 'L': 3.8, 'K': -3.9,
        'M': 1.9, 'F': 2.8, 'P': -1.6, 'S': -0.8,
        'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
    }

    # Convert the sequence to uppercase
    sequence = sequence.upper()

    # Calculate the Kyte-Doolittle hydrophobicity score for the sequence
    score = sum(hydrophobicity_scale.get(aa, 0) for aa in sequence)

    return score

"""
# Example usage
protein_sequence = "METHINKS IT IS LIKE A WEASEL"
result = kyte_doolittle(protein_sequence)
print(f"Kyte-Doolittle Hydrophobicity Score: {result}")
"""


def calculate_protein_symmetry(pdb_id):
    # Create a PDB parser
    parser = PDB.PDBParser(QUIET=True)

    # Fetch the PDB file
    pdb_file = PDB.PDBList()
    pdb_file.retrieve_pdb_file(pdb_id, file_format="pdb", pdir=".")

    # Load the structure
    structure = parser.get_structure(pdb_id, f"{pdb_id.lower()}.pdb")

    # Get the biological assembly
    bio_assembly = structure.header['biological_assemblies']

    # Perform symmetry analysis
    symmetry_operations = analyze_symmetry(bio_assembly)

    # Update symmetry information (example: print it)
    print(f"Symmetry for {pdb_id}: {symmetry_operations}")

def analyze_symmetry(bio_assembly):
    # Create a SymmetryFinder object
    symmetry_finder = PDB.Symmetry.SymmetryFinder()

    # Iterate through each biological assembly and analyze symmetry
    symmetry_operations = []
    for assembly_id in bio_assembly:
        assembly = bio_assembly[assembly_id]
        symmetry = symmetry_finder.find_operators(assembly)
        symmetry_operations.extend(symmetry)

    return symmetry_operations