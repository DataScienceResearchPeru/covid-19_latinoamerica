import pandas as pd
import numpy as np
import datetime
import sys
import os


def get_iso_by_country_name(country_name, mode):

    array_iso = np.array(['EC-A',
                          'EC-B',
                          'EC-F',
                          'EC-C',
                          'EC-H',
                          'EC-X',
                          'EC-O',
                          'EC-E',
                          'EC-W',
                          'EC-G',
                          'EC-I',
                          'EC-L',
                          'EC-R',
                          'EC-M',
                          'EC-S',
                          'EC-N',
                          'EC-D',
                          'EC-Y',
                          'EC-P',
                          'EC-SE',
                          'EC-SD',
                          'EC-U',
                          'EC-T',
                          'EC-Z'])

    array_ecuador_csv = np.array(['Azuay',
                                  'Bolívar',
                                  'Carchi',
                                  'Cañar',
                                  'Chimborazo',
                                  'Cotopaxi',
                                  'El Oro',
                                  'Esmeraldas',
                                  'Galápagos',
                                  'Guayas',
                                  'Imbabura',
                                  'Loja',
                                  'Los Ríos',
                                  'Manabí',
                                  'Morona Santiago',
                                  'Napo',
                                  'Orellana',
                                  'Pastaza',
                                  'Pichincha',
                                  'Santa Elena',
                                  'Sto. Domingo Tsáchilas',
                                  'Sucumbíos',
                                  'Tungurahua',
                                  'Zamora Chinchipe'])

    array_ecuador_fixed = np.array(['Azuay',
                                    'Bolivar',
                                    'Carchi',
                                    'Canar',
                                    'Chimborazo',
                                    'Cotopaxi',
                                    'El Oro',
                                    'Esmeraldas',
                                    'Galapagos',
                                    'Guayas',
                                    'Imbabura',
                                    'Loja',
                                    'Los Rios',
                                    'Manabi',
                                    'Morona Santiago',
                                    'Napo',
                                    'Orellana',
                                    'Pastaza',
                                    'Pichincha',
                                    'Santa Elena',
                                    'Santo Domingo de los Tsachilas',
                                    'Sucumbios',
                                    'Tungurahua',
                                    'Zamora-Chinchipe'])

    df = pd.DataFrame({'ISO 3166-2 Code': array_iso,
                       'Remote': array_ecuador_csv, 'Local': array_ecuador_fixed})

    string_iso = ''

    if mode == 'remote':
        string_iso = df[df['Remote'] ==
                        country_name]['ISO 3166-2 Code'].values[0]
    elif mode == 'local':
        string_iso = df[df['Local'] ==
                        country_name]['ISO 3166-2 Code'].values[0]

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
    path_ecuador_confirmed_csv = "https://raw.githubusercontent.com/andrab/ecuacovid/master/datos_crudos/positivas/por_fecha/provincias_por_dia.csv"
    path_ecuador_deaths_csv = "https://raw.githubusercontent.com/andrab/ecuacovid/master/datos_crudos/muertes/por_fecha/provincias_por_dia.csv"
    # path_ecuador_recovered (NOT FOUND)
    path_dsrp = "latam_covid_19_data/templates/daily_reports.csv"
    path_csv = "utils/scripts/data_collection/data/ecuador_temporal/"

    data_ecuador_confirmed = pd.read_csv(path_ecuador_confirmed_csv)
    data_ecuador_deaths = pd.read_csv(path_ecuador_deaths_csv)

    data_dsrp = pd.read_csv(path_dsrp)

    array_dates_csv, array_dates = generate_list_dates(path_dsrp_daily_reports)

    array_iso_fixed = ['EC-A', 'EC-B', 'EC-F', 'EC-C', 'EC-H', 'EC-X', 'EC-O', 'EC-E', 'EC-W', 'EC-G',
                       'EC-I', 'EC-L', 'EC-R', 'EC-M', 'EC-S', 'EC-N', 'EC-D', 'EC-Y', 'EC-P', 'EC-SE', 'EC-SD', 'EC-U', 'EC-T', 'EC-Z']

    for d in array_dates:  # array_dates

        d_fix = datetime.datetime.strptime(d, '%Y-%m-%d')
        d_fix = d_fix.strftime('%d/%m/%Y')

        temp_dsrp = data_dsrp[data_dsrp['ISO 3166-2 Code']
                              .str.contains('EC-')].copy()

        temp_dsrp['Confirmed'] = 0
        temp_dsrp['Deaths'] = 0
        temp_dsrp['Recovered'] = 0

        try:
            data_confirmed = data_ecuador_confirmed[['provincia', str(d_fix)]]
            data_confirmed = data_confirmed.fillna('')
            data_confirmed['ISO 3166-2 Code'] = np.array(array_iso_fixed)
            data_confirmed = data_confirmed.sort_values(by=['ISO 3166-2 Code'])
        except Exception as e:
            print(e)
        try:
            data_deaths = data_ecuador_deaths[['provincia', str(d_fix)]]
            data_deaths = data_deaths.fillna('')
            data_deaths['ISO 3166-2 Code'] = np.array(array_iso_fixed)
            data_deaths = data_deaths.sort_values(by=['ISO 3166-2 Code'])
        except Exception as e:
            print(e)

        try:
            temp_dsrp['Confirmed'] = data_confirmed[str(d_fix)].values
            temp_dsrp['Deaths'] = data_deaths[str(d_fix)].values
            temp_dsrp['Last Update'] = today
        except Exception as e:
            print(e)

        print(d, end=' - ')
        # print(temp_dsrp)
        temp_dsrp = temp_dsrp.fillna('')

        temp_dsrp.to_csv(path_csv+d+'.csv', index=False)


if __name__ == "__main__":
    load_and_generatecsv(['2020-05-22', '2020-02-25'])
