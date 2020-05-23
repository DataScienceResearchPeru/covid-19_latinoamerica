import datetime
import os
import sys
import zipfile

import numpy as np
import pandas as pd
from six.moves import urllib


def get_iso_by_country_name(country_name, mode):

    array_iso = np.array(['PE-AMA',
                          'PE-ANC',
                          'PE-APU',
                          'PE-ARE',
                          'PE-AYA',
                          'PE-CAJ',
                          'PE-CAL',
                          'PE-CUS',
                          'PE-HUV',
                          'PE-HUC',
                          'PE-ICA',
                          'PE-JUN',
                          'PE-LAL',
                          'PE-LAM',
                          'PE-LIM',
                          'PE-LOR',
                          'PE-MDD',
                          'PE-MOQ',
                          'PE-PAS',
                          'PE-PIU',
                          'PE-PUN',
                          'PE-SAM',
                          'PE-TAC',
                          'PE-TUM',
                          'PE-UCA'])

    array_peru_csv = np.array(['Amazonas',
                               'Ancash',
                               'Apurimac',
                               'Arequipa',
                               'Ayacucho',
                               'Cajamarca',
                               'Callao',
                               'Cusco',
                               'Huancavelica',
                               'Huánuco',
                               'Ica',
                               'Junín',
                               'La Libertad',
                               'Lambayeque',
                               'Lima',
                               'Loreto',
                               'Madre de Dios',
                               'Moquegua',
                               'Pasco',
                               'Piura',
                               'Puno',
                               'San Martín',
                               'Tacna',
                               'Tumbes',
                               'Ucayali'])

    array_peru_fixed = np.array(['Amazonas',
                                 'Ancash',
                                 'Apurimac',
                                 'Arequipa',
                                 'Ayacucho',
                                 'Cajamarca',
                                 'Callao',
                                 'Cusco',
                                 'Huancavelica',
                                 'Huanuco',
                                 'Ica',
                                 'Junin',
                                 'La Libertad',
                                 'Lambayeque',
                                 'Lima',
                                 'Loreto',
                                 'Madre de dios',
                                 'Moquegua',
                                 'Pasco',
                                 'Piura',
                                 'Puno',
                                 'San Martin',
                                 'Tacna',
                                 'Tumbes',
                                 'Ucayali'])

    df = pd.DataFrame({'ISO 3166-2 Code': array_iso,
                       'Remote': array_peru_csv, 'Local': array_peru_fixed})

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


def get_data_per_patient_oficial():
    urllib.request.urlretrieve("https://www.datosabiertos.gob.pe/sites/default/files/DATOSABIERTOS_SISCOVID.zip", "utils/scripts/data_collection/data/peru_temporal/PE.zip")
    
    zip_ref = zipfile.ZipFile("utils/scripts/data_collection/data/peru_temporal/PE.zip", 'r')
    zip_ref.extractall("latam_covid_19_data/per_patient/")
    zip_ref.close()
    
    os.rename('latam_covid_19_data/per_patient/DATOSABIERTOS_SISCOVID.csv', 'latam_covid_19_data/per_patient/PE.csv')

def load_and_generatecsv(list_date_list):

    today = datetime.datetime.now().strftime('%Y-%m-%d')

    path_dsrp_daily_reports = 'latam_covid_19_data/daily_reports/'
    path_peru_csv = "https://raw.githubusercontent.com/jmcastagnetto/covid-19-peru-data/master/datos/covid-19-peru-data.csv"
    
    path_dsrp = "latam_covid_19_data/templates/daily_reports.csv"
    path_csv = "utils/scripts/data_collection/data/peru_temporal/"

    data_peru = pd.read_csv(path_peru_csv)
    data_dsrp = pd.read_csv(path_dsrp)

    array_dates_csv, array_dates = generate_list_dates(path_dsrp_daily_reports)

    get_data_per_patient_oficial()

    for d in array_dates:  # array_dates

        temp_dsrp = data_dsrp[data_dsrp['ISO 3166-2 Code'].str.contains('PE-')].copy()

        temp_dsrp['Confirmed'] = 0
        temp_dsrp['Deaths'] = 0
        temp_dsrp['Recovered'] = 0

        # data_peru
        data = data_peru[data_peru['date'] == d]
        data = data.fillna('')
        data=data[data['region']!='']
        data.reset_index(drop=True)

        for r in np.array(data.index):

            if data['confirmed'][r] != '':
                numero_confirmed = int(float(data['confirmed'][r]))
            else:
                numero_confirmed = ''
            if data['deaths'][r] != '':
                numero_deaths = int(float(data['deaths'][r]))
            else:
                numero_deaths = ''

            try:
                string_iso = get_iso_by_country_name(
                    data_peru["region"][r], 'remote')
                f = temp_dsrp[temp_dsrp['ISO 3166-2 Code'] == string_iso]
                # print(f.index.values[0])
                temp_dsrp.loc[f.index.values[0], ['Confirmed']] = numero_confirmed
                temp_dsrp.loc[f.index.values[0], ['Deaths']] = numero_deaths
                temp_dsrp.loc[f.index.values[0], ['Last Update']] = today
            except Exception as e:
                print('ERROR:[{}]:{}'.format(r,e))

            #numero_confirmed = data['confirmed'][r]

        print(d, end=' - ')

        print(temp_dsrp)
        temp_dsrp = temp_dsrp.fillna('')

        temp_dsrp.to_csv(path_csv+d+'.csv', index=False)


if __name__ == "__main__":
    load_and_generatecsv(['2020-05-15']) 
