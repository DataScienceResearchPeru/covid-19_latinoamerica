import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd


DATA_URL = 'https://geovision.uned.ac.cr/oges/archivos_covid/2021_05_28/05_28_21_EXCEL_SERIES.xlsx'
SHEET_CONFIRMED_NAME = '2_1CANT_ACUMULADOS'
SHEET_DEATHS_NAME = '2_3 CANT_FALLECIDOS'
SHEET_RECOVERED_NAME = '2_2 CANT_RECUPERADOS'
DATA_TEMPLATE_URL = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/templates/daily_report.csv'
PATH_CSV = "utils/scripts/data_collection/data/costa_rica_temporal/"
PATH_DSRP_DAILY_REPORTS = 'latam_covid_19_data/daily_reports/'
LAST_UPDATE = datetime.today().isoformat()
DICT_PLACES = {'Alajuela': 'CR-A',
               'Cartago': 'CR-C',
               'Guanacaste': 'CR-G',
               'Heredia': 'CR-H',
               'Limón': 'CR-L',
               'Puntarenas': 'CR-P',
               'San José': 'CR-SJ'}


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

    # DOWNLOAD DATASETS
    print('[COSTA-RICA] Downloading csv...')
    xlsx = pd.ExcelFile(DATA_URL)
    print('[COSTA-RICA] Loading as DataFrame')
    df_confirmed_original = pd.read_excel(
        xlsx, sheet_name=SHEET_CONFIRMED_NAME)
    df_deaths_original = pd.read_excel(xlsx, sheet_name=SHEET_DEATHS_NAME)
    df_recovered_original = pd.read_excel(
        xlsx, sheet_name=SHEET_RECOVERED_NAME)

    # CONFIRMED
    df_confirmed_original = df_confirmed_original.groupby(
        'provincia').sum().reset_index()
    df_confirmed_original = df_confirmed_original.dropna()

    # DEATHS
    df_deaths_original = df_deaths_original.groupby(
        'provincia').sum().reset_index()
    df_deaths_original = df_deaths_original.dropna()

    # RECOVERED
    df_recovered_original = df_recovered_original.groupby(
        'provincia').sum().reset_index()
    df_recovered_original = df_recovered_original.dropna()

    # TEMPLATE
    df_template = pd.read_csv(DATA_TEMPLATE_URL)
    df_template = df_template.fillna('')
    # df_template['Confirmed']=df_template['Confirmed'].astype(int)
    # df_template['Deaths']=df_template['Deaths'].astype(int)
    # df_template['Recovered']=df_template['Recovered'].astype(int)
    # df_template['Last Update']=''
    df_template.loc[df_template['ISO 3166-2 Code']
                    .str.contains('CR-'), 'Last Update'] = LAST_UPDATE
    df_template = df_template[df_template['ISO 3166-2 Code']
                              .str.contains('CR-')]

    print('Starting iteration')
    for day in list_date_list:  # array_dates

        day_splitted = day.split('-')
        df_confirmed = df_confirmed_original
        df_deaths = df_deaths_original
        df_recovered = df_recovered_original
        try:
            # CONFIRMED
            df_confirmed = df_confirmed.loc[:, ['provincia',
                                                datetime(int(day_splitted[0]),
                                                        int(day_splitted[1]),
                                                        int(day_splitted[2]))
                                                ]]
            df_confirmed['ISO 3166-2 Code'] = df_confirmed['provincia'].map(
                DICT_PLACES)

            # DEATHS
            df_deaths = df_deaths.loc[:, ['provincia',
                                        datetime(int(day_splitted[0]),
                                                int(day_splitted[1]),
                                                int(day_splitted[2]))
                                        ]]
            df_deaths['ISO 3166-2 Code'] = df_deaths['provincia'].map(DICT_PLACES)

            # RECOVERED
            df_recovered = df_recovered.loc[:, ['provincia',
                                                datetime(int(day_splitted[0]),
                                                        int(day_splitted[1]),
                                                        int(day_splitted[2]))
                                                ]]
            df_recovered['ISO 3166-2 Code'] = df_recovered['provincia'].map(
                DICT_PLACES)

            for country_region in df_template['ISO 3166-2 Code']:

                try:

                    # CONFIRMED
                    value_per_country_code = df_confirmed.loc[df_confirmed['ISO 3166-2 Code']
                                                            == country_region].values[0][1]
                    df_template.loc[df_template['ISO 3166-2 Code'] ==
                                    country_region, 'Confirmed'] = value_per_country_code

                    # DEATHS
                    value_per_country_code = df_deaths.loc[df_deaths['ISO 3166-2 Code']
                                                        == country_region].values[0][1]
                    df_template.loc[df_template['ISO 3166-2 Code'] ==
                                    country_region, 'Deaths'] = value_per_country_code

                    # RECOVERED
                    value_per_country_code = df_recovered.loc[df_recovered['ISO 3166-2 Code']
                                                            == country_region].values[0][1]
                    df_template.loc[df_template['ISO 3166-2 Code'] ==
                                    country_region, 'Recovered'] = value_per_country_code

                except Exception as e:
                    print(day, e)
                finally:

                    df_filtered = df_template.loc[df_template['ISO 3166-2 Code'].str.contains(
                        'CR-')]
                    df_filtered.to_csv(PATH_CSV+day+'.csv', index=False)

        except Exception as e:
            print(day, e[0:20]+'...')

    print('Ended iteration')


if __name__ == "__main__":
    print("======================COSTA-RICA======================")
    load_and_generatecsv(['2021-05-20', '2021-05-18'])
