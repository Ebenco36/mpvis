import os
import re
import json
import urllib
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup



"""
    We are doing this for PDB code that has been replaced with something else.
    If PDB assertion number is not found while enrichment is going on then 
    try to check if it was replaced with something else. As of now, we discovered that 
    some PDB codes were replace thereby causing some issues.
"""

def extract_pdb_code(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the link containing the replacement PDB code
    replacement_link = soup.find('a', href=re.compile(r'/structure/(\w+)'))

    if replacement_link:
        # Extract the PDB code from the href attribute
        replacement_pdb_code = replacement_link['href'].split('/')[-1]
        return replacement_pdb_code
    else:
        return None
    
    
def check_pdb_replacement(pdb_code):
    # PDB website URL for a specific entry
    pdb_url = f"https://www.rcsb.org/structure/removed/{pdb_code}"

    # Send a GET request to the PDB website
    response = requests.get(pdb_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Check if the page contains a specific message indicating replacement
        content = response.text
        # Use regular expression to find the next 100 characters after "replaced"
        match = re.search(r'replaced(.{1,100})', content, re.IGNORECASE)
        
        if match:
            next_100_chars = match.group(1).strip()
            res = extract_pdb_code(next_100_chars)
            return res
        else:
            return pdb_code
    else:
        return pdb_code
    
class PDBJOBS:
    
    def create_directory(self, directory_path):
        try:
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created successfully.")
        except FileExistsError:
            print(f"Directory '{directory_path}' already exists.")
            

    def load_data(self):
        # create directory
        self.create_directory("datasets")
        #Read the ids from the mpstruc
        current_date = datetime.date.today().strftime('%Y-%m-%d')
        self.ids = pd.read_csv("./datasets/mpstruct_ids.csv")
        protein_entries = []

        return self


    #Fetch the information on the ids 
    def read_in(self, ident):
        pdb_id = ident 
        try:
            # Fetch data for the original PDB ID
            req = urllib.request.urlopen("https://data.rcsb.org/rest/v1/core/entry/" + pdb_id)
            data = json.load(req)
            data = pd.json_normalize(data)
            data.insert(1, "Pdb Code", pdb_id)
            data.insert(2, "Is Replaced", "Replaced")
            data.insert(3, "PDB Code Changed", "")
            return data
        except urllib.error.HTTPError as e:
            # If there's an HTTP error, check for replacement PDB ID
            check_phase_2 = check_pdb_replacement(pdb_id)

            # Fetch data for the replacement PDB ID
            try:
                req = urllib.request.urlopen("https://data.rcsb.org/rest/v1/core/entry/" + str(check_phase_2))
                data = json.load(req)
                data = pd.json_normalize(data)
                data.insert(1, "Pdb Code", pdb_id)
                data.insert(2, "Is Replaced", "Not Replaced")
                data.insert(3, "PDB Code Changed", pdb_id + " was replaced by " + check_phase_2)
                return data
            except urllib.error.HTTPError as e:
                # If there's still an HTTP error, print an error message
                print("There is an issue with : https://data.rcsb.org/rest/v1/core/entry/" + pdb_id)
            
            
        """
            OLD implementation
            try:
                req = urllib.request.urlopen("https://data.rcsb.org/rest/v1/core/entry/" + ident)
                data = json.load(req)
                data = pd.json_normalize(data)
                data.insert(1, "Pdb Code", pdb_id)
                return data
            except urllib.error.HTTPError as e:
                print("There is an issue with : https://data.rcsb.org/rest/v1/core/entry/" + ident)
        """
    
    def parse_data(self):
        # create directory
        self.create_directory("datasets")
        ids = self.ids["Pdb Code"]
        data = pd.DataFrame()

        #Read in all the information about the ids and display at which id you are at the moment
        i = 0
        for one_id in ids:
            entry = self.read_in(str(one_id))
            # Not available any more
            # data = data.append(entry)
            # Append the new DataFrame to the existing DataFrame

            # New method
            data = pd.concat([data, entry], ignore_index=True)
            i += 1
            if (i%10 == 0):
                print ("Currently at:", i)

        #Save the resulting data in a .csv-table
        data.to_csv("./datasets/PDB_data.csv")
        
    
    def fetch_data(self):
        return self.load_data().parse_data()
    
    
    def convert_month(self, mon):
        if (mon == "Jan"):
            return 1
        if (mon == "Feb"):
            return 2
        if (mon == "Mar"):
            return 3
        if (mon == "Apr"):
            return 4
        if (mon == "May"):
            return 5
        if (mon == "Jun"):
            return 6
        if (mon == "Jul"):
            return 7
        if (mon == "Aug"):
            return 8
        if (mon == "Sep"):
            return 9
        if (mon == "Oct"):
            return 10
        if (mon == "Nov"):
            return 11
        if (mon == "Dec"):
            return 12
    

    
        
        
# Instantiate the class and call the function
pdb_obj = PDBJOBS()
pdb_obj.fetch_data()