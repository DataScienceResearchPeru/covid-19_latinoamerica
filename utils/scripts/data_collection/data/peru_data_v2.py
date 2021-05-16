import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

DATA_URL = 'https://raw.githubusercontent.com/jmcastagnetto/covid-19-peru-data/main/datos/covid-19-peru-data.csv'
DATA_TEMPLATE_URL = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/templates/daily_report.csv'
PATH_CSV = 'utils/scripts/data_collection/data/peru_temporal/'
PATH_DSRP_DAILY_REPORTS = 'latam_covid_19_data/daily_reports/'
LAST_UPDATE = datetime.today().isoformat()
DICT_PLACES = {'Amazonas': 'PE-AMA',
               'Ancash': 'PE-ANC',
               'Apurimac': 'PE-APU',
               'Arequipa': 'PE-ARE',
               'Ayacucho':  'PE-AYA',
               'Cajamarca': 'PE-CAJ',
               'Callao': 'PE-CAL',
               'Cusco':  'PE-CUS',
               'Huancavelica':  'PE-HUV',
               'Huánuco':   'PE-HUC',
               'Ica': 'PE-ICA',
               'Junín': 'PE-JUN',
               'La Libertad':  'PE-LAL',
               'Lambayeque': 'PE-LAM',
               'Lima Metropolitana': 'PE-LIM',
               'Lima Región': 'PE-LIM',
               'Lima': 'PE-LIM',
               'Loreto': 'PE-LOR',
               'Madre de Dios': 'PE-MDD',
               'Moquegua': 'PE-MOQ',
               'Pasco': 'PE-PAS',
               'Piura': 'PE-PIU',
               'Puno':    'PE-PUN',
               'San Martín': 'PE-SAM',
               'Tacna': 'PE-TAC',
               'Tumbes': 'PE-TUM',
               'Ucayali':  'PE-UCA'}


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

    df = pd.read_csv(DATA_URL)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%dT%H:%M%:%SZ')

    df_template = pd.read_csv(DATA_TEMPLATE_URL)
    df_template=df_template.fillna('')
    # df_template['Confirmed']=df_template['Confirmed'].astype(int)
    # df_template['Deaths']=df_template['Deaths'].astype(int)
    # df_template['Recovered']=df_template['Recovered'].astype(int)
    # df_template['Last Update']=''
    df_template.loc[df_template['ISO 3166-2 Code'].str.contains('PE-'),'Last Update']=LAST_UPDATE

    #array_dates_csv, array_dates = generate_list_dates(PATH_DSRP_DAILY_REPORTS)


    print('Starting iteration')
    for d in list_date_list:  # array_dates
        print(d, end=' - ')
        try:
            df_filtered_by_day = df[df['date'].str.contains(d)]
            df_filtered_by_day = df_filtered_by_day.fillna(0)
            df_filtered_by_day['confirmed'] = df_filtered_by_day['confirmed'].astype(
                int)
            df_filtered_by_day['deaths'] = df_filtered_by_day['deaths'].astype(int)
            df_filtered_by_day['recovered'] = df_filtered_by_day['recovered'].astype(
                int)
            df_filtered_by_day = df_filtered_by_day[[
                'region', 'date', 'confirmed', 'deaths', 'recovered']]
            # df map LIMA
            df_filtered_by_day['ISO 3166-2 Code'] = df_filtered_by_day['region'].map(
                DICT_PLACES)
            # sum 'PE-LIM' exceptions
            df_filtered_by_day = df_filtered_by_day.groupby(
                'ISO 3166-2 Code').sum()

            # df_template=df_template[df_template['ISO 3166-2 Code'].str.contains('PE-')==True]

            # Replace values
            for country_region in df_filtered_by_day.index:
                # Confirmed
                value_confirmed = df_filtered_by_day.loc[df_filtered_by_day.index == country_region, 'confirmed'].astype(
                    int)
                df_template.loc[df_template['ISO 3166-2 Code'] ==
                                country_region, 'Confirmed'] = int(value_confirmed)

                # Deaths
                value_deaths = df_filtered_by_day.loc[df_filtered_by_day.index == country_region, 'deaths'].astype(
                    int)
                df_template.loc[df_template['ISO 3166-2 Code'] ==
                                country_region, 'Deaths'] = int(value_deaths)

                # Recovered
                value_recovered = df_filtered_by_day.loc[df_filtered_by_day.index == country_region, 'recovered'].astype(
                    int)
            
            df_filtered=df_template.loc[df_template['ISO 3166-2 Code'].str.contains('PE-')]
            df_filtered.to_csv(PATH_CSV+d+'.csv', index=False)
        except Exception as e:
            print(d,e)

        


if __name__ == "__main__":
    print("======================PERU======================")
    load_and_generatecsv(['2021-05-13','2021-05-12'])
