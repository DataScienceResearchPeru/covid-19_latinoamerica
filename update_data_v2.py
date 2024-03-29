import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests
import fuckit

import utils.scripts.data_collection.data.peru_data_v2 as peru_data
import utils.scripts.data_collection.data.ecuador_data_v2 as ecuador_data
import utils.scripts.data_collection.data.cuba_data_v2 as cuba_data
import utils.scripts.data_collection.data.bolivia_data_v2 as bolivia_data
import utils.scripts.data_collection.data.brazil_data_v2 as brazil_data
import utils.scripts.data_collection.data.republica_dominicana_data_v2 as republica_domicana_data
import utils.scripts.data_collection.data.argentina_data_v2 as argentina_data
import utils.scripts.data_collection.data.colombia_data_v2 as colombia_data
import utils.scripts.data_collection.data.costa_rica_data_v2 as costa_rica_data
import utils.scripts.data_collection.data.nicaragua_data_v2 as nicaragua_data
import utils.scripts.data_collection.data.uruguay_data_v2 as uruguay_data
import utils.scripts.data_collection.data.francia_data_v2 as francia_data


import utils.scripts.data_time_series.time_series_generator as time_series_generator


PATH_DSRP_DAILY_REPORTS = "latam_covid_19_data/daily_reports/"
DATA_TEMPLATE_URL = "https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/templates/daily_report.csv"
PATH_CUBA = "utils/scripts/data_collection/data/cuba_temporal/"
PATH_ECUADOR = "utils/scripts/data_collection/data/ecuador_temporal/"
PATH_PERU = "utils/scripts/data_collection/data/peru_temporal/"
PATH_BOLIVIA = "utils/scripts/data_collection/data/bolivia_temporal/"
PATH_BRAZIL = "utils/scripts/data_collection/data/brazil_temporal/"
PATH_REPUBLICA_DOMINICANA = "utils/scripts/data_collection/data/republica_dominicana_temporal/"
PATH_ARGENTINA = "utils/scripts/data_collection/data/argentina_temporal/"
PATH_COLOMBIA = "utils/scripts/data_collection/data/colombia_temporal/"
PATH_COSTA_RICA = "utils/scripts/data_collection/data/costa_rica_temporal/"
PATH_NICARAGUA = "utils/scripts/data_collection/data/nicaragua_temporal/"
PATH_URUGUAY = "utils/scripts/data_collection/data/uruguay_temporal/"
PATH_FRANCIA = "utils/scripts/data_collection/data/francia_temporal/"


def logo():
    print(
        """                                                                                       
    ,ad8888ba,    ,ad8888ba,   8b           d8  88  88888888ba,              88   ad88888ba   
    d8"'    `"8b  d8"'    `"8b  `8b         d8'  88  88      `"8b           ,d88  d8"     "88  
   d8'           d8'        `8b  `8b       d8'   88  88        `8b        888888  8P       88  
   88            88          88   `8b     d8'    88  88         88            88  Y8,    ,d88  
   88            88          88    `8b   d8'     88  88         88  aaaaaaaa  88   "PPPPPP"88  
   Y8,           Y8,        ,8P     `8b d8'      88  88         8P  """
        """""  88           8P  
    Y8a.    .a8P  Y8a.    .a8P       `888'       88  88      .a8P             88  8b,    a8P   
    `"Y8888Y"'    `"Y8888Y"'         `8'        88  88888888Y"'              88  `"Y8888P'    
                                                                                                
                                                                                                
                                                                                                
    88888888ba                        88888888ba,     ad88888ba   88888888ba   88888888ba       
    88      "8b                       88      `"8b   d8"     "8b  88      "8b  88      "8b      
    88      ,8P                       88        `8b  Y8,          88      ,8P  88      ,8P      
    88aaaaaa8P'  8b       d8  888     88         88  `Y8aaaaa,    88aaaaaa8P'  88aaaaaa8P'      
    88"""
        """8b,  `8b     d8'  888     88         88    `'''''8b,  88''''88'    88"""
        """'        
    88      `8b   `8b   d8'           88         8P          `8b  88    `8b    88               
    88      a8P    `8b,d8'    888     88      .a8P   Y8a     a8P  88     `8b   88               
    88888888P"       Y88'     888     88888888Y"'     "Y88888P"   88      `8b  88               
                     d8'                                                                        
                    d8'                                                                         
    """
    )


def generate_list_dates(path):
    # Generate dates from files existing
    date_list_csv = []
    path, dirs, files = next(os.walk(path))
    numero_archivos = len(files)
    print("There is {} files on the path and one is README. We iterate {} times...".format(numero_archivos, numero_archivos - 1))
    # dates
    base = (datetime.today()).date()
    numdays = 5#numero_archivos - 1
    date_list_csv = [str(base - timedelta(days=x)) + str(".csv") for x in range(numdays)]
    print("Adding {} dates in a list...".format(len(date_list_csv)))
    date_list = []
    print("List of dates csv:", date_list_csv)
    for d in date_list_csv:
        date_list.append(d[:-4])
    print("List of dates:", date_list)
    return date_list_csv, date_list


def fix_format(df):
    df = df.fillna("")

    for m in range(len(df)):

        if df.loc[m]["Confirmed"] != "":
            a = int(float(df.loc[m]["Confirmed"]))
        else:
            a = ""

        if df.loc[m]["Deaths"] != "":
            b = int(float(df.loc[m]["Deaths"]))
        else:
            b = ""

        if df.loc[m]["Recovered"] != "":
            c = int(float(df.loc[m]["Recovered"]))
        else:
            c = ""

        df.loc[m, ["Confirmed"]] = str(a)
        df.loc[m, ["Deaths"]] = str(b)
        df.loc[m, ["Recovered"]] = str(c)

    return df


@fuckit  # https://stackoverflow.com/a/50051815/10491422
def load_all_data_temporal(list_date_list):

    print("[load_all_data_temporal] STARTING...")

    peru_data.load_and_generatecsv(list_date_list)
    ecuador_data.load_and_generatecsv(list_date_list)
    cuba_data.load_and_generatecsv(list_date_list)
    bolivia_data.load_and_generatecsv(list_date_list)
    brazil_data.load_and_generatecsv(list_date_list)
    republica_domicana_data.load_and_generatecsv(list_date_list)
    ecuador_data.load_and_generatecsv(list_date_list)
    argentina_data.load_and_generatecsv(list_date_list)
    colombia_data.load_and_generatecsv(list_date_list)
    costa_rica_data.load_and_generatecsv(list_date_list)
    nicaragua_data.load_and_generatecsv(list_date_list)
    uruguay_data.load_and_generatecsv(list_date_list)
    francia_data.load_and_generatecsv(list_date_list)

    print("[load_all_data_temporal] END...")


def update_data_per_country(df_template, path, d, isocode):

    try:
        df_template = df_template.set_index("ISO 3166-2 Code")
        MY_PATH = f"{path+d}.csv"
        df = pd.read_csv(MY_PATH)
        df = df.set_index("ISO 3166-2 Code")

        df_template.update(df)

    except Exception as e:
        print(f"Exception caughted in {isocode} -> {path+d}.csv")

    finally:

        df_template = df_template.reset_index(drop=False)
        return df_template


if __name__ == "__main__":

    logo()

    df_template = pd.read_csv(DATA_TEMPLATE_URL)
    df_template = df_template.fillna("")

    date_list_csv, date_list = generate_list_dates(PATH_DSRP_DAILY_REPORTS)

    if datetime.now().day % 7 == 0:
        # End of weekend
        data_loader_per_days = date_list[0:7]
    else:
        # any other day
        data_loader_per_days = date_list[0:1]
    # elif datetime.now().day % 29 == 0:
    #     # End of month
    #     data_loader_per_days = date_list[0:29]

    load_all_data_temporal(data_loader_per_days)

    # Days to check if file exists
    for day in date_list:  # date_list
        URL = f"https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/daily_reports/{day}.csv"

        # Check if file exists, if not -> create based on template
        try:
            response = requests.head(URL)
        except Exception as e:
            print(f"NOT OK: {str(e)}")
        else:
            if response.status_code == 200:
                print(f"OK daily/{day}.csv exists, using that file as DataFrame.")
            else:
                print(f"NOT OK: HTTP response code {response.status_code}")
                print(f"Creating file {day}.csv")
                df_template.to_csv(PATH_DSRP_DAILY_REPORTS + day + ".csv", index=False)

        try:
            # Use template
            df_template = pd.read_csv(URL)
            # Update data
            data_updated = update_data_per_country(df_template, PATH_ECUADOR, day, "EC-")
            data_updated = update_data_per_country(data_updated, PATH_PERU, day, "PE-")
            data_updated = update_data_per_country(data_updated, PATH_CUBA, day, "CU-")
            data_updated = update_data_per_country(data_updated, PATH_BOLIVIA, day, "BO-")
            data_updated = update_data_per_country(data_updated, PATH_BRAZIL, day, "BR-")
            data_updated = update_data_per_country(data_updated, PATH_REPUBLICA_DOMINICANA, day, "DO-")
            data_updated = update_data_per_country(data_updated, PATH_ARGENTINA, day, "AR-")
            data_updated = update_data_per_country(data_updated, PATH_COLOMBIA, day, "CO-")
            data_updated = update_data_per_country(data_updated, PATH_COSTA_RICA, day, "CR-")
            data_updated = update_data_per_country(data_updated, PATH_NICARAGUA, day, "NI-")
            data_updated = update_data_per_country(data_updated, PATH_URUGUAY, day, "UY-")
            data_updated = update_data_per_country(data_updated, PATH_FRANCIA, day, "FR-")

            data_updated = fix_format(data_updated)
            data_updated.to_csv(PATH_DSRP_DAILY_REPORTS + day + ".csv", index=False)
        except Exception as e:
            print(f"Error in {day} caughted, probably a new day without info.")

    time_series_generator.generate()  # Generate time series

    print("----------------------------------FIN--------------------------")
