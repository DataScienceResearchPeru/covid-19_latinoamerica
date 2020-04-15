from bs4 import BeautifulSoup
import urllib.request as urllib
import ssl
import json
import numpy as np
import pandas as pd
from datetime import date

"""
Variables a cambiar
"""
# Scraping
webpage = 'http://covid19honduras.org/dll/ODEPTO.php'

# ISO Code
default_columns = ['Number', 'Subdivision',
                   'ISO 3166-2 Code', 'Confirmed', 'Death', 'Recovered']
reorder_columns = ['ISO 3166-2 Code', 'Subdivision',
                   'Country', 'Last Update', 'Confirmed', 'Death', 'Recovered']


if __name__ == "__main__":
    """
    SCRAP DATA
    """
    print("We're going to scrap Honduras reports to create a pandas dataframe")
    # Creamos conexión SSL necesaria
    context = ssl._create_unverified_context()
    web = urllib.urlopen(webpage, context=context)
    soup = BeautifulSoup(web)
    clean_json = json.loads(str(soup))
    # to create a pandas dataframe with the data
    dataset = pd.DataFrame(clean_json)
    # Naming columns
    dataset.columns = default_columns
    dataset['Country'] = 'Honduras'
    dataset['Last Update'] = date.today()
    print(dataset)

    # Reorder columns
    dataset = dataset.reindex(columns=reorder_columns)
    print(dataset)

    """
    CHANGE REPOSITORY FAILS
    WARNING: TO_CSV TEMPORAL
    """
    dataset.to_csv(
        "utils/scripts/data_collection/honduras_temporal/{}.csv".format(date.today()), sep=',', index=False)
