import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

DATA_URL_CONFIRMED = 'https://raw.githubusercontent.com/andrab/ecuacovid/master/datos_crudos/positivas/por_fecha/provincias_por_dia.csv'
DATA_URL_DEATHS = 'https://raw.githubusercontent.com/andrab/ecuacovid/master/datos_crudos/muertes/por_fecha/provincias_por_dia.csv'
DATA_TEMPLATE_URL = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/templates/daily_report.csv'
PATH_CSV = 'utils/scripts/data_collection/data/ecuador_temporal/'
PATH_DSRP_DAILY_REPORTS = 'latam_covid_19_data/daily_reports/'
LAST_UPDATE = datetime.today().isoformat()
DICT_PLACES = {'Azuay': 'EC-A',
               'Bolívar': 'EC-B',
               'Carchi': 'EC-F',
               'Cañar': 'EC-C',
               'Chimborazo': 'EC-H',
               'Cotopaxi': 'EC-X',
               'El Oro': 'EC-O',
               'Esmeraldas': 'EC-E',
               'Galápagos': 'EC-W',
               'Guayas': 'EC-G',
               'Imbabura': 'EC-I',
               'Loja': 'EC-L',
               'Los Ríos': 'EC-R',
               'Manabí': 'EC-M',
               'Morona Santiago': 'EC-S',
               'Napo': 'EC-N',
               'Orellana': 'EC-D',
               'Pastaza': 'EC-Y',
               'Pichincha': 'EC-P',
               'Santa Elena': 'EC-SE',
               'Sto. Domingo Tsáchilas': 'EC-SD',
               'Sucumbíos': 'EC-U',
               'Tungurahua': 'EC-T',
               'Zamora Chinchipe': 'EC-Z'}


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


def load_and_generatecsv(list_date_list):

    df_confirmed=pd.read_csv(DATA_URL_CONFIRMED)
    df_confirmed['ISO 3166-2 Code']=df_confirmed['provincia'].map(DICT_PLACES)
    
    df_deaths=pd.read_csv(DATA_URL_DEATHS)
    df_deaths['ISO 3166-2 Code']=df_deaths['provincia'].map(DICT_PLACES)
    
    df_template=pd.read_csv(DATA_TEMPLATE_URL)
    df_template=df_template.fillna('')
    # df_template['Confirmed']=df_template['Confirmed'].astype(int)
    # df_template['Deaths']=df_template['Deaths'].astype(int)
    # df_template['Recovered']=df_template['Recovered'].astype(int)
    # df_template['Last Update']=''
    df_template.loc[df_template['ISO 3166-2 Code'].str.contains('EC-'),'Last Update']=LAST_UPDATE

    for d in list_date_list:  # array_dates

        try:
            d_fix = datetime.strptime(d, '%Y-%m-%d')
            d_fix = d_fix.strftime('%d/%m/%Y')
            df_confirmed=df_confirmed[['ISO 3166-2 Code',d_fix]]

            d_fix = datetime.strptime(d, '%Y-%m-%d')
            d_fix = d_fix.strftime('%d/%m/%Y')
            df_deaths=df_deaths[['ISO 3166-2 Code',d_fix]]            

            for country_region in df_confirmed['ISO 3166-2 Code']:
                value_confirmed=df_confirmed.loc[df_confirmed['ISO 3166-2 Code']==country_region,d_fix]
                df_template.loc[df_template['ISO 3166-2 Code']==country_region,'Confirmed']=int(value_confirmed)

                value_deaths=df_deaths.loc[df_deaths['ISO 3166-2 Code']==country_region,d_fix]
                df_template.loc[df_template['ISO 3166-2 Code']==country_region,'Deaths']=int(value_deaths)

            
            df_filtered=df_template.loc[df_template['ISO 3166-2 Code'].str.contains('EC-')]
            df_filtered.to_csv(PATH_CSV+d+'.csv', index=False)

        except Exception as e:
            print(d,e)



if __name__ == "__main__":
    print("======================ECUADOR======================")
    load_and_generatecsv(['2021-05-13'])
