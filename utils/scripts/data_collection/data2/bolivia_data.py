import datetime
import os
import sys

import numpy as np
import pandas as pd


def get_iso_by_country_name(country_name, mode):
    array_iso = np.array(['BO-B',
                          'BO-H',
                          'BO-C',
                          'BO-L',
                          'BO-O',
                          'BO-N',
                          'BO-P',
                          'BO-S',
                          'BO-T'])

    array_bolivia_csv = np.array(['Beni',
                                  'Chuquisaca',
                                  'Cochabamba',
                                  'La Paz',
                                  'Oruro',
                                  'Pando',
                                  'Potosí',
                                  'Santa Cruz',
                                  'Tarija'])

    array_bolivia_fixed = np.array(['Beni',
                                    'Chuquisaca',
                                    'Cochabamba',
                                    'La Paz',
                                    'Oruro',
                                    'Pando',
                                    'Potosi',
                                    'Santa Cruz',
                                    'Tarija'])

    df = pd.DataFrame({'ISO 3166-2 Code': array_iso,
                       'Remote': array_bolivia_csv, 'Local': array_bolivia_fixed})

    string_iso = ''

    if mode == 'remote':
        string_iso = df[df['Remote'].str.contains(
            country_name)]['ISO 3166-2 Code'].values
    elif mode == 'local':
        string_iso = df[df['Local'].str.contains(
            country_name)]['ISO 3166-2 Code'].values

    return string_iso


def generate_list_dates(path):
    # Generate dates from files existing
    date_list_csv = []
    path, dirs, files = next(os.walk(path))
    numero_archivos = len(files)
    print('There is {} files on the path and one is README. We iterate {} times...'.format(
        numero_archivos, numero_archivos-1))
    # dates
    base = (datetime.datetime.today()).date()
    numdays = numero_archivos-1
    date_list_csv = [str(base - datetime.timedelta(days=x))+str('.csv')
                     for x in range(numdays)]
    print('Adding {} dates in a list...'.format(len(date_list_csv)))
    date_list = []
    for d in date_list_csv:
        date_list.append(d[:-4])
    print("List of dates:", date_list)
    return date_list_csv, date_list


def load_and_generatecsv(list_date_list):

    today = datetime.datetime.now().strftime('%Y-%m-%d')

    root_relative = '../../'

    path_dsrp_daily_reports = os.path.abspath(
        root_relative+'latam_covid_19_data/daily_reports/')
    path_bolivia_confirmed_csv = "https://github.com/mauforonda/covid19-bolivia/raw/master/confirmados.csv"
    path_bolivia_deaths_csv = "https://github.com/mauforonda/covid19-bolivia/raw/master/decesos.csv"
    path_bolivia_recoverd_csv = "https://github.com/mauforonda/covid19-bolivia/raw/master/recuperados.csv"
    # path_ecuador_recovered (NOT FOUND)
    path_dsrp = os.path.abspath(
        root_relative+"latam_covid_19_data/templates/daily_reports.csv")
    path_csv = os.path.abspath(
        root_relative+"utils/scripts/data_collection/data2/bolivia_temporal/")

    data_bolivia_confirmed = pd.read_csv(
        path_bolivia_confirmed_csv, engine='python')
    data_bolivia_deaths = pd.read_csv(path_bolivia_deaths_csv, engine='python')
    data_bolivia_recovered = pd.read_csv(
        path_bolivia_recoverd_csv, engine='python')

    data_dsrp = pd.read_csv(path_dsrp, engine='python')

    array_dates_csv, array_dates = generate_list_dates(path_dsrp_daily_reports)

    array_bolivia_csv = np.array(['Beni',
                                  'Chuquisaca',
                                  'Cochabamba',
                                  'La Paz',
                                  'Oruro',
                                  'Pando',
                                  'Potosí',
                                  'Santa Cruz',
                                  'Tarija'])

    array_iso = np.array(['BO-B',
                          'BO-H',
                          'BO-C',
                          'BO-L',
                          'BO-O',
                          'BO-N',
                          'BO-P',
                          'BO-S',
                          'BO-T'])

    df_confirmed = data_bolivia_confirmed.set_index('Fecha').T
    df_confirmed = df_confirmed.reset_index(drop=False)
    df_confirmed['ISO 3166-2 Code'] = df_confirmed['index'].apply(
        lambda x: get_iso_by_country_name(x, 'remote'))

    df_deaths = data_bolivia_deaths.set_index('Fecha').T
    df_deaths = df_deaths.reset_index(drop=False)
    df_deaths['ISO 3166-2 Code'] = df_deaths['index'].apply(
        lambda x: get_iso_by_country_name(x, 'remote'))

    df_recovered = data_bolivia_recovered.set_index('Fecha').T
    df_recovered = df_recovered.reset_index(drop=False)
    df_recovered['ISO 3166-2 Code'] = df_recovered['index'].apply(
        lambda x: get_iso_by_country_name(x, 'remote'))

    for d in array_dates:  # array_dates

        temp_dsrp = data_dsrp[data_dsrp['ISO 3166-2 Code']
                              .str.contains('BO-')].copy()

        temp_dsrp['Confirmed'] = 0
        temp_dsrp['Deaths'] = 0
        temp_dsrp['Recovered'] = 0

        for iso in array_iso:

            """
            CONFIRMED
            """

            df_per_iso = df_confirmed[df_confirmed['ISO 3166-2 Code'] == iso]

            try:
                if df_per_iso[d].values[0] != '':
                    number_confirmed = int(float(df_per_iso[d].values[0]))
                else:
                    number_confirmed = ''

                a = temp_dsrp[temp_dsrp['ISO 3166-2 Code'] == iso]
                temp_dsrp.loc[a.index.values[0],
                              'Confirmed'] = number_confirmed
            except Exception as e:
                print(e,'BUT WORKING',end=' - ')
            try:
                """
                DEATHS
                """
                df_per_iso = df_deaths[df_deaths['ISO 3166-2 Code'] == iso]

                if df_per_iso[d].values[0] != '':
                    number_deaths = int(float(df_per_iso[d].values[0]))
                else:
                    number_deaths = ''

                a = temp_dsrp[temp_dsrp['ISO 3166-2 Code'] == iso]
                temp_dsrp.loc[a.index.values[0], 'Deaths'] = number_deaths
            except Exception as e:
                print(e,'BUT WORKING',end=' - ')
            try:
                """
                RECOVERED
                """
                df_per_iso = df_recovered[df_recovered['ISO 3166-2 Code'] == iso]

                if df_per_iso[d].values[0] != '':
                    number_recovered = int(float(df_per_iso[d].values[0]))
                else:
                    number_recovered = ''

                a = temp_dsrp[temp_dsrp['ISO 3166-2 Code'] == iso]
                temp_dsrp.loc[a.index.values[0],
                              'Recovered'] = number_recovered
            except Exception as e:
                print(e,'BUT WORKING',end=' - ')
        print(d, end=' - ')
        # print(temp_dsrp)
        temp_dsrp = temp_dsrp.fillna('')

        temp_dsrp.to_csv(path_csv+'/'+d+'.csv', index=False)


if __name__ == "__main__":
    load_and_generatecsv(['2020-04-03', '2020-04-05'])
