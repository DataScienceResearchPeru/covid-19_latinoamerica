import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests


PATH_DSRP_DAILY_REPORTS = 'latam_covid_19_data/daily_reports/'
DATA_TEMPLATE_URL = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/templates/daily_report.csv'
PATH__TIME_SERIES='latam_covid_19_data/time_series/'
LAST_UPDATE = datetime.today().isoformat()

def generate():

    df_full=pd.DataFrame(columns=pd.read_csv(DATA_TEMPLATE_URL).columns.values)
    df_full['Day']=''
    
    list_report_days=os.listdir(PATH_DSRP_DAILY_REPORTS)
    list_report_days.remove('README.md')

    # ARRAY OF DATAFRAMES TO CONCAT
    array_of_dataframes=[]

    for d in list_report_days:
        print(d,end='->')
        columns_to_read=['ISO 3166-2 Code','Confirmed','Deaths','Recovered']
        df_temp=pd.read_csv(PATH_DSRP_DAILY_REPORTS+d,usecols = columns_to_read)
        df_temp['Day']=pd.to_datetime(d[:-4])
        array_of_dataframes.append(df_temp)

    # GENERATE ALL DATA IN ONE DF
    df_full = pd.concat(array_of_dataframes)
    df_full=df_full.reset_index(drop=True)
    df_full=df_full.fillna(0)
    df_full['Confirmed']=df_full['Confirmed'].astype(int)
    df_full['Deaths']=df_full['Deaths'].astype(int)
    df_full['Recovered']=df_full['Recovered'].astype(int)


    df_time_series=pd.read_csv(DATA_TEMPLATE_URL,usecols=['ISO 3166-2 Code','Country','Subdivision','Last Update'])
    df_time_series['Last Update']=LAST_UPDATE

    df_time_series_confirmed=df_time_series
    df_time_series_deaths=df_time_series
    df_time_series_recovered=df_time_series

    for day in np.sort(np.array(list_report_days)):
        day=day[:-4]
        for country_code in df_time_series_confirmed['ISO 3166-2 Code']:  
            """Confirmed"""
            condition=((df_full['ISO 3166-2 Code']==country_code) &
                    (df_full['Day']==day))
            value=df_full[condition]['Confirmed'].values[0]
            #print(day,country_code,value)
            condition_time_series=(df_time_series_confirmed['ISO 3166-2 Code']==country_code)
            df_time_series_confirmed.loc[condition_time_series,day]=value

            """Deaths"""
            condition=((df_full['ISO 3166-2 Code']==country_code) &
                    (df_full['Day']==day))
            value=df_full[condition]['Deaths'].values[0]
            #print(day,country_code,value)
            condition_time_series=(df_time_series_deaths['ISO 3166-2 Code']==country_code)
            df_time_series_deaths.loc[condition_time_series,day]=value

            """Recovered"""
            condition=((df_full['ISO 3166-2 Code']==country_code) &
                    (df_full['Day']==day))
            value=df_full[condition]['Recovered'].values[0]
            #print(day,country_code,value)
            condition_time_series=(df_time_series_recovered['ISO 3166-2 Code']==country_code)
            df_time_series_recovered.loc[condition_time_series,day]=value
            
    for day in list_report_days:
        day=day[:-4]
        df_time_series_confirmed[day]=df_time_series_confirmed[day].astype(int)


    """Save files"""
    df_time_series_confirmed.to_csv(PATH__TIME_SERIES+'time_series_confirmed.csv',
                                    sep=',', index=False)
    df_time_series_deaths.to_csv(PATH__TIME_SERIES+'time_series_deaths.csv', 
                                    sep=',', index=False)
    df_time_series_recovered.to_csv(PATH__TIME_SERIES+'time_series_recovered.csv',
                                    sep=',', index=False)

    return True

if __name__ == "__main__":
    print("======================TIME SERIES======================")
    generate()
