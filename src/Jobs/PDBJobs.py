import pandas as pd
import urllib
import json
import datetime


class PDBJOBS:

    def load_data(self):
        #Read the ids from the mpstruc
        current_date = datetime.date.today().strftime('%Y-%m-%d')
        self.ids = pd.read_csv("mpstruck_ids.csv")
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
        except urllib.error.HTTPError:        
            pass
        
    
    def parse_data(self):
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
        data.to_csv("PDB Data.csv")