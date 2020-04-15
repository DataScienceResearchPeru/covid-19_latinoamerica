import urllib.request as urllib
from bs4 import BeautifulSoup
import json
import re
import numpy as np
import pandas as pd
from datetime import date

"""
Variables a cambiar
"""
# Scraping
webpage = "https://e.infogram.com/_/fx5xud0FhM7Z9NS6qpxs?src=embed"
tag = "script"
tag_number = 4
variable_json = "window.infographicData="
seq = ['elements', 'content', 'content', 'entities', '777cd339-9f0a-4acc-8e3d-7a245cbc1b17',
       'props', 'chartData', 'data', 0]  # seq to find data

# ISO Code
iso_file = "https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/utils/iso3166-2.csv"
external_subdivisions = ['AHUACHAPÁN', 'CABAÑAS', 'CHALATENANGO', 'CUSCATLÁN', 'LA LIBERTAD', 'LA PAZ',
                         'LA UNIÓN', 'MORAZÁN', 'SAN MIGUEL', 'SAN SALVADOR', 'SAN VICENTE', 'SANTA ANA', 'SONSONATE', 'USULUTÁN']
filt_col = ['Code', 'Subdivision Name Used']
ctryiso = "SV"
iso_col_name="ISO 3166-2 Code"


if __name__ == "__main__":
    """
    SCRAP DATA
    """
    print("We're going to scrap El Salvador Gov reports to create a pandas dataframe")
    web = urllib.urlopen(webpage)
    soup = BeautifulSoup(web.read())
    data = soup.find_all(tag)[tag_number].string
    # -1 for ";" at the final
    dirty_json = data.replace(variable_json, " ")[:-1]
    clean_json = json.loads(dirty_json)
    # sequence in json to find data
    clean_json = clean_json[seq[0]][seq[1]][seq[2]][seq[3]][seq[4]]
    cases_per_subdivision = clean_json[seq[5]][seq[6]][seq[7]][seq[8]]
    table = np.array(cases_per_subdivision)
    # to create a pandas dataframe with the data
    dataset = pd.DataFrame({table[0, 0]: table[1:, 0],
                            table[0, 1]: table[1:, 1],
                            table[0, 2]: table[1:, 2]})
    print(dataset)

    """
    ADD ONE COLUM WITH ISO
    """
    print("We're going to match ISO CODE")
    iso = pd.read_csv(iso_file)
    isocode_el_salvador = iso[iso['Country Code'] == ctryiso][filt_col]
    isocode_el_salvador['External Subdivision Name'] = external_subdivisions
    print(isocode_el_salvador)

    """
    ADDING ISO TO DATA SCRAPPED
    """
    print("We're going to add ISO column to data scrapped")
    #Initialize colum
    dataset[iso_col_name]=0
    dataset["Date"]=date.today()
    for index, row in dataset.iterrows():
        subdivision=dataset['DEPARTAMENTO'][index]
        if subdivision!=None:
            cod=isocode_el_salvador[isocode_el_salvador['External Subdivision Name']==subdivision]['Code']
        else:
            print("Please check dataset variable, there's None row. We're going to fix for you. Check row below.")
            subdivision=dataset['DEPARTAMENTO'][index-1]
            cod=isocode_el_salvador[isocode_el_salvador['External Subdivision Name']==subdivision]['Code']        
        dataset[iso_col_name][index]=cod.values[0]
    print (dataset)

    """
    CHANGE REPOSITORY FAILS
    WARNING: TO_CSV TEMPORAL
    """
    dataset.to_csv("utils/scripts/data_collection/el_salvador_temporal/{}.csv".format(date.today()), sep=',', index=False)