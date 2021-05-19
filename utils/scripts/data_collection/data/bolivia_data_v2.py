import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

DATA_URL_CONFIRMED = 'https://raw.githubusercontent.com/pr0nstar/covid19-data/master/raw/paho/confirmed.timeline.csv'
DATA_URL_DEATHS = 'https://raw.githubusercontent.com/pr0nstar/covid19-data/master/raw/paho/deaths.timeline.csv'
DATA_TEMPLATE_URL = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/templates/daily_report.csv'
PATH_CSV = "utils/scripts/data_collection/data/bolivia_temporal/"
PATH_DSRP_DAILY_REPORTS = 'latam_covid_19_data/daily_reports/'
LAST_UPDATE = datetime.today().isoformat()

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

    df_confirmed_original=pd.read_csv(DATA_URL_CONFIRMED).fillna(0)
    df_confirmed_original=df_confirmed_original.loc[:, (df_confirmed_original.columns.str.startswith('BO'))|(df_confirmed_original.columns.str.startswith('ISO'))]
    df_confirmed_original.columns=df_confirmed_original.iloc[0].to_list()
    df_confirmed_original=df_confirmed_original.iloc[2:]

    df_deaths_original=pd.read_csv(DATA_URL_DEATHS).fillna(0)
    df_deaths_original=df_deaths_original.loc[:, (df_deaths_original.columns.str.startswith('BO'))|(df_deaths_original.columns.str.startswith('ISO'))]
    df_deaths_original.columns=df_deaths_original.iloc[0].to_list()
    df_deaths_original=df_deaths_original.iloc[2:]
    

    df_template = pd.read_csv(DATA_TEMPLATE_URL)
    df_template=df_template.fillna('')
    # df_template['Confirmed']=df_template['Confirmed'].astype(int)
    # df_template['Deaths']=df_template['Deaths'].astype(int)
    # df_template['Recovered']=df_template['Recovered'].astype(int)
    # df_template['Last Update']=''
    df_template.loc[df_template['ISO 3166-2 Code'].str.contains('BO-'),'Last Update']=LAST_UPDATE

    #array_dates_csv, array_dates = generate_list_dates(PATH_DSRP_DAILY_REPORTS)

    print('Starting iteration')
    for d in list_date_list:  # array_dates
        # print(d, end=' - ')
        try:

            df_confirmed=df_confirmed_original[df_confirmed_original['ADM1_ISOCODE']==d].transpose()

            df_deaths=df_deaths_original[df_deaths_original['ADM1_ISOCODE']==d].transpose()

            for country_code in df_confirmed.index[1:]:
                
                value_per_contry=df_confirmed.loc[country_code].values[0]
                df_template.loc[df_template['ISO 3166-2 Code']==country_code,'Confirmed']=int(value_per_contry)

                value_per_contry=df_deaths.loc[country_code].values[0]
                df_template.loc[df_template['ISO 3166-2 Code']==country_code,'Deaths']=int(value_per_contry)

                df_filtered=df_template.loc[df_template['ISO 3166-2 Code'].str.contains('BO-')]
                df_filtered.to_csv(PATH_CSV+d+'.csv', index=False)


        except Exception as e:
            print(d,e)

    print('Ended iteration')

if __name__ == "__main__":
    print("======================BOLIVIA======================")
    load_and_generatecsv(['2021-05-13','2021-05-11'])
