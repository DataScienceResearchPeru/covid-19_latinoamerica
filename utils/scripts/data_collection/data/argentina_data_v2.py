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
        print('[ARGENTINA] FILE NOT FOUND, DOWNLOADING...')
        r = requests.get(url, headers=headers)
        
        with open(PATH_FILE,'wb') as f:
            f.write(r.content)
        print(f'[ARGENTINA] FILE SAVE TO {PATH_FILE}')
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
        for country_code in df_confirmed['ISO 3166-2 Code'].unique():

            # CONFIRMED CASES
            try:
                value_per_contry=df_confirmed[(df_confirmed['fecha_diagnostico']==day)&
                                            (df_confirmed['ISO 3166-2 Code']==country_code)]['ultima_actualizacion'].values[0]
            except IndexError:
                value_per_contry=0
            except Exception as e:
                print(day,e)
            finally:
                df_template.loc[df_template['ISO 3166-2 Code']==country_code,'Confirmed']=int(value_per_contry)

            # DEATHS CASES
            try:
                value_per_contry=df_deaths[(df_deaths['fecha_diagnostico']==day)&
                                            (df_deaths['ISO 3166-2 Code']==country_code)]['ultima_actualizacion'].values[0]
            except IndexError:
                value_per_contry=0
            except Exception as e:
                print(day,e)
            finally:
                df_template.loc[df_template['ISO 3166-2 Code']==country_code,'Deaths']=int(value_per_contry)

        df_filtered=df_template.loc[df_template['ISO 3166-2 Code'].str.contains('AR-')]
        df_filtered.to_csv(PATH_CSV+day+'.csv', index=False)


    print('Ended iteration')

if __name__ == "__main__":
    print("======================ARGENTINA======================")
    load_and_generatecsv(['2021-05-28', '2021-05-27'])
