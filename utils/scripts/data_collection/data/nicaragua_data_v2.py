import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

DATA_URL = 'https://raw.githubusercontent.com/RRMaximiliano/covid-shiny-app/main/data/observatorio_nicaragua_dep.csv'
DATA_TEMPLATE_URL = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/templates/daily_report.csv'
PATH_CSV = "utils/scripts/data_collection/data/nicaragua_temporal/"
PATH_DSRP_DAILY_REPORTS = 'latam_covid_19_data/daily_reports/'
LAST_UPDATE = datetime.today().isoformat()
DICT_PLACES = {'Boaco':'NI-BO',
               'Carazo':'NI-CA',
               'Chinandega':'NI-CI',
               'Chontales':'NI-CO', 
               'EstelÃ\xad':'NI-ES',
               'Granada':'NI-GR', 
               'Jinotega':'NI-JI', 
               'LeÃ³n':'NI-LE', 
               'Madriz':'NI-MD', 
               'Managua':'NI-MN', 
               'Masaya':'NI-MS',
               'Matagalpa':'NI-MT', 
               'Nueva Segovia':'NI-NS', 
               'RACCN':'NI-AN',
               'RACCS':'NI-AS', 
               'Rio San Juan':'NI-SJ',
               'Rivas':'NI-RI'}


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

    df_original = pd.read_csv(DATA_URL)
    df_original['ISO 3166-2 Code']=df_original['departamento'].map(DICT_PLACES)

    df_template = pd.read_csv(DATA_TEMPLATE_URL)
    df_template=df_template.fillna('')
    # df_template['Confirmed']=df_template['Confirmed'].astype(int)
    # df_template['Deaths']=df_template['Deaths'].astype(int)
    # df_template['Recovered']=df_template['Recovered'].astype(int)
    # df_template['Last Update']=''
    df_template.loc[df_template['ISO 3166-2 Code'].str.contains('NI-'),'Last Update']=LAST_UPDATE


    # CREATE ROWS AUSENCES
    isos_code_unique=df_original['ISO 3166-2 Code'].unique()
    my_date_list=df_original['date'].unique()
    df_complete=pd.DataFrame({'date':day,
                            'ISO 3166-2 Code':country,
                            'cases':np.nan,
                            'deaths':np.nan} for country in isos_code_unique for day in my_date_list   )


    df_complete.set_index(['ISO 3166-2 Code','date'])
    df_original.set_index(['ISO 3166-2 Code','date'])
    df_complete.update(df_original)
    df_complete=df_complete.reset_index()
    df_complete['cases_fixed'] = df_complete.groupby(['ISO 3166-2 Code','date'])['cases'].ffill()
    df_complete['deaths_fixed'] = df_complete.groupby(['ISO 3166-2 Code','date'])['deaths'].ffill()
    df_complete=df_complete.fillna(0)


    print('Starting iteration')
    for day in list_date_list:  # array_dates
        
        df=df_complete
        # Replace values
        for country_region in isos_code_unique:

            try:
                # Confirmed
                value_confirmed = df.loc[(df['ISO 3166-2 Code']==country_region)&
                                        (df['date']==day)]['cases_fixed'].values[0]
                df_template.loc[df_template['ISO 3166-2 Code'] == country_region, 
                                                    'Confirmed'] = int(value_confirmed)
            except Exception as e:
                print(day,e)

            try:
                # Deaths
                value_deaths =df.loc[(df['ISO 3166-2 Code']==country_region)&
                                        (df['date']==day)]['deaths_fixed'].values[0]
                df_template.loc[df_template['ISO 3166-2 Code'] ==country_region,
                                                                 'Deaths'] = int(value_deaths)
            except Exception as e:
                print(day,e)
            finally:        
                df_filtered=df_template.loc[df_template['ISO 3166-2 Code'].str.contains('NI-')]
                df_filtered.to_csv(PATH_CSV+day+'.csv', index=False)

if __name__ == "__main__":
    print("======================NICARAGUA======================")
    load_and_generatecsv(['2021-04-13','2021-04-12'])
