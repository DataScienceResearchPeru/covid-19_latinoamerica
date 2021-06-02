import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

DATA_URL = 'https://catalogodatos.gub.uy/dataset/560823fe-5ed7-47d2-9b3f-48a6768c6ebf/resource/22626680-4ff1-49e7-a8ad-e580636618b2/download/estadisticas-covid-19.xlsx'
DATA_TEMPLATE_URL = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/templates/daily_report.csv'
PATH_CSV = "utils/scripts/data_collection/data/uruguay_temporal/"
PATH_DSRP_DAILY_REPORTS = 'latam_covid_19_data/daily_reports/'
LAST_UPDATE = datetime.today().isoformat()
DICT_PLACES = {'Artigas':'UY-AR',
                'Canelones':'UY-CA',
                'Cerro Largo ':'UY-CL',
                'Cerro Largo\xa0':'UY-CL',
                'Colonia':'UY-CO', 
                'Durazno':'UY-DU',
                'Flores':'UY-FS', 
                'Florida':'UY-FD', 
                'Lavalleja':'UY-LA',
                'Maldonado':'UY-MA',
                'Montevideo':'UY-MO',
                'Paysandú':'UY-PA',
                'Río Negro':'UY-RN',
                'Rivera':'UY-RV',
                'Rocha':'UY-RO', 
                'Salto':'UY-SA', 
                'San José':'UY-SJ',
                'Soriano':'UY-SO', 
                'Tacuarembó':'UY-TA',
                'Treinta y Tres':'UY-TT',
                'Todo el país':np.nan,}

DICT_INDICATORS = { 'Casos activos':'Casos activos', 
                    'Casos recuperados':'Casos recuperados',
                    'Fallecidos':'Fallecidos',
                    'Fallecidos ':'Fallecidos',
                    'Casos nuevos ':'Casos nuevos', 
                    'Fallecidos\xa0':'Fallecidos',
                    'Casos nuevos\xa0':'Casos nuevos',
                    'Personas en CTI':np.nan,
                    'Personas en CI':np.nan,
                    'Personal de la salud  Confirmados ':np.nan,
                    'Personal de la salud  Recuperados ':np.nan,
                    'Personal de la salud  Activos ':np.nan,
                    'Personal de la salud  Fallecidos ':np.nan,
                    'Cantidad de Tests  Positivos ':np.nan,
                    'Cantidad de Tests  Negativos ':np.nan,
                    'Personal de la salud\xa0 Confirmados\xa0':np.nan,
                    'Personal de la salud\xa0 Recuperados\xa0':np.nan,
                    'Personal de la salud\xa0 Activos\xa0':np.nan,
                    'Personal de la salud\xa0 Fallecidos\xa0':np.nan,
                    'Cantidad de Tests\xa0 Positivos\xa0':np.nan,
                    'Cantidad de Tests\xa0 Negativos\xa0':np.nan,
                    'Cantidad de Tests\xa0 Total\xa0':np.nan,
                    'Personas en Cuidados criticos':np.nan,
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

    xls = pd.ExcelFile(DATA_URL)
    df=pd.read_excel(xls,'Datos')
    df=df[['Fecha','Indicador','Territorio','Valor']]
    df['ISO 3166-2 Code']=df['Territorio'].map(DICT_PLACES)
    df['Indicador_fixed']=df['Indicador'].map(DICT_INDICATORS)
    df=df.dropna()

    df_template = pd.read_csv(DATA_TEMPLATE_URL)
    df_template=df_template.fillna('')
    # df_template['Confirmed']=df_template['Confirmed'].astype(int)
    # df_template['Deaths']=df_template['Deaths'].astype(int)
    # df_template['Recovered']=df_template['Recovered'].astype(int)
    # df_template['Last Update']=''
    df_template.loc[df_template['ISO 3166-2 Code'].str.contains('UY-'),'Last Update']=LAST_UPDATE

    df_confirmed=df[df['Indicador_fixed']=='Casos activos']
    df_confirmed=df_confirmed.groupby(['Fecha','ISO 3166-2 Code']).sum() \
                .groupby(level=0).cumsum().reset_index()

    df_deaths=df[df['Indicador_fixed']=='Fallecidos']
    df_deaths=df_deaths.groupby(['Fecha','ISO 3166-2 Code']).sum() \
                .groupby(level=0).cumsum().reset_index()

    df_recovered=df[df['Indicador_fixed']=='Casos recuperados']
    df_recovered=df_recovered.groupby(['Fecha','ISO 3166-2 Code']).sum() \
                .groupby(level=0).cumsum().reset_index()


    print('Starting iteration')
    for day in list_date_list:
        for country_region in df['ISO 3166-2 Code'].unique():
            # Confirmed
            try:
                criteria=((df_confirmed['Fecha']==day)&
                            (df_confirmed['ISO 3166-2 Code']==country_region))
                value_confirmed_per_country=df_confirmed.loc[criteria,'Valor'].values[0]
                df_template.loc[df_template['ISO 3166-2 Code'] ==country_region, 'Confirmed'] = int(value_confirmed_per_country)
            except Exception as e:
                print(day, e)

            # Deaths
            try:
                criteria=((df_deaths['Fecha']==day)&
                            (df_deaths['ISO 3166-2 Code']==country_region))
                value_confirmed_per_country=df_deaths.loc[criteria,'Valor'].values[0]
                df_template.loc[df_template['ISO 3166-2 Code'] ==country_region, 'Deaths'] = int(value_confirmed_per_country)
            except Exception as e:
                print(day, e)
            
            # Recovered
            try:
                criteria=((df_recovered['Fecha']==day)&
                            (df_recovered['ISO 3166-2 Code']==country_region))
                value_confirmed_per_country=df_recovered.loc[criteria,'Valor'].values[0]
                df_template.loc[df_template['ISO 3166-2 Code'] ==country_region, 'Recovered'] = int(value_confirmed_per_country)
            except Exception as e:
                print(day, e)

            df_filtered = df_template.loc[df_template['ISO 3166-2 Code'].str.contains(
                'UY-')]
            df_filtered.to_csv(PATH_CSV+day+'.csv', index=False)

    print('Ended iteration')


if __name__ == "__main__":
    print("======================URUGUAY======================")
    load_and_generatecsv(['2021-05-13', '2021-05-10'])
