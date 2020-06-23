import datetime
import os
import sys

import numpy as np
import pandas as pd


def load_iso(path):
    # ISO 3166-2
    iso = pd.read_csv(path_iso, sep=',', encoding='latin-1', engine='python')
    isocode = iso['Code']
    isocode = isocode[isocode != 'PE-LMA']
    array = isocode.to_numpy()
    return array


def generate_list_dates(path):
    # Generate dates from files existing
    date_list_csv = []
    path, dirs, files = next(os.walk(os.path.abspath(
        root_relative+'latam_covid_19_data/daily_reports/')))
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


def load_filter_dataframe(path, isocode):
    df = pd.read_csv(path, engine='python')
    df2 = df[df['ISO 3166-2 Code'].str.contains(isocode)]
    return df2


def load_dataframe(path):
    df = pd.read_csv(path, engine='python')
    return df


def fix_format(df):
    df = df.fillna('')

    for m in range(len(df)):

        if df.loc[m]['Confirmed'] != '':
            a = int(float(df.loc[m]['Confirmed']))
        else:
            a = ''

        if df.loc[m]['Deaths'] != '':
            b = int(float(df.loc[m]['Deaths']))
        else:
            b = ''

        if df.loc[m]['Recovered'] != '':
            c = int(float(df.loc[m]['Recovered']))
        else:
            c = ''

        df.loc[m, ['Confirmed']] = str(a)
        df.loc[m, ['Deaths']] = str(b)
        df.loc[m, ['Recovered']] = str(c)

    return df


def execute_country(path_country, path_dsrp, d, isocode, today):
    try:
        data_peru = load_filter_dataframe(path_country+'/'+d+'.csv', isocode)
        data_peru = data_peru.fillna('')
        data_dsrp_day = load_dataframe(path_dsrp+'/'+d+'.csv')
        data_dsrp_day = fix_format(data_dsrp_day)

        for l in range(len(data_peru)):
            a = data_dsrp_day[data_dsrp_day['ISO 3166-2 Code']
                              == data_peru.loc[l]['ISO 3166-2 Code']]

            if data_peru.loc[l]['Confirmed'] != '':
                number_confirmed = int(float(data_peru.loc[l]['Confirmed']))
            else:
                number_confirmed = ''

            if data_peru.loc[l]['Deaths'] != '':
                number_deaths = int(float(data_peru.loc[l]['Deaths']))
            else:
                number_deaths = ''

            data_dsrp_day.loc[a.index.values[0], [
                'Confirmed']] = str(number_confirmed)
            data_dsrp_day.loc[a.index.values[0],
                              ['Deaths']] = str(number_deaths)
            data_dsrp_day.loc[a.index.values[0], ['Last Update']] = str(today)

        data_dsrp_day.to_csv(path_dsrp+'/'+d+'.csv',index=False,encoding='utf-8')
    except:
        print('ERROR {},{}'.format(isocode, d))


def load_all_data_temporal(list_date_list):

    command = 'python '
    scripts = [
        # 'utils/scripts/data_collection/data2/argentina_data.py', NOT WORKING
        'data_collection/data2/bolivia_data.py',
        'data_collection/data2/brazil_data.py',
        'data_collection/data2/colombia_data.py',
        'data_collection/data2/costarica_data.py',
        'data_collection/data2/cuba_data.py',
        'data_collection/data2/ecuador_data.py',
        'data_collection/data2/peru_data.py',
        ]

    for file in scripts:
        a = command+file
        print(a)
        os.system(a)

    print("------------------------ALL TEMPORALS CREATED----------------------------")


def time_series_generator_generate():

    command = 'python '
    scripts = [
        'data_time_series/time_series_generator2.py']

    for file in scripts:
        a = command+file
        print(a)
        os.system(a)

    print("------------------------     FINISH     ----------------------------")


def logo():
    print("""                                                                                       
    ,ad8888ba,    ,ad8888ba,   8b           d8  88  88888888ba,              88   ad88888ba   
    d8"'    `"8b  d8"'    `"8b  `8b         d8'  88  88      `"8b           ,d88  d8"     "88  
   d8'           d8'        `8b  `8b       d8'   88  88        `8b        888888  8P       88  
   88            88          88   `8b     d8'    88  88         88            88  Y8,    ,d88  
   88            88          88    `8b   d8'     88  88         88  aaaaaaaa  88   "PPPPPP"88  
   Y8,           Y8,        ,8P     `8b d8'      88  88         8P  """"""""  88           8P  
    Y8a.    .a8P  Y8a.    .a8P       `888'       88  88      .a8P             88  8b,    a8P   
    `"Y8888Y"'    `"Y8888Y"'         `8'        88  88888888Y"'              88  `"Y8888P'    
                                                                                                
                                                                                                
                                                                                                
    88888888ba                        88888888ba,     ad88888ba   88888888ba   88888888ba       
    88      "8b                       88      `"8b   d8"     "8b  88      "8b  88      "8b      
    88      ,8P                       88        `8b  Y8,          88      ,8P  88      ,8P      
    88aaaaaa8P'  8b       d8  888     88         88  `Y8aaaaa,    88aaaaaa8P'  88aaaaaa8P'      
    88""""""8b,  `8b     d8'  888     88         88    `'''''8b,  88''''88'    88""""""'        
    88      `8b   `8b   d8'           88         8P          `8b  88    `8b    88               
    88      a8P    `8b,d8'    888     88      .a8P   Y8a     a8P  88     `8b   88               
    88888888P"       Y88'     888     88888888Y"'     "Y88888P"   88      `8b  88               
                    d8'                                                                        
                    d8'                                                                         
    """)


if __name__ == "__main__":

    root_relative = '../../'

    logo()

    # Path
    path_argentina = os.path.abspath(
        root_relative+'utils/scripts/data_collection/data2/argentina_temporal/')
    path_bolivia = os.path.abspath(
        root_relative+'utils/scripts/data_collection/data2/bolivia_temporal/')
    path_brazil = os.path.abspath(
        root_relative+'utils/scripts/data_collection/data2/brazil_temporal/')
    path_colombia = os.path.abspath(
        root_relative+'utils/scripts/data_collection/data2/colombia_temporal/')
    path_costarica = os.path.abspath(
        root_relative+'utils/scripts/data_collection/data2/costarica_temporal/')
    path_cuba = os.path.abspath(
        root_relative+'utils/scripts/data_collection/data2/cuba_temporal/')
    path_ecuador = os.path.abspath(
        root_relative+'utils/scripts/data_collection/data2/ecuador_temporal/')
    # path_el_salvador = 'utils/scripts/data_collection/data2/el_salvador_temporal/' #BROKEN
    # path_honduras = 'utils/scripts/data_collection/data2/honduras_temporal/' #HONDURAS ALREADY UPDATED
    path_peru = os.path.abspath(
        root_relative+'utils/scripts/data_collection/data2/peru_temporal/')

    path_dsrp = os.path.abspath(
        root_relative+'latam_covid_19_data/daily_reports/')
    path_dsrp_daily_reports = os.path.abspath(
        root_relative+'latam_covid_19_data/daily_reports/')
    path_iso = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/utils/iso3166-2.csv'

    # Loading files
    array_isocode = load_iso(path_iso)
    today = datetime.datetime.today()
    date_list_csv, date_list = generate_list_dates(path_dsrp_daily_reports)
    # HERE YOU DEFINE THE RANGE OF DATES TO UPDATE
    list_date_list = date_list[0:4]

    load_all_data_temporal(list_date_list)

    print('List of dates to be modified:', end='')

    for d in list_date_list:  # date_list

        # data_brazil = load_filter_dataframe(path_brazil+d, 'BR-') DEPRECATED
        # data_costarica = load_filter_dataframe(path_costarica+d, 'CR-') DEPRECATED
        # data_el_salvador = load_filter_dataframe(path_el_salvador+d, 'SV-') DEPRECATED
        # data_honduras = load_filter_dataframe(path_honduras+d, 'HN-') #HONDURAS ALREADY UPDATED

        execute_country(path_argentina, path_dsrp, d, 'AR-', today)
        execute_country(path_bolivia, path_dsrp, d, 'BO-', today)
        execute_country(path_brazil, path_dsrp, d, 'BR-', today)
        execute_country(path_colombia, path_dsrp, d, 'CO-', today)
        execute_country(path_costarica, path_dsrp, d, 'CR-', today)
        execute_country(path_cuba, path_dsrp, d, 'CU-', today)
        execute_country(path_ecuador, path_dsrp, d, 'EC-', today)
        execute_country(path_peru, path_dsrp, d, 'PE-', today)

        print(d, end=' & ')

    time_series_generator_generate()  # Generate time series

    print("----------------------------------FIN--------------------------")
