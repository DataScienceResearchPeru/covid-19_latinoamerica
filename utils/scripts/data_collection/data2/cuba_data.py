import pandas as pd
import numpy as np
import datetime
import sys
import os


def get_iso_by_country_name(country_name, mode):

    array_iso = np.array(['CU-15',
                          'CU-09',
                          'CU-08',
                          'CU-06',
                          'CU-12',
                          'CU-14',
                          'CU-11',
                          'CU-99',
                          'CU-03',
                          'CU-10',
                          'CU-04',
                          'CU-16',
                          'CU-01',
                          'CU-07',
                          'CU-13',
                          'CU-05'])

    array_cuba_csv = np.array(['Artemisa',
                               'Camagüey',
                               'Ciego de Ávila',
                               'Cienfuegos',
                               'Granma',
                               'Guantánamo',
                               'Holguín',
                               'Isla de la Juventud',
                               'La Habana',
                               'Las Tunas',
                               'Matanzas',
                               'Mayabeque',
                               'Pinar del Río',
                               'Sancti Spíritus',
                               'Santiago de Cuba',
                               'Villa Clara'])

    array_cuba_fixed = np.array(['Artemisa',
                                 'Camagüey',
                                 'Ciego de Ávila',
                                 'Cienfuegos',
                                 'Granma',
                                 'Guantánamo',
                                 'Holguín',
                                 'Isla de la Juventud',
                                 'La Habana',
                                 'Las Tunas',
                                 'Matanzas',
                                 'Mayabeque',
                                 'Pinar del Río',
                                 'Sancti Spíritus',
                                 'Santiago de Cuba',
                                 'Villa Clara'])

    df = pd.DataFrame({'ISO 3166-2 Code': array_iso,
                       'Remote': array_cuba_csv, 'Local': array_cuba_fixed})

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
    path_cuba_csv = "https://raw.githubusercontent.com/covid19cubadata/covid19cubadata.github.io/master/data/covid19-casos.csv"
    path_dsrp = os.path.abspath(root_relative+"latam_covid_19_data/templates/daily_reports.csv")
    path_csv = os.path.abspath(root_relative+"utils/scripts/data_collection/data2/cuba_temporal/")
    path_per_patient_csv = os.path.abspath(root_relative+'latam_covid_19_data/per_patient/CU.csv')

    data_cuba = pd.read_csv(path_cuba_csv,encoding='utf8', engine='python')
    # SAVE FILE
    data_cuba.to_csv(path_per_patient_csv,encoding='utf8',  index=False, engine='python')

    data_dsrp = pd.read_csv(path_dsrp,encoding='utf8', engine='python')

    array_dates_csv, array_dates = generate_list_dates(path_dsrp_daily_reports)

    total_confirmed = [0]*800
    # total_death = [0]*800
    # total_recover = [0]*800

    data_cuba = data_cuba[['sexo', 'provincia', 'fecha_confirmacion']]
    data_cuba = data_cuba.fillna('')

    for d in list(np.flip(array_dates)):  # array_dates forced

        d_fix = datetime.datetime.strptime(d, '%Y-%m-%d')
        d_fix = d_fix.strftime('%Y/%m/%d')

        temp_dsrp = data_dsrp[data_dsrp['ISO 3166-2 Code'].str.contains('CU-')].copy()

        temp_dsrp['Confirmed'] = 0
        temp_dsrp['Deaths'] = 0
        temp_dsrp['Recovered'] = 0

        # Colombia
        data = data_cuba[data_cuba['fecha_confirmacion'].str.contains(d_fix)]
        data = data.fillna('')
        data.reset_index(drop=True)

        data_confirmed = data[data['provincia'] != ' ']
        data_confirmed = data_confirmed.groupby(['provincia']).size().reset_index(name='Confirmed')

        
        # DATA NOT FOUND
        # data_death = data_argentina[data_argentina['fecha_fallecimiento'].str.contains(
        #     d)]
        # data_death = data_death[data_death['fecha_fallecimiento'] != ' ']
        # data_death = data_death.fillna('')
        # data_death = data_death.groupby(
        #     ['provincia_residencia']).size().reset_index(name='Deaths')

        # DATA RECOVERED NOT FOUND
        # data_recovered = data_colombia[data_colombia['Fecha recuperado'].str.contains(d)]
        # data_recovered = data_recovered[data_recovered['Fecha recuperado'] != ' ']
        # data_recovered = data_recovered.fillna('')
        # data_recovered = data_recovered.groupby(['provincia_residencia']).size().reset_index(name='Recovered')

        for r in range(len(data_confirmed)):
            try:
                country_name_confirmed = get_iso_by_country_name(data_confirmed['provincia'][r], 'remote')
                numero_confirmed = data_confirmed.loc[r]['Confirmed']
                f = temp_dsrp[temp_dsrp['ISO 3166-2 Code'] == country_name_confirmed]
                # print(f.index.values[0])
                # print(f.index.values[0])
                total_confirmed[f.index.values[0]] += numero_confirmed
                temp_dsrp.loc[f.index.values[0], ['Confirmed']] = total_confirmed[f.index.values[0]]
                # temp_dsrp.loc[f.index.values[0], ['Deaths']] = numero_deaths
                temp_dsrp.loc[f.index.values[0], ['Last Update']] = today
            except Exception as e:
                print('ERROR:[{}]:{}'.format(r, e))

        # for r in range(len(data_death)):
        #     try:
        #         country_name_deaths = get_iso_by_country_name(
        #             data_death['provincia_residencia'][r], 'remote')
        #         numero_deaths = data_death.loc[r]['Deaths']
        #         f = temp_dsrp[temp_dsrp['ISO 3166-2 Code']
        #                       == country_name_deaths]
        #         # print(f.index.values[0])
        #         total_death[f.index.values[0]] += numero_deaths
        #         temp_dsrp.loc[f.index.values[0], ['Deaths']
        #                       ] = total_death[f.index.values[0]]
        #         # temp_dsrp.loc[f.index.values[0], ['Deaths']] = numero_deaths
        #         temp_dsrp.loc[f.index.values[0], ['Last Update']] = today
        #     except Exception as e:
        #         print('ERROR:[{}]:{}'.format(r, e))

        # for r in range(len(data_recovered)):
        #     try:
        #         country_name_recovered = get_iso_by_country_name(
        #             data_recovered['provincia_residencia'][r], 'remote')
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
        temp_dsrp.to_csv(path_csv+'/'+d+'.csv', index=False,encoding='utf-8')


if __name__ == "__main__":
    load_and_generatecsv(['2020-05-13','2020-05-12'])
