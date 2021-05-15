import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

try:    
    import utils.scripts.data_collection.data.peru_data_v2 as peru_data
    import utils.scripts.data_collection.data.ecuador_data_v2 as ecuador_data
    import utils.scripts.data_collection.data.cuba_data_v2 as cuba_data
    import utils.scripts.data_time_series.time_series_generator as time_series_generator
except Exception as e:
    print('Exception fixed: ',e)
    import data_collection.data.peru_data_v2 as peru_data
    import data_collection.data.ecuador_data_v2 as ecuador_data
    import data_collection.data.cuba_data_v2 as cuba_data
    import data_time_series.time_series_generator as time_series_generator


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


def execute_country(df,PATH_COUNTRY, d, isocode):
    try:
        path_day_per_country=PATH_COUNTRY+d+'.csv'
        data_country=pd.read_csv(path_day_per_country)
        data_country=data_country[data_country['ISO 3166-2 Code'].str.contains(isocode)]

        df=df.combine_first(data_country)

    except Exception as e:
        print('Exception fixed: ',e)
        
    return df


def load_all_data_temporal(list_date_list):

    cuba_data.load_and_generatecsv(list_date_list)
    peru_data.load_and_generatecsv(list_date_list)
    ecuador_data.load_and_generatecsv(list_date_list)

    print("------------------------ALL TEMPORALS CREATED----------------------------")


if __name__ == "__main__":

    logo()


    df_template=pd.read_csv(DATA_TEMPLATE_URL)
    df_template=df_template.fillna(0)
    df_template['Confirmed']=df_template['Confirmed'].astype(int)
    df_template['Deaths']=df_template['Deaths'].astype(int)
    df_template['Recovered']=df_template['Recovered'].astype(int)
    df_template['Last Update']=''

    date_list_csv, date_list = generate_list_dates(PATH_DSRP_DAILY_REPORTS)

    for d in date_list[0:10]:  # date_list
        try:
            daily_path='latam_covid_19_data/daily_reports/'+d+'.csv'
            if not os.path.isfile(daily_path):
                # Create day if not exists
                df_base = pd.read_csv(DATA_TEMPLATE_URL)  # Template
                df_base['Confirmed'] =''
                df_base['Deaths'] =''
                df_base['Recovered'] = ''
                df_base['Last Update']=''
                df_base.to_csv(daily_path, index=False)
                print(f'Creating not found {daily_path}')
        except Exception as e:
            print(e)

    list_date_list = date_list[1:2]
    load_all_data_temporal(date_list)
    print('List of dates to be modified:')

    for d in list_date_list:  # date_list
        # df_template=execute_country(df_template,PATH_CUBA, d, 'CU-')
        df_template=execute_country(df_template,PATH_ECUADOR, d, 'EC-')
        df_template=execute_country(df_template,PATH_PERU, d, 'PE-')

        df_template.to_csv(PATH_DSRP_DAILY_REPORTS+d+'.csv', index=False)

    time_series_generator.generate()  # Generate time series

    print("----------------------------------FIN--------------------------")
