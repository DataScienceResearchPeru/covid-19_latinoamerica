import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

DATA_URL_CONFIRMED = 'https://raw.githubusercontent.com/elhenrico/covid19-Brazil-timeseries/master/confirmed-cases.csv'
DATA_URL_DEATHS = 'https://raw.githubusercontent.com/elhenrico/covid19-Brazil-timeseries/master/deaths.csv'
DATA_TEMPLATE_URL = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/templates/daily_report.csv'
PATH_CSV = "utils/scripts/data_collection/data/brazil_temporal/"
PATH_DSRP_DAILY_REPORTS = 'latam_covid_19_data/daily_reports/'
LAST_UPDATE = datetime.today().isoformat()
DICT_PLACES={'Acre':'BR-AC',
            'Amapá':'BR-AP',
            'Amazonas':'BR-AM',
            'Pará':'BR-PA',
            'Rondônia':'BR-RO',
            'Roraima':'BR-RR',
            'Tocantins':'BR-TO',
            'Alagoas':'BR-AL',
            'Bahia':'BR-BA',
            'Ceará':'BR-CE',
            'Maranhão':'BR-MA',
            'Paraíba':'BR-PB',
            'Pernambuco':'BR-PE',
            'Piauí':'BR-PI',
            'Rio Grande do Norte':'BR-RN',
            'Sergipe':'BR-SE',
            'Espirito Santo':'BR-ES',
            'Minas Gerais':'BR-MG',
            'Rio de Janeiro':'BR-RJ',
            'São Paulo':'BR-SP',
            'Paraná':'BR-PR',
            'Rio Grande do Sul':'BR-RS',
            'Santa Catarina':'BR-SC',
            'Distrito Federal':'BR-DF',
            'Goiás':'BR-GO',
            'Mato Grosso':'BR-MT',
            'Mato Grosso do Sul':'BR-MS',
            }

def load_and_generatecsv(list_date_list):

    df_confirmed=pd.read_csv(DATA_URL_CONFIRMED)
    df_confirmed['ISO 3166-2 Code']=df_confirmed['Unnamed: 0'].map(DICT_PLACES)
    df_confirmed=df_confirmed.dropna()

    df_deaths=pd.read_csv(DATA_URL_DEATHS)
    df_deaths['ISO 3166-2 Code']=df_deaths['Unnamed: 0'].map(DICT_PLACES)
    df_deaths=df_deaths.dropna()

    df_template=pd.read_csv(DATA_TEMPLATE_URL)
    df_template=df_template.fillna(0)
    #df_template['Confirmed']=df_template['Confirmed'].astype(int)
    #df_template['Deaths']=df_template['Deaths'].astype(int)
    #df_template['Recovered']=df_template['Recovered'].astype(int)
    df_template['Last Update']=LAST_UPDATE

    for day in list_date_list:
        try:
            for country_code in df_confirmed['ISO 3166-2 Code']:
                
                """Confirmed"""
                day_adapted=datetime.strptime(day, '%Y-%m-%d').strftime('%d/%m/%Y')
                value=df_confirmed[df_confirmed['ISO 3166-2 Code']==country_code][day_adapted].values[0]
                df_template.loc[df_template['ISO 3166-2 Code']==country_code,'Confirmed']=int(value)
                
                """Deaths"""
                day_adapted=datetime.strptime(day, '%Y-%m-%d').strftime('%d/%m/%Y')
                value=df_deaths[df_deaths['ISO 3166-2 Code']==country_code][day_adapted].values[0]
                df_template.loc[df_template['ISO 3166-2 Code']==country_code,'Deaths']=int(value)


            df_filtered=df_template.loc[df_template['ISO 3166-2 Code'].str.contains('BR-')]
            df_filtered['Confirmed']=df_filtered['Confirmed'].astype(int)
            df_filtered['Deaths']=df_filtered['Deaths'].astype(int)
            df_filtered['Recovered']=df_filtered['Recovered'].astype(int)
            df_filtered.to_csv(PATH_CSV+day+'.csv', index=False)

        except Exception as e:
            print(day,e)

if __name__ == "__main__":
    print("======================BRAZIL======================")
    load_and_generatecsv(['2021-05-13','2021-05-11'])