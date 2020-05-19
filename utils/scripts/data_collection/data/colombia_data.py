import pandas as pd
import numpy as np
import datetime
import sys
import os


def get_iso_by_country_name(country_name, mode):

    array_iso = np.array(['CO-AMA',
                          'CO-ANT',
                          'CO-ARA',
                          'CO-SAP',
                          'CO-ATL',
                          'CO-ATL',
                          'CO-DC',
                          'CO-BOL',
                          'CO-BOY',
                          'CO-CAU',
                          'CO-CAL',
                          'CO-CAQ',
                          'CO-BOL',
                          'CO-CAS',
                          'CO-CAU',
                          'CO-CES',
                          'CO-COR',
                          'CO-CUN',
                          'CO-CHO',
                          'CO-HUI',
                          'CO-LAG',
                          'CO-MAG',
                          'CO-MET',
                          'CO-NAR',
                          'CO-NSA',
                          'CO-PUT',
                          'CO-QUI',
                          'CO-RIS',
                          'CO-MAG',
                          'CO-SAN',
                          'CO-SUC',
                          'CO-TOL',
                          'CO-VAC',
                          'CO-VAU'])

    array_brazil_csv = np.array(['Amazonas',
                                 'Antioquia',
                                 'Arauca',
                                 'Archipiélago de San Andrés Providencia y Santa Catalina',
                                 'Atlántico',
                                 'Barranquilla D.E.',
                                 'Bogotá D.C.',
                                 'Bolívar',
                                 'Boyacá',
                                 'Buenaventura D.E.',
                                 'Caldas',
                                 'Caquetá',
                                 'Cartagena D.T. y C.',
                                 'Casanare',
                                 'Cauca',
                                 'Cesar',
                                 'Chocó',
                                 'Córdoba',
                                 'Cundinamarca',
                                 'Huila',
                                 'La Guajira',
                                 'Magdalena',
                                 'Meta',
                                 'Nariño',
                                 'Norte de Santander',
                                 'Putumayo',
                                 'Quindío',
                                 'Risaralda',
                                 'Santa Marta D.T. y C.',
                                 'Santander',
                                 'Sucre',
                                 'Tolima',
                                 'Valle del Cauca',
                                 'Vaupés'])

    array_brazil_fixed = np.array(['Amazonas',
                                   'Antioquia',
                                   'Arauca',
                                   'San Andres y Providencia',
                                   'Atlantico',
                                   'Atlantico',
                                   'Bogota',
                                   'Bolivar',
                                   'Boyaca',
                                   'Cauca',
                                   'Caldas',
                                   'Caqueta',
                                   'Bolivar',
                                   'Casanare',
                                   'Cauca',
                                   'Cesar',
                                   'Choco',
                                   'Cordoba',
                                   'Cundinamarca',
                                   'Huila',
                                   'La Guajira',
                                   'Magdalena',
                                   'Meta',
                                   'Narino',
                                   'Norte de Santander',
                                   'Putumayo',
                                   'Quindio',
                                   'Risaralda',
                                   'Magdalena',
                                   'Santander',
                                   'Sucre',
                                   'Tolima',
                                   'Valle del Cauca',
                                   'Vaupes'])

    df = pd.DataFrame({'ISO 3166-2 Code': array_iso,
                       'Remote': array_brazil_csv, 'Local': array_brazil_fixed})

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
    path_colombia_csv = "https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD&bom=true&format=true"
    path_dsrp = "https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/daily_reports/2020-03-08.csv"
    path_csv = "utils/scripts/data_collection/data/colombia_temporal/"
    path_per_patient_csv = 'latam_covid_19_data/per_patient/CO.csv'
    data_colombia = pd.read_csv(path_colombia_csv)
    # SAVE FILE
    data_colombia.to_csv(path_per_patient_csv, index=False)

    data_dsrp = pd.read_csv(path_dsrp)

    array_dates_csv, array_dates = generate_list_dates(path_dsrp_daily_reports)

    total_confirmed=[0]*800
    total_death=[0]*800
    total_recover=[0]*800

    for d in list(np.flip(array_dates)):  # array_dates

        temp_dsrp = data_dsrp[data_dsrp['ISO 3166-2 Code']
                              .str.contains('CO-')].copy()

        temp_dsrp['Confirmed'] = 0
        temp_dsrp['Deaths'] = 0
        temp_dsrp['Recovered'] = 0

        # Colombia
        data = data_colombia[data_colombia['fecha reporte web'].str.contains(d)]
        data = data.fillna('')
        data.reset_index(drop=True)

        data_confirmed = data[data['fecha reporte web'] != '-   -']
        data_confirmed = data_confirmed.groupby(['Departamento o Distrito ']).size().reset_index(name='Confirmed')

        data_death = data_colombia[data_colombia['Fecha de muerte'].str.contains(d)]
        data_death = data_death[data_death['Fecha de muerte'] != '-   -']
        data_death = data_death.fillna('')
        data_death = data_death.groupby(['Departamento o Distrito ']).size().reset_index(name='Deaths')

        data_recovered = data_colombia[data_colombia['Fecha recuperado'].str.contains(d)]
        data_recovered = data_recovered[data_recovered['Fecha recuperado'] != '-   -']
        data_recovered = data_recovered.fillna('')
        data_recovered = data_recovered.groupby(['Departamento o Distrito ']).size().reset_index(name='Recovered')

        for r in range(len(data_confirmed)):
            try:
                country_name_confirmed = get_iso_by_country_name(data_confirmed['Departamento o Distrito '][r], 'remote')
                numero_confirmed = data_confirmed.loc[r]['Confirmed']
                f = temp_dsrp[temp_dsrp['ISO 3166-2 Code'] == country_name_confirmed]
                # print(f.index.values[0])
                # print(f.index.values[0])
                total_confirmed[f.index.values[0]]+=numero_confirmed
                temp_dsrp.loc[f.index.values[0], ['Confirmed']] = total_confirmed[f.index.values[0]]
                # temp_dsrp.loc[f.index.values[0], ['Deaths']] = numero_deaths
                temp_dsrp.loc[f.index.values[0], ['Last Update']] = today
            except Exception as e:
                print('ERROR:[{}]:{}'.format(r, e))

        for r in range(len(data_death)):
            try:
                country_name_deaths = get_iso_by_country_name(data_death['Departamento o Distrito '][r], 'remote')
                numero_deaths = data_death.loc[r]['Deaths']
                f = temp_dsrp[temp_dsrp['ISO 3166-2 Code'] == country_name_deaths]
                # print(f.index.values[0])
                total_death[f.index.values[0]]+=numero_deaths
                temp_dsrp.loc[f.index.values[0], ['Deaths']] = total_death[f.index.values[0]]
                # temp_dsrp.loc[f.index.values[0], ['Deaths']] = numero_deaths
                temp_dsrp.loc[f.index.values[0], ['Last Update']] = today
            except Exception as e:
                print('ERROR:[{}]:{}'.format(r, e))

        for r in range(len(data_recovered)):
            try:
                country_name_recovered = get_iso_by_country_name(data_recovered['Departamento o Distrito '][r], 'remote')
                numero_recovered = data_recovered.loc[r]['Recovered']
                f = temp_dsrp[temp_dsrp['ISO 3166-2 Code'] == country_name_recovered]
                # print(f.index.values[0])
                total_recover[f.index.values[0]]+=numero_recovered
                temp_dsrp.loc[f.index.values[0], ['Recovered']] =  total_recover[f.index.values[0]]
                # temp_dsrp.loc[f.index.values[0], ['Deaths']] = numero_deaths
                temp_dsrp.loc[f.index.values[0], ['Last Update']] = today
            except Exception as e:
                print('ERROR:[{}]:{}'.format(r, e))
            
        print(d, end=' - ')
        temp_dsrp = temp_dsrp.fillna('')
        temp_dsrp.to_csv(path_csv+d+'.csv', index=False)

if __name__ == "__main__":
    load_and_generatecsv('2020-05-13')
