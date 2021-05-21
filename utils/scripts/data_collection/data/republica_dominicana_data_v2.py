import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd


DATA_URL = 'https://github.com/gcaff/COVID19-RD/raw/master/data/covid_data_rd.csv'
DATA_TEMPLATE_URL = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/templates/daily_report.csv'
PATH_CSV = "utils/scripts/data_collection/data/republica_dominicana_temporal/"
PATH_DSRP_DAILY_REPORTS = 'latam_covid_19_data/daily_reports/'
LAST_UPDATE = datetime.today().isoformat()
DICT_PLACES = {'Azua': 'DO-02',
               'Baoruco': 'DO-03',
               'Barahona': 'DO-04',
               'Dajabón': 'DO-05',
               'Distrito Nacional': 'DO-06',
               'Duarte': 'DO-08',
               'El Seibo': 'DO-09',
               'Elías Piña': 'DO-30',
               'Espaillat': 'DO-10',
               'Hato Mayor': 'DO-11',
               'Hermanas Mirabal': 'DO-07',
               'Independencia': 'DO-12',
               'La Altagracia': 'DO-13',
               'La Romana': 'DO-14',
               'La Vega': 'DO-28',
               'María Trinidad Sánchez': 'DO-15',
               'Monseñor Nouel': 'DO-29',
               'Monte Cristi': 'DO-16',
               'Monte Plata': 'DO-17',
               'Pedernales': 'DO-18',
               'Peravia': 'DO-19',
               'Puerto Plata': 'DO-20',
               'Samaná': 'DO-21',
               'San Cristóbal': 'DO-31',
               'San José de Ocoa': 'DO-22',
               'San Juan': 'DO-23',
               'San Pedro de Macorís': 'DO-24',
               'Sánchez Ramírez': 'DO-25',
               'Santiago': 'DO-26',
               'Santiago Rodríguez': 'DO-32',
               'Santo Domingo': 'DO-01',
               'Valverde': 'DO-27',
               'No especificado': np.nan
               }


os.makedirs(PATH_CSV, exist_ok=True) 

def generate_list_dates(path):
    # Generate dates from files existing
    date_list_csv = []
    path, dirs, files = next(os.walk(path))
    numero_archivos = len(files)
    print('There is {} files on the path and one is README. We iterate {} times...'.format(
        numero_archivos, numero_archivos-1))
    # dates
    base = (datetime.today()).date()
    numdays = numero_archivos-1
    date_list_csv = [str(base - timedelta(days=x))+str('.csv')
                     for x in range(numdays)]
    print('Adding {} dates in a list...'.format(len(date_list_csv)))
    date_list = []
    for d in date_list_csv:
        date_list.append(d[:-4])
    print("List of dates:", date_list)
    return date_list_csv, date_list


def load_and_generatecsv(list_date_list):

    df = pd.read_csv(DATA_URL,
                     usecols=['fecha', 'provincia', 'casos_acum','defun_acum', 'recuperados'],
                     encoding='latin-1',
                     parse_dates=['fecha'],
                     dayfirst=True)
    df = df.fillna(0)
    df['ISO 3166-2 Code'] = df['provincia'].map(DICT_PLACES)
    df = df.dropna()

    df_template=pd.read_csv(DATA_TEMPLATE_URL)
    df_template=df_template.fillna(0)
    #df_template['Confirmed']=df_template['Confirmed'].astype(int)
    #df_template['Deaths']=df_template['Deaths'].astype(int)
    #df_template['Recovered']=df_template['Recovered'].astype(int)
    df_template['Last Update']=LAST_UPDATE
    df_template.head()

    codecountry_list=df['ISO 3166-2 Code'].unique()

    print('Starting iteration')
    for day in list_date_list:  # array_dates
        # print(d, end=' - ')
        try:
            
            for country_code in codecountry_list:
                value=df[((df['ISO 3166-2 Code']==country_code)&(df['fecha']==day))]['casos_acum'].values[0]
                condition=(df['ISO 3166-2 Code']==country_code)
                df_template.loc[condition,'Confirmed']=int(value)    
                
                value=df[((df['ISO 3166-2 Code']==country_code)&(df['fecha']==day))]['defun_acum'].values[0]
                condition=(df['ISO 3166-2 Code']==country_code)
                df_template.loc[condition,'Deaths']=int(value)
                
                value=df[((df['ISO 3166-2 Code']==country_code)&(df['fecha']==day))]['recuperados'].values[0]
                condition=(df['ISO 3166-2 Code']==country_code)
                df_template.loc[condition,'Recovered']=int(value)
                

            df_filtered=df_template.loc[df_template['ISO 3166-2 Code'].str.contains('DO-')]
            df_filtered['Confirmed']=df_filtered['Confirmed'].astype(int)
            df_filtered['Deaths']=df_filtered['Deaths'].astype(int)
            df_filtered['Recovered']=df_filtered['Recovered'].astype(int)
            df_filtered.to_csv(PATH_CSV+day+'.csv', index=False)

        except Exception as e:
            print(day, e)

    print('Ended iteration')


if __name__ == "__main__":
    print("======================REPUBLICA-DOMINICANA======================")
    load_and_generatecsv(['2021-05-13','2021-05-11'])