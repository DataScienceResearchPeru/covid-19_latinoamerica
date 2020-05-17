import pandas as pd
import numpy as np
import datetime
import sys
import os


def load_iso(path):
    # ISO 3166-2
    iso = pd.read_csv(path_iso, sep=',')
    isocode = iso['Code']
    isocode = isocode[isocode != 'PE-LMA']
    array = isocode.to_numpy()
    return array


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


def load_filter_dataframe(path, isocode):
    df = pd.read_csv(path)
    df2 = df[df['ISO 3166-2 Code'].str.contains(isocode)]
    return df2


if __name__ == "__main__":
    # Path
    path_brazil = 'utils/scripts/data_collection/data/brazil_temporal/'
    path_costarica = 'utils/scripts/data_collection/data/costarica_temporal/'
    path_el_salvador = 'utils/scripts/data_collection/data/el_salvador_temporal/'
    path_honduras = 'utils/scripts/data_collection/data/honduras_temporal/'
    path_peru = 'utils/scripts/data_collection/data/peru_temporal/'

    path_dsrp = 'latam_covid_19_data/daily_reports/'
    path_iso = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/utils/iso3166-2.csv'

    # Loading files
    array_isocode = load_iso(path_iso)
    date_list_csv, date_list = generate_list_dates(path_dsrp)

    d = '2020-05-15.csv'

    data_brazil = load_filter_dataframe(path_brazil+d, 'BR')
    data_costarica = load_filter_dataframe(path_costarica+d, 'CR')
    #data_el_salvador = load_filter_dataframe(path_el_salvador+d, 'SV')
    #data_honduras = load_filter_dataframe(path_honduras+d, 'HN')
    data_peru = load_filter_dataframe(path_peru+d, 'PE')
