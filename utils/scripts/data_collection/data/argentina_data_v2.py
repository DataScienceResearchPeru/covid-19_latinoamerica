import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

DATA_URL = 'https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.zip'
DATA_TEMPLATE_URL = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/templates/daily_report.csv'
PATH_CSV = "utils/scripts/data_collection/data/argentina_temporal/"
PATH_DSRP_DAILY_REPORTS = 'latam_covid_19_data/daily_reports/'
LAST_UPDATE = datetime.today().isoformat()
DICT_PLACES = {'Buenos Aires':'AR-B',
               'CABA':'AR-C',
               'Catamarca':'AR-K',
               'Chaco':'AR-H',
               'Chubut':'AR-U',
               'Corrientes':'AR-W',
               'Córdoba':'AR-X',
               'Entre Ríos':'AR-E',
               'Formosa':'AR-P',
               'Indeterminado':'',
               'Jujuy':'AR-Y',
               'La Pampa':'AR-L',
               'La Rioja': 'AR-F',
               'Mendoza':'AR-M',
               'Misiones': 'AR-N',
               'Neuquén':'AR-Q',
               'Río Negro':'AR-R',
               'Salta':'AR-A',
               'San Juan':'AR-J',
               'San Luis':'AR-D',
               'Santa Cruz':'AR-Z',
               'Santa Fe':'AR-S',
               'Santiago del Estero':'AR-G',
               'Tierra del Fuego':'AR-V',
               'Tucumán':'AR-T'
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

    import requests
    url = DATA_URL
    headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}

    PATH_FILE=PATH_CSV+"data.zip"
    if not os.path.isfile(PATH_FILE):
        r = requests.get(url, headers=headers)
        
        with open(PATH_FILE,'wb') as f:
            f.write(r.content)
    else:
        print('[ARGENTINA] FILE ZIP ALREADY EXISTS, USING THAT FILE')

    df = pd.read_csv(PATH_FILE, 
                    usecols=['residencia_provincia_nombre','fecha_diagnostico','ultima_actualizacion','clasificacion_resumen','fallecido'],
                    compression="zip")

    df_confirmed=df[df['clasificacion_resumen']=='Confirmado'].groupby(['residencia_provincia_nombre','fecha_diagnostico']).count() \
                    .groupby(level=0).cumsum().reset_index()

    df_confirmed['ISO 3166-2 Code']=df_confirmed['residencia_provincia_nombre'].map(DICT_PLACES)
    df_confirmed=df_confirmed[['ISO 3166-2 Code','fecha_diagnostico','ultima_actualizacion']]
    df_confirmed=df_confirmed.dropna()
    # df_confirmed[df_confirmed['fecha_diagnostico']=='2021-05-22']


    df_deaths=df[df['fallecido']=='SI'].groupby(['residencia_provincia_nombre','fecha_diagnostico']).count() \
                .groupby(level=0).cumsum().reset_index()

    df_deaths['ISO 3166-2 Code']=df_deaths['residencia_provincia_nombre'].map(DICT_PLACES)
    df_deaths=df_deaths[['ISO 3166-2 Code','fecha_diagnostico','ultima_actualizacion']]
    df_deaths=df_deaths.dropna()
    # df_deaths[df_deaths['fecha_diagnostico']=='2021-05-22']

    df_template = pd.read_csv(DATA_TEMPLATE_URL)
    df_template=df_template.fillna('')
    # df_template['Confirmed']=df_template['Confirmed'].astype(int)
    # df_template['Deaths']=df_template['Deaths'].astype(int)
    # df_template['Recovered']=df_template['Recovered'].astype(int)
    # df_template['Last Update']=''
    df_template.loc[df_template['ISO 3166-2 Code'].str.contains('AR-'),'Last Update']=LAST_UPDATE

    #array_dates_csv, array_dates = generate_list_dates(PATH_DSRP_DAILY_REPORTS)

    print('Starting iteration')
    for day in list_date_list:  # array_dates
        # print(d, end=' - ')
        try:
            for country_code in df_confirmed['ISO 3166-2 Code'].unique():

                value_per_contry=df_confirmed[(df_confirmed['fecha_diagnostico']==day)&
                                            (df_confirmed['ISO 3166-2 Code']==country_code)]['ultima_actualizacion'].values[0]
                df_template.loc[df_template['ISO 3166-2 Code']==country_code,'Confirmed']=int(value_per_contry)

                value_per_contry=df_deaths[(df_deaths['fecha_diagnostico']==day)&
                                            (df_deaths['ISO 3166-2 Code']==country_code)]['ultima_actualizacion'].values[0]
                df_template.loc[df_template['ISO 3166-2 Code']==country_code,'Deaths']=int(value_per_contry)

                df_filtered=df_template.loc[df_template['ISO 3166-2 Code'].str.contains('AR-')]
                df_filtered.to_csv(PATH_CSV+day+'.csv', index=False)
        except Exception as e:
            print(day,e)


    print('Ended iteration')

if __name__ == "__main__":
    print("======================ARGENTINA======================")
    # load_and_generatecsv(['2021-05-04', '2021-05-03'])
    load_and_generatecsv(['2021-05-24', '2021-05-23', '2021-05-22', '2021-05-21', '2021-05-20', '2021-05-19', '2021-05-18', '2021-05-17', '2021-05-16', '2021-05-15', '2021-05-14', '2021-05-13', '2021-05-12', '2021-05-11', '2021-05-10', '2021-05-09', '2021-05-08', '2021-05-07', '2021-05-06', '2021-05-05', '2021-05-04', '2021-05-03', '2021-05-02', '2021-05-01', '2021-04-30', '2021-04-29', '2021-04-28', '2021-04-27', '2021-04-26', '2021-04-25', '2021-04-24', '2021-04-23', '2021-04-22', '2021-04-21', '2021-04-20', '2021-04-19', '2021-04-18', '2021-04-17', '2021-04-16', '2021-04-15', '2021-04-14', '2021-04-13', '2021-04-12', '2021-04-11', '2021-04-10', '2021-04-09', '2021-04-08', '2021-04-07', '2021-04-06', '2021-04-05', '2021-04-04', '2021-04-03', '2021-04-02', '2021-04-01', '2021-03-31', '2021-03-30', '2021-03-29', '2021-03-28', '2021-03-27', '2021-03-26', '2021-03-25', '2021-03-24', '2021-03-23', '2021-03-22', '2021-03-21', '2021-03-20', '2021-03-19', '2021-03-18', '2021-03-17', '2021-03-16', '2021-03-15', '2021-03-14', '2021-03-13', '2021-03-12', '2021-03-11', '2021-03-10', '2021-03-09', '2021-03-08', '2021-03-07', '2021-03-06', '2021-03-05', '2021-03-04', '2021-03-03', '2021-03-02', '2021-03-01', '2021-02-28', '2021-02-27', '2021-02-26', '2021-02-25', '2021-02-24', '2021-02-23', '2021-02-22', '2021-02-21', '2021-02-20', '2021-02-19', '2021-02-18', '2021-02-17', '2021-02-16', '2021-02-15', '2021-02-14', '2021-02-13', '2021-02-12', '2021-02-11', '2021-02-10', '2021-02-09', '2021-02-08', '2021-02-07', '2021-02-06', '2021-02-05', '2021-02-04', '2021-02-03', '2021-02-02', '2021-02-01', '2021-01-31', '2021-01-30', '2021-01-29', '2021-01-28', '2021-01-27', '2021-01-26', '2021-01-25', '2021-01-24', '2021-01-23', '2021-01-22', '2021-01-21', '2021-01-20', '2021-01-19', '2021-01-18', '2021-01-17', '2021-01-16', '2021-01-15', '2021-01-14', '2021-01-13', '2021-01-12', '2021-01-11', '2021-01-10', '2021-01-09', '2021-01-08', '2021-01-07', '2021-01-06', '2021-01-05', '2021-01-04', '2021-01-03', '2021-01-02', '2021-01-01', '2020-12-31', '2020-12-30', '2020-12-29', '2020-12-28', '2020-12-27', '2020-12-26', '2020-12-25', '2020-12-24', '2020-12-23', '2020-12-22', '2020-12-21', '2020-12-20', '2020-12-19', '2020-12-18', '2020-12-17', '2020-12-16', '2020-12-15', '2020-12-14', '2020-12-13', '2020-12-12', '2020-12-11', '2020-12-10', '2020-12-09', '2020-12-08', '2020-12-07', '2020-12-06', '2020-12-05', '2020-12-04', '2020-12-03', '2020-12-02', '2020-12-01', '2020-11-30', '2020-11-29', '2020-11-28', '2020-11-27', '2020-11-26', '2020-11-25', '2020-11-24', '2020-11-23', '2020-11-22', '2020-11-21', '2020-11-20', '2020-11-19', '2020-11-18', '2020-11-17', '2020-11-16', '2020-11-15', '2020-11-14', '2020-11-13', '2020-11-12', '2020-11-11', '2020-11-10', '2020-11-09', '2020-11-08', '2020-11-07', '2020-11-06', '2020-11-05', '2020-11-04', '2020-11-03', '2020-11-02', '2020-11-01', '2020-10-31', '2020-10-30', '2020-10-29', '2020-10-28', '2020-10-27', '2020-10-26', '2020-10-25', '2020-10-24', '2020-10-23', '2020-10-22', '2020-10-21', '2020-10-20', '2020-10-19', '2020-10-18', '2020-10-17', '2020-10-16', '2020-10-15', '2020-10-14', '2020-10-13', '2020-10-12', '2020-10-11', '2020-10-10', '2020-10-09', '2020-10-08', '2020-10-07', '2020-10-06', '2020-10-05', '2020-10-04', '2020-10-03', '2020-10-02', '2020-10-01', '2020-09-30', '2020-09-29', '2020-09-28', '2020-09-27', '2020-09-26', '2020-09-25', '2020-09-24', '2020-09-23', '2020-09-22', '2020-09-21', '2020-09-20', '2020-09-19', '2020-09-18', '2020-09-17', '2020-09-16', '2020-09-15', '2020-09-14', '2020-09-13', '2020-09-12', '2020-09-11', '2020-09-10', '2020-09-09', '2020-09-08', '2020-09-07', '2020-09-06', '2020-09-05', '2020-09-04', '2020-09-03', '2020-09-02', '2020-09-01', '2020-08-31', '2020-08-30', '2020-08-29', '2020-08-28', '2020-08-27', '2020-08-26', '2020-08-25', '2020-08-24', '2020-08-23', '2020-08-22', '2020-08-21', '2020-08-20', '2020-08-19', '2020-08-18', '2020-08-17', '2020-08-16', '2020-08-15', '2020-08-14', '2020-08-13', '2020-08-12', '2020-08-11', '2020-08-10', '2020-08-09', '2020-08-08', '2020-08-07', '2020-08-06', '2020-08-05', '2020-08-04', '2020-08-03', '2020-08-02', '2020-08-01', '2020-07-31', '2020-07-30', '2020-07-29', '2020-07-28', '2020-07-27', '2020-07-26', '2020-07-25', '2020-07-24', '2020-07-23', '2020-07-22', '2020-07-21', '2020-07-20', '2020-07-19', '2020-07-18', '2020-07-17', '2020-07-16', '2020-07-15', '2020-07-14', '2020-07-13', '2020-07-12', '2020-07-11', '2020-07-10', '2020-07-09', '2020-07-08', '2020-07-07', '2020-07-06', '2020-07-05', '2020-07-04', '2020-07-03', '2020-07-02', '2020-07-01', '2020-06-30', '2020-06-29', '2020-06-28', '2020-06-27', '2020-06-26', '2020-06-25', '2020-06-24', '2020-06-23', '2020-06-22', '2020-06-21', '2020-06-20', '2020-06-19', '2020-06-18', '2020-06-17', '2020-06-16', '2020-06-15', '2020-06-14', '2020-06-13', '2020-06-12', '2020-06-11', '2020-06-10', '2020-06-09', '2020-06-08', '2020-06-07', '2020-06-06', '2020-06-05', '2020-06-04', '2020-06-03', '2020-06-02', '2020-06-01', '2020-05-31', '2020-05-30', '2020-05-29', '2020-05-28', '2020-05-27', '2020-05-26', '2020-05-25', '2020-05-24', '2020-05-23', '2020-05-22', '2020-05-21', '2020-05-20', '2020-05-19', '2020-05-18', '2020-05-17', '2020-05-16', '2020-05-15', '2020-05-14', '2020-05-13', '2020-05-12', '2020-05-11', '2020-05-10', '2020-05-09', '2020-05-08', '2020-05-07', '2020-05-06', '2020-05-05', '2020-05-04', '2020-05-03', '2020-05-02', '2020-05-01', '2020-04-30', '2020-04-29', '2020-04-28', '2020-04-27', '2020-04-26', '2020-04-25', '2020-04-24', '2020-04-23', '2020-04-22', '2020-04-21', '2020-04-20', '2020-04-19', '2020-04-18', '2020-04-17', '2020-04-16', '2020-04-15', '2020-04-14', '2020-04-13', '2020-04-12', '2020-04-11', '2020-04-10', '2020-04-09', '2020-04-08', '2020-04-07', '2020-04-06', '2020-04-05', '2020-04-04', '2020-04-03', '2020-04-02', '2020-04-01', '2020-03-31', '2020-03-30', '2020-03-29', '2020-03-28', '2020-03-27', '2020-03-26', '2020-03-25', '2020-03-24', '2020-03-23', '2020-03-22', '2020-03-21', '2020-03-20', '2020-03-19', '2020-03-18', '2020-03-17', '2020-03-16', '2020-03-15', '2020-03-14', '2020-03-13', '2020-03-12', '2020-03-11', '2020-03-10', '2020-03-09', '2020-03-08', '2020-03-07', '2020-03-06', '2020-03-05', '2020-03-04', '2020-03-03', '2020-03-02', '2020-03-01', '2020-02-29', '2020-02-28', '2020-02-27', '2020-02-26'])
