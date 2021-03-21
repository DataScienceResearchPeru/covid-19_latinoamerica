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

    path_dsrp_daily_reports = 'latam_covid_19_data/daily_reports/'
    path_cuba_csv = "https://raw.githubusercontent.com/covid19cubadata/covid19cubadata.github.io/master/data/covid19-casos.csv"
    path_dsrp = "latam_covid_19_data/templates/daily_reports.csv"
    path_csv = "utils/scripts/data_collection/data/cuba_temporal/"
    path_per_patient_csv = 'latam_covid_19_data/per_patient/CU.csv'

    data_cuba = pd.read_csv(path_cuba_csv)
    # SAVE FILE
    data_cuba.to_csv(path_per_patient_csv, index=False)

    data_dsrp = pd.read_csv(path_dsrp)

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
        temp_dsrp.to_csv(path_csv+d+'.csv', index=False)


if __name__ == "__main__":

    print("======================CUBA======================")
    load_and_generatecsv(['2021-03-21', '2021-03-20', '2021-03-19', '2021-03-18', '2021-03-17', '2021-03-16', '2021-03-15', '2021-03-14', '2021-03-13', '2021-03-12', '2021-03-11', '2021-03-10', '2021-03-09', '2021-03-08', '2021-03-07', '2021-03-06', '2021-03-05', '2021-03-04', '2021-03-03', '2021-03-02', '2021-03-01', '2021-02-28', '2021-02-27', '2021-02-26', '2021-02-25', '2021-02-24', '2021-02-23', '2021-02-22', '2021-02-21', '2021-02-20', '2021-02-19', '2021-02-18', '2021-02-17', '2021-02-16', '2021-02-15', '2021-02-14', '2021-02-13', '2021-02-12', '2021-02-11', '2021-02-10', '2021-02-09', '2021-02-08', '2021-02-07', '2021-02-06', '2021-02-05', '2021-02-04', '2021-02-03', '2021-02-02', '2021-02-01', '2021-01-31', '2021-01-30', '2021-01-29', '2021-01-28', '2021-01-27', '2021-01-26', '2021-01-25', '2021-01-24', '2021-01-23', '2021-01-22', '2021-01-21', '2021-01-20', '2021-01-19', '2021-01-18', '2021-01-17', '2021-01-16', '2021-01-15', '2021-01-14', '2021-01-13', '2021-01-12', '2021-01-11', '2021-01-10', '2021-01-09', '2021-01-08', '2021-01-07', '2021-01-06', '2021-01-05', '2021-01-04', '2021-01-03', '2021-01-02', '2021-01-01', '2020-12-31', '2020-12-30', '2020-12-29', '2020-12-28', '2020-12-27', '2020-12-26', '2020-12-25', '2020-12-24', '2020-12-23', '2020-12-22', '2020-12-21', '2020-12-20', '2020-12-19', '2020-12-18', '2020-12-17', '2020-12-16', '2020-12-15', '2020-12-14', '2020-12-13', '2020-12-12', '2020-12-11', '2020-12-10', '2020-12-09', '2020-12-08', '2020-12-07', '2020-12-06', '2020-12-05', '2020-12-04', '2020-12-03', '2020-12-02', '2020-12-01', '2020-11-30', '2020-11-29', '2020-11-28', '2020-11-27', '2020-11-26', '2020-11-25', '2020-11-24', '2020-11-23', '2020-11-22', '2020-11-21', '2020-11-20', '2020-11-19', '2020-11-18', '2020-11-17', '2020-11-16', '2020-11-15', '2020-11-14', '2020-11-13', '2020-11-12', '2020-11-11', '2020-11-10', '2020-11-09', '2020-11-08', '2020-11-07', '2020-11-06', '2020-11-05', '2020-11-04', '2020-11-03', '2020-11-02', '2020-11-01', '2020-10-31', '2020-10-30', '2020-10-29', '2020-10-28', '2020-10-27', '2020-10-26', '2020-10-25', '2020-10-24', '2020-10-23', '2020-10-22', '2020-10-21', '2020-10-20', '2020-10-19', '2020-10-18', '2020-10-17', '2020-10-16', '2020-10-15', '2020-10-14', '2020-10-13', '2020-10-12', '2020-10-11', '2020-10-10', '2020-10-09', '2020-10-08', '2020-10-07', '2020-10-06', '2020-10-05', '2020-10-04', '2020-10-03', '2020-10-02', '2020-10-01', '2020-09-30', '2020-09-29', '2020-09-28', '2020-09-27', '2020-09-26', '2020-09-25', '2020-09-24', '2020-09-23', '2020-09-22', '2020-09-21', '2020-09-20', '2020-09-19', '2020-09-18', '2020-09-17', '2020-09-16', '2020-09-15', '2020-09-14', '2020-09-13', '2020-09-12', '2020-09-11', '2020-09-10', '2020-09-09', '2020-09-08', '2020-09-07', '2020-09-06', '2020-09-05', '2020-09-04', '2020-09-03', '2020-09-02', '2020-09-01', '2020-08-31', '2020-08-30', '2020-08-29', '2020-08-28', '2020-08-27', '2020-08-26', '2020-08-25', '2020-08-24', '2020-08-23', '2020-08-22', '2020-08-21', '2020-08-20', '2020-08-19', '2020-08-18', '2020-08-17', '2020-08-16', '2020-08-15', '2020-08-14', '2020-08-13', '2020-08-12', '2020-08-11', '2020-08-10', '2020-08-09', '2020-08-08', '2020-08-07', '2020-08-06', '2020-08-05', '2020-08-04', '2020-08-03', '2020-08-02', '2020-08-01', '2020-07-31', '2020-07-30', '2020-07-29', '2020-07-28', '2020-07-27', '2020-07-26', '2020-07-25', '2020-07-24', '2020-07-23', '2020-07-22', '2020-07-21', '2020-07-20', '2020-07-19', '2020-07-18', '2020-07-17', '2020-07-16', '2020-07-15', '2020-07-14', '2020-07-13', '2020-07-12', '2020-07-11', '2020-07-10', '2020-07-09', '2020-07-08', '2020-07-07', '2020-07-06', '2020-07-05', '2020-07-04', '2020-07-03', '2020-07-02', '2020-07-01', '2020-06-30', '2020-06-29', '2020-06-28', '2020-06-27', '2020-06-26', '2020-06-25', '2020-06-24', '2020-06-23', '2020-06-22', '2020-06-21', '2020-06-20', '2020-06-19', '2020-06-18', '2020-06-17', '2020-06-16', '2020-06-15', '2020-06-14', '2020-06-13', '2020-06-12', '2020-06-11', '2020-06-10', '2020-06-09', '2020-06-08', '2020-06-07', '2020-06-06', '2020-06-05', '2020-06-04', '2020-06-03', '2020-06-02', '2020-06-01', '2020-05-31', '2020-05-30', '2020-05-29', '2020-05-28', '2020-05-27', '2020-05-26', '2020-05-25', '2020-05-24', '2020-05-23', '2020-05-22', '2020-05-21', '2020-05-20', '2020-05-19', '2020-05-18', '2020-05-17', '2020-05-16', '2020-05-15', '2020-05-14', '2020-05-13', '2020-05-12', '2020-05-11', '2020-05-10', '2020-05-09', '2020-05-08', '2020-05-07', '2020-05-06', '2020-05-05', '2020-05-04', '2020-05-03', '2020-05-02', '2020-05-01', '2020-04-30', '2020-04-29', '2020-04-28', '2020-04-27', '2020-04-26', '2020-04-25', '2020-04-24', '2020-04-23', '2020-04-22', '2020-04-21', '2020-04-20', '2020-04-19', '2020-04-18', '2020-04-17', '2020-04-16', '2020-04-15', '2020-04-14', '2020-04-13', '2020-04-12', '2020-04-11', '2020-04-10', '2020-04-09', '2020-04-08', '2020-04-07', '2020-04-06', '2020-04-05', '2020-04-04', '2020-04-03', '2020-04-02', '2020-04-01', '2020-03-31', '2020-03-30', '2020-03-29', '2020-03-28', '2020-03-27', '2020-03-26', '2020-03-25', '2020-03-24', '2020-03-23', '2020-03-22', '2020-03-21', '2020-03-20', '2020-03-19', '2020-03-18', '2020-03-17', '2020-03-16', '2020-03-15', '2020-03-14', '2020-03-13', '2020-03-12', '2020-03-11', '2020-03-10', '2020-03-09', '2020-03-08', '2020-03-07', '2020-03-06', '2020-03-05', '2020-03-04', '2020-03-03', '2020-03-02', '2020-03-01', '2020-02-29', '2020-02-28', '2020-02-27', '2020-02-26', '2020-02-25'])
