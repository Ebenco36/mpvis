import os
import pandas as pd
import urllib
import requests
import json
import datetime


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
            req = urllib.request.urlopen("https://data.rcsb.org/rest/v1/core/entry/" + ident)
            data = json.load(req)
            data = pd.json_normalize(data)
            data.insert(1, "Pdb Code", pdb_id)
            return data
        except urllib.error.HTTPError as e:
            print("There is an issue with : https://data.rcsb.org/rest/v1/core/entry/" + ident)
        
    
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