import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

DATA_URL = 'https://raw.githubusercontent.com/covid19cubadata/covid19cubadata.github.io/master/data/covid19-casos.csv'
DATA_TEMPLATE_URL = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/templates/daily_report.csv'
PATH_CSV = 'utils/scripts/data_collection/data/cuba_temporal/'
PATH_DSRP_DAILY_REPORTS = 'latam_covid_19_data/daily_reports/'
LAST_UPDATE = datetime.today().isoformat()
DICT_PLACES={'Artemisa': 'CU-15',
 'Camagüey': 'CU-09',
 'Ciego de Ávila': 'CU-08',
 'Cienfuegos': 'CU-06',
 'Granma': 'CU-12',
 'Guantánamo': 'CU-14',
 'Holguín': 'CU-11',
 'Isla de la Juventud': 'CU-99',
 'La Habana': 'CU-03',
 'Las Tunas': 'CU-10',
 'Matanzas': 'CU-04',
 'Mayabeque': 'CU-16',
 'Pinar del Río': 'CU-01',
 'Sancti Spíritus': 'CU-07',
 'Santiago de Cuba': 'CU-13',
 'Villa Clara': 'CU-05'}


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

    df = pd.read_csv(DATA_URL,low_memory=False,parse_dates=['fecha_confirmacion'])
    df = df[['sexo', 'provincia', 'fecha_confirmacion']]
    df=df.fillna(0)
    df=df.groupby(['provincia','fecha_confirmacion'],as_index=True).count()
    df.reset_index(inplace=True)
    df['provincia']=df['provincia'].astype('str')
    df['sexo']=df['sexo'].astype('str')
    df['ISO 3166-2 Code']=df['provincia'].map(DICT_PLACES)

    df_template = pd.read_csv(DATA_TEMPLATE_URL)
    df_template=df_template.fillna('')
    # df_template['Confirmed']=df_template['Confirmed'].astype(int)
    # df_template['Deaths']=df_template['Deaths'].astype(int)
    # df_template['Recovered']=df_template['Recovered'].astype(int)
    # df_template['Last Update']=''
    df_template.loc[df_template['ISO 3166-2 Code'].str.contains('CU-'),'Last Update']=LAST_UPDATE

    #array_dates_csv, array_dates = generate_list_dates(PATH_DSRP_DAILY_REPORTS)

    print('Starting iteration')
    for d in list_date_list:  # array_dates
        # print(d, end=' - ')
        try:
            df_filtered_by_day=df[df['fecha_confirmacion']==d]
            # Replace values
            for country_region in  df_filtered_by_day['ISO 3166-2 Code']:
                # Confirmed
                value_confirmed=df.loc[(df['ISO 3166-2 Code']==country_region) & (df['fecha_confirmacion']==d),'sexo']
                df_template.loc[df_template['ISO 3166-2 Code']==country_region,'Confirmed']=int(value_confirmed)

                df_filtered=df_template.loc[df_template['ISO 3166-2 Code'].str.contains('CU-')]
                df_filtered.to_csv(PATH_CSV+d+'.csv', index=False)


        except Exception as e:
            print(d,e)

    print('Ended iteration')

if __name__ == "__main__":
    print("======================CUBA======================")
    load_and_generatecsv(['2021-05-13','2021-05-10'])
