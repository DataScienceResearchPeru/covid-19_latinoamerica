# Importing libraries
import datetime
import os
import time

import numpy as np
import pandas as pd


def generate():

    path = 'latam_covid_19_data/daily_reports/'
    path, dirs, files = next(os.walk(path))
    numero_archivos = len(files)
    print('Hay {} archivos en el folder y 1 el README. Iteraremos {} veces'.format(
        numero_archivos, numero_archivos-1))

    """Loading ISO 3166-2 Code"""

    url = 'utils/iso3166-2.csv'
    template_isocode = pd.read_csv(url, sep=',')
    isocode = template_isocode['Code']
    isocode = isocode[isocode != 'PE-LMA']
    array_isocode = isocode.to_numpy()

    """Generating array with name of files"""

    # Generamos un arreglo con cada día que se tiene en archivo.
    base = (datetime.datetime.today()).date()
    numdays = numero_archivos-1
    date_list = [str(base - datetime.timedelta(days=x))+str('.csv')
                 for x in range(numdays)]
    print('Agregamos {} nombres de archivo al arreglo'.format(len(date_list)))
    str(date_list)

    # Convertimos a data frame cada archivo.
    array_dataframes = []
    indice = 0
    print('En total hay {} archivos'.format(numdays))
    for date in date_list:
        array_dataframes.append(pd.read_csv(path+date, sep=','))
        array_dataframes[indice]['Date'] = date[:-4]
        # Crear dataframe total
        indice += 1

    """# Confirmed"""

    # Extrayendo las mismas columnas
    confirmed = array_dataframes[0].iloc[:, 0:4]
    confirmed = confirmed.fillna('')

    # Extrayendo Confirmados por día de los demás dataframes y añadiendo columnas al data frame inicial

    for i in range(len(array_dataframes)-1):
        m = len(array_dataframes)-1-i
        confirmed[str([array_dataframes[m]['Date'][0]][0])
                  ] = array_dataframes[m][['Confirmed']]

    today = datetime.datetime.now()
    confirmed['Last Update'] = today
    confirmed = confirmed.fillna('')

    """# Deaths"""

    # Extrayendo las mismas columnas
    deaths = array_dataframes[0].iloc[:, 0:4]
    deaths = deaths.fillna('')

    # Extrayendo Confirmados por día de los demás dataframes y añadiendo columnas al data frame inicial

    for i in range(len(array_dataframes)-1):
        m = len(array_dataframes)-1-i
        deaths[str([array_dataframes[m]['Date'][0]][0])
               ] = array_dataframes[m][['Deaths']]

    deaths['Last Update'] = today
    deaths = deaths.fillna('')

    """# Recovered"""

    # Extrayendo las mismas columnas
    recovered = array_dataframes[0].iloc[:, 0:4]
    recovered = recovered.fillna('')

    # Extrayendo Confirmados por día de los demás dataframes y añadiendo columnas al data frame inicial

    for i in range(len(array_dataframes)-1):
        m = len(array_dataframes)-1-i
        recovered[str([array_dataframes[m]['Date'][0]][0])
                  ] = array_dataframes[m][['Recovered']]

    recovered['Last Update'] = today
    recovered = recovered.fillna('')

    """# Save files"""

    confirmed.to_csv(
        'latam_covid_19_data/time_series/time_series_confirmed.csv', sep=',', index=False)
    deaths.to_csv(
        'latam_covid_19_data/time_series/time_series_deaths.csv', sep=',', index=False)
    recovered.to_csv(
        'latam_covid_19_data/time_series/time_series_recovered.csv', sep=',', index=False)

    return True

if __name__ == "__main__":
    generate()
