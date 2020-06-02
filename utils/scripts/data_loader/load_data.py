"""
DATA LOADER .CSV TO ARRAY OF PANDAS DATAFRAME
"""

# Importamos las librerías
import pandas as pd
import datetime
import os

# Variables globales
iso_col_name = "ISO 3166-2 Code"
path = 'latam_covid_19_data/daily_reports/'


def load_files(path):
    path, dirs, files = next(os.walk(path))
    numero_archivos = len(files)
    print('Hay {} archivos en el folder, 1 es del formato y 1 el README. Iteraremos {} veces'.format(
        numero_archivos, numero_archivos-2))

    # Generamos un arreglo con cada día que se tiene en archivo.
    base = (datetime.datetime.today()).date()
    numdays = numero_archivos-2
    date_list = [str(base - datetime.timedelta(days=x))+str('.csv')
                 for x in range(numdays)]
    print('Agregamos {} nombres de archivo al arreglo'.format(len(date_list)))

    # Convertimos a data frame cada archivo.
    data_x_day = []
    indice = 0
    print('En total hay {} archivos'.format(numdays))
    for date in date_list:
        try:
            data_x_day.append(pd.read_csv(path+date, sep=','))
            print('Día {} agregado. Accede mediante el arreglo dataframe[{}] '.format(
                date, indice))
        except:
            print('Día {} no encontrado.'.format(date))
        indice += 1

    return (data_x_day)

if __name__ == "__main__":
    # .csv files to pandas dataframe
    dataframe = load_files(path)

    # INSERT YOUR CODE HERE
    print(dataframe[0])