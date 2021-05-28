import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

DATA_URL_CONFIRMED = 'https://raw.githubusercontent.com/danielcs88/colombia_covid-19/master/datos/cronologia.csv'
DATA_TEMPLATE_URL = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/templates/daily_report.csv'
PATH_CSV = "utils/scripts/data_collection/data/colombia_temporal/"
PATH_DSRP_DAILY_REPORTS = 'latam_covid_19_data/daily_reports/'
LAST_UPDATE = datetime.today().isoformat()
DICT_PLACES = {'Amazonas': 'CO-AMA',
               'Antioquia': 'CO-ANT',
               'Arauca': 'CO-ARA',
               'Atlántico': 'CO-ATL',
               'Bogotá D.C.': 'CO-DC',
               'Bolívar': 'CO-BOL',
               'Boyacá': 'CO-BOY',
               'Caldas': 'CO-CAL',
               'Caquetá': 'CO-CAQ',
               'Casanare': 'CO-CAS',
               'Cauca': 'CO-CAU',
               'Cesar': 'CO-CES',
               'Chocó': 'CO-COR',
               'Córdoba': 'CO-CUN',
               'Cundinamarca': 'CO-CHO',
               'Guainía': 'CO-GUA',
               'Guaviare': 'CO-GUV',
               'Huila': 'CO-HUI',
               'La Guajira': 'CO-LAG',
               'Magdalena': 'CO-MAG',
               'Meta': 'CO-MET',
               'Nariño': 'CO-NAR',
               'Norte de Santander': 'CO-NSA',
               'Putumayo': 'CO-PUT',
               'Quindío': 'CO-QUI',
               'Risaralda': 'CO-RIS',
               'San Andrés y Providencia': 'CO-SAP',
               'Santander': 'CO-SAN',
               'Sucre': 'CO-SUC',
               'Tolima': 'CO-TOL',
               'Valle del Cauca': 'CO-VAC',
               'Vaupés': 'CO-VAU',
               'Vichada': 'CO-VID',
               }


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

    df=pd.read_csv(DATA_URL_CONFIRMED)
    df['ISO 3166-2 Code']=df['departamento'].map(DICT_PLACES)


    df_template=pd.read_csv(DATA_TEMPLATE_URL)
    df_template=df_template.fillna('')
    # df_template['Confirmed']=df_template['Confirmed'].astype(int)
    # df_template['Deaths']=df_template['Deaths'].astype(int)
    # df_template['Recovered']=df_template['Recovered'].astype(int)
    # df_template['Last Update']=''
    df_template.loc[df_template['ISO 3166-2 Code'].str.contains('CO-'),'Last Update']=LAST_UPDATE
    df_template=df_template[df_template['ISO 3166-2 Code'].str.contains('CO-')]

    print('Starting iteration')
    for day in list_date_list:  # array_dates
        df_confirmed=df
        df_deaths=df
        try:
            for country_region in df_confirmed[df_confirmed['fecha']==day]['ISO 3166-2 Code'].unique():

                # Confirmed
                value_confirmed=df_confirmed.loc[(df_confirmed['ISO 3166-2 Code']==country_region) &
                                                (df_confirmed['fecha']==day)]['casos'].values[0]
                df_template.loc[df_template['ISO 3166-2 Code']==country_region,'Confirmed']=int(value_confirmed)
            
            df_filtered=df_template.loc[df_template['ISO 3166-2 Code'].str.contains('CO-')]
            df_filtered.to_csv(PATH_CSV+day+'.csv', index=False)

        except Exception as e:
            print(day,e)

    print('Ended iteration')


if __name__ == "__main__":
    print("======================COLOMBIA======================")
    load_and_generatecsv(['2021-05-13', '2021-05-10'])
