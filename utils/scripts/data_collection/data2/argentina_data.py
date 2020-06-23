import pandas as pd
import numpy as np
import datetime
import sys
import os


def get_iso_by_country_name(country_name, mode):

    array_iso = np.array(['AR-B',
                          'AR-K',
                          'AR-H',
                          'AR-U',
                          'AR-C',
                          'AR-X',
                          'AR-W',
                          'AR-E',
                          'AR-P',
                          'AR-Y',
                          'AR-L',
                          'AR-F',
                          'AR-M',
                          'AR-N',
                          'AR-Q',
                          'AR-R',
                          'AR-A',
                          'AR-J',
                          'AR-D',
                          'AR-Z',
                          'AR-S',
                          'AR-G',
                          'AR-V',
                          'AR-T'])

    array_argentina_csv = np.array(['Buenos Aires',
                                    'Catamarca',
                                    'Chaco',
                                    'Chubut',
                                    'CABA',
                                    'Córdoba',
                                    'Corrientes',
                                    'Entre Ríos',
                                    'Formosa',
                                    'Jujuy',
                                    'La Pampa',
                                    'La Rioja',
                                    'Mendoza',
                                    'Misiones',
                                    'Neuquén',
                                    'Río Negro',
                                    'Salta',
                                    'San Juan',
                                    'San Luis',
                                    'Santa Cruz',
                                    'Santa Fe',
                                    'Santiago del Estero',
                                    'Tierra del Fuego',
                                    'Tucumán'])

    array_argentina_fixed = np.array(['Buenos Aires',
                                      'Catamarca',
                                      'Chaco',
                                      'Chubut',
                                      'Ciudad Autonoma de Buenos Aires',
                                      'Cordoba',
                                      'Corrientes',
                                      'Entre Rios',
                                      'Formosa',
                                      'Jujuy',
                                      'La Pampa',
                                      'La Rioja',
                                      'Mendoza',
                                      'Misiones',
                                      'Neuquen',
                                      'Rio Negro',
                                      'Salta',
                                      'San Juan',
                                      'San Luis',
                                      'Santa Cruz',
                                      'Santa Fe',
                                      'Santiago del Estero',
                                      'Tierra del Fuego',
                                      'Tucuman'])

    df = pd.DataFrame({'ISO 3166-2 Code': array_iso,
                       'Remote': array_argentina_csv, 'Local': array_argentina_fixed})

    string_iso = ''

    if mode == 'remote':
        string_iso = df[df['Remote'].str.contains(
            country_name)]['ISO 3166-2 Code'].values[0]
    elif mode == 'local':
        string_iso = df[df['Local'].str.contains(
            country_name)]['ISO 3166-2 Code'].values[0]

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

    path_dsrp_daily_reports = os.path.abspath(root_relative+'latam_covid_19_data/daily_reports/')
    path_argentina_csv = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"
    path_dsrp = os.path.abspath(root_relative+"latam_covid_19_data/templates/daily_reports.csv")
    path_csv = os.path.abspath(root_relative+"utils/scripts/data_collection/data2/argentina_temporal/")
    path_per_patient_csv = os.path.abspath(root_relative+'latam_covid_19_data/per_patient/AR.csv')

    data_argentina = pd.read_csv(path_argentina_csv,encoding='utf-16',delimiter=',', engine='python')
    # SAVE FILE
    data_argentina.to_csv(path_per_patient_csv, index=False,encoding='utf-8')

    data_dsrp = pd.read_csv(path_dsrp, engine='python')

    array_dates_csv, array_dates = generate_list_dates(path_dsrp_daily_reports)

    total_confirmed = [0]*800
    total_death = [0]*800
    total_recover = [0]*800

    data_argentina = data_argentina[['fecha_diagnostico', 'residencia_provincia_nombre', 'sexo', 'fecha_fallecimiento']]
    data_argentina = data_argentina.fillna('')

    for d in list(np.flip(array_dates)):  # array_dates

        temp_dsrp = data_dsrp[data_dsrp['ISO 3166-2 Code']
                              .str.contains('AR-')].copy()

        temp_dsrp['Confirmed'] = 0
        temp_dsrp['Deaths'] = 0
        temp_dsrp['Recovered'] = 0

        # Colombia
        data = data_argentina[data_argentina['fecha_diagnostico'].str.contains(
            d)]
        data = data.fillna('')
        data.reset_index(drop=True)

        data_confirmed = data[data['fecha_diagnostico'] != ' ']
        data_confirmed = data_confirmed.groupby(
            ['residencia_provincia_nombre']).size().reset_index(name='Confirmed')

        data_death = data_argentina[data_argentina['fecha_fallecimiento'].str.contains(
            d)]
        data_death = data_death[data_death['fecha_fallecimiento'] != ' ']
        data_death = data_death.fillna('')
        data_death = data_death.groupby(
            ['residencia_provincia_nombre']).size().reset_index(name='Deaths')

        # DATA RECOVERED NOT FOUND
        # data_recovered = data_colombia[data_colombia['Fecha recuperado'].str.contains(d)]
        # data_recovered = data_recovered[data_recovered['Fecha recuperado'] != ' ']
        # data_recovered = data_recovered.fillna('')
        # data_recovered = data_recovered.groupby(['residencia_provincia_nombre']).size().reset_index(name='Recovered')

        for r in range(len(data_confirmed)):
            try:
                country_name_confirmed = get_iso_by_country_name(
                    data_confirmed['residencia_provincia_nombre'][r], 'remote')
                numero_confirmed = data_confirmed.loc[r]['Confirmed']
                f = temp_dsrp[temp_dsrp['ISO 3166-2 Code']
                              == country_name_confirmed]
                # print(f.index.values[0])
                # print(f.index.values[0])
                total_confirmed[f.index.values[0]] += numero_confirmed
                temp_dsrp.loc[f.index.values[0], ['Confirmed']
                              ] = total_confirmed[f.index.values[0]]
                # temp_dsrp.loc[f.index.values[0], ['Deaths']] = numero_deaths
                temp_dsrp.loc[f.index.values[0], ['Last Update']] = today
            except Exception as e:
                print('ERROR:[{}]:{}'.format(r, e))

        for r in range(len(data_death)):
            try:
                country_name_deaths = get_iso_by_country_name(
                    data_death['residencia_provincia_nombre'][r], 'remote')
                numero_deaths = data_death.loc[r]['Deaths']
                f = temp_dsrp[temp_dsrp['ISO 3166-2 Code']
                              == country_name_deaths]
                # print(f.index.values[0])
                total_death[f.index.values[0]] += numero_deaths
                temp_dsrp.loc[f.index.values[0], ['Deaths']
                              ] = total_death[f.index.values[0]]
                # temp_dsrp.loc[f.index.values[0], ['Deaths']] = numero_deaths
                temp_dsrp.loc[f.index.values[0], ['Last Update']] = today
            except Exception as e:
                print('ERROR:[{}]:{}'.format(r, e))

        # for r in range(len(data_recovered)):
        #     try:
        #         country_name_recovered = get_iso_by_country_name(
        #             data_recovered['residencia_provincia_nombre'][r], 'remote')
        #         numero_recovered = data_recovered.loc[r]['Recovered']
        #         f = temp_dsrp[temp_dsrp['ISO 3166-2 Code']
        #                       == country_name_recovered]
        #         # print(f.index.values[0])
        #         total_recover[f.index.values[0]] += numero_recovered
        #         temp_dsrp.loc[f.index.values[0], ['Recovered']
        #                       ] = total_recover[f.index.values[0]]
        #         # temp_dsrp.loc[f.index.values[0], ['Deaths']] = numero_deaths
        #         temp_dsrp.loc[f.index.values[0], ['Last Update']] = today
        #     except Exception as e:
        #         print('ERROR:[{}]:{}'.format(r, e))

        print(d, end=' - ')
        temp_dsrp = temp_dsrp.fillna('')
        temp_dsrp.to_csv(path_csv+'/'+d+'.csv',index=False,encoding='utf-8')


if __name__ == "__main__":
    load_and_generatecsv(['2020-04-01'])
