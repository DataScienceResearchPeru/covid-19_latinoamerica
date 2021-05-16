import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests

import utils.scripts.data_collection.data.peru_data_v2 as peru_data
import utils.scripts.data_collection.data.ecuador_data_v2 as ecuador_data
import utils.scripts.data_collection.data.cuba_data_v2 as cuba_data
import utils.scripts.data_time_series.time_series_generator as time_series_generator


PATH_DSRP_DAILY_REPORTS = 'latam_covid_19_data/daily_reports/'
DATA_TEMPLATE_URL = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/templates/daily_report.csv'
PATH_CUBA = 'utils/scripts/data_collection/data/cuba_temporal/'
PATH_ECUADOR = 'utils/scripts/data_collection/data/ecuador_temporal/'
PATH_PERU = 'utils/scripts/data_collection/data/peru_temporal/'


def logo():
    print("""                                                                                       
    ,ad8888ba,    ,ad8888ba,   8b           d8  88  88888888ba,              88   ad88888ba   
    d8"'    `"8b  d8"'    `"8b  `8b         d8'  88  88      `"8b           ,d88  d8"     "88  
   d8'           d8'        `8b  `8b       d8'   88  88        `8b        888888  8P       88  
   88            88          88   `8b     d8'    88  88         88            88  Y8,    ,d88  
   88            88          88    `8b   d8'     88  88         88  aaaaaaaa  88   "PPPPPP"88  
   Y8,           Y8,        ,8P     `8b d8'      88  88         8P  """"""""  88           8P  
    Y8a.    .a8P  Y8a.    .a8P       `888'       88  88      .a8P             88  8b,    a8P   
    `"Y8888Y"'    `"Y8888Y"'         `8'        88  88888888Y"'              88  `"Y8888P'    
                                                                                                
                                                                                                
                                                                                                
    88888888ba                        88888888ba,     ad88888ba   88888888ba   88888888ba       
    88      "8b                       88      `"8b   d8"     "8b  88      "8b  88      "8b      
    88      ,8P                       88        `8b  Y8,          88      ,8P  88      ,8P      
    88aaaaaa8P'  8b       d8  888     88         88  `Y8aaaaa,    88aaaaaa8P'  88aaaaaa8P'      
    88""""""8b,  `8b     d8'  888     88         88    `'''''8b,  88''''88'    88""""""'        
    88      `8b   `8b   d8'           88         8P          `8b  88    `8b    88               
    88      a8P    `8b,d8'    888     88      .a8P   Y8a     a8P  88     `8b   88               
    88888888P"       Y88'     888     88888888Y"'     "Y88888P"   88      `8b  88               
                    d8'                                                                        
                    d8'                                                                         
    """)


def generate_list_dates(path):
    # Generate dates from files existing
    date_list_csv = []
    path, dirs, files = next(os.walk(path))
    numero_archivos = len(files)
    print('There is {} files on the path and one is README. We iterate {} times...'.format(
        numero_archivos, numero_archivos-1))
    # dates
    base = (datetime.today()).date()
    numdays = numero_archivos-1
    date_list_csv = [str(base - timedelta(days=x))+str('.csv')
                     for x in range(numdays)]
    print('Adding {} dates in a list...'.format(len(date_list_csv)))
    date_list = []
    for d in date_list_csv:
        date_list.append(d[:-4])
    print("List of dates:", date_list)
    return date_list_csv, date_list


def fix_format(df):
    df = df.fillna('')

    for m in range(len(df)):

        if df.loc[m]['Confirmed'] != '':
            a = int(float(df.loc[m]['Confirmed']))
        else:
            a = ''

        if df.loc[m]['Deaths'] != '':
            b = int(float(df.loc[m]['Deaths']))
        else:
            b = ''

        if df.loc[m]['Recovered'] != '':
            c = int(float(df.loc[m]['Recovered']))
        else:
            c = ''

        df.loc[m, ['Confirmed']] = str(a)
        df.loc[m, ['Deaths']] = str(b)
        df.loc[m, ['Recovered']] = str(c)

    return df


def load_all_data_temporal(list_date_list):

    cuba_data.load_and_generatecsv(list_date_list)
    peru_data.load_and_generatecsv(list_date_list)
    ecuador_data.load_and_generatecsv(list_date_list)

    print("------------------------ALL TEMPORALS CREATED----------------------------")


def update_data_per_country(df_template,path, d, isocode):

    try:
        df_template=df_template.set_index('ISO 3166-2 Code')
        MY_PATH=f'{path+d}.csv'
        df=pd.read_csv(MY_PATH)
        df=df.set_index('ISO 3166-2 Code')

        df_template.update(df)

    except Exception as e:
        print(f'Exception caughted in {isocode} -> {path+d}.csv')
    
    finally:        
        
        df_template=df_template.reset_index(drop=False)
        return df_template


if __name__ == "__main__":

    logo()

    df_template=pd.read_csv(DATA_TEMPLATE_URL)
    df_template=df_template.fillna('')
    
    date_list_csv, date_list = generate_list_dates(PATH_DSRP_DAILY_REPORTS)

    load_all_data_temporal(date_list[0:10])

    # Days to check if file exists
    for d in date_list[0:3]:  # date_list
        URL = f"https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/daily_reports/{d}.csv"

        # Check if file exists, if not -> create based on template
        try:
            response = requests.head(URL)
        except Exception as e:
            print(f"NOT OK: {str(e)}")
        else:
            if response.status_code == 200:
                print(f"OK daily/{d}.csv exists, using that file as DataFrame.")
            else:
                print(f"NOT OK: HTTP response code {response.status_code}")
                print(f'Creating file {d}.csv')
                df_template.to_csv(PATH_DSRP_DAILY_REPORTS+d+'.csv',index=False)

        try:
            # Use template
            df_template=pd.read_csv(URL)
            # Update data
            data_updated=update_data_per_country(df_template,PATH_ECUADOR, d, 'EC-')
            data_updated=update_data_per_country(data_updated,PATH_PERU, d, 'PE-')
            data_updated=update_data_per_country(data_updated,PATH_CUBA,d,'CU-')

            data_updated=fix_format(data_updated)
            data_updated.to_csv(PATH_DSRP_DAILY_REPORTS+d+'.csv', index=False)
        except Exception as e:
            print(f'Error in {d} caughted, probably a new day without info.')
    
    #time_series_generator.generate()  # Generate time series

    print("----------------------------------FIN--------------------------")
