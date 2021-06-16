import requests
import io
import pandas as pd
from datetime import datetime, timedelta
import os

DATA_URL = 'https://www.data.gouv.fr/fr/datasets/r/f4935ed4-7a88-44e4-8f8a-33910a151d42'
DATA_TEMPLATE_URL = 'https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/templates/daily_report.csv'
PATH_CSV = "utils/scripts/data_collection/data/francia_temporal/"
PATH_DSRP_DAILY_REPORTS = 'latam_covid_19_data/daily_reports/'
LAST_UPDATE = datetime.today().isoformat()
DICT_PLACES = {'Guadeloupe': 'FR-GP',
               'Martinique': 'FR-MQ',
               'Guyane Française': 'FR-GF',
               'Guyana': 'FR-GF',
               'Saint Barthélemy': 'FR-BL',
               'Saint Martin': 'FR-MF',
               'Saint-Marin': 'FR-MF',
               # Pierre et Miquelon doesnt appear
               }


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

    file_data = requests.get(DATA_URL).content.decode('utf-8')
    file_data = file_data.replace("#Source de ce jeu de données : https://coronavirus.politologue.com - Les données proposées dans ce fichier sont une compilation des données proposées par le CSSE (The Johns Hopkins University) https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6\r\n#Les données de ce fichier sont celles qui sont produites pour générer les graphiques sur https: //coronavirus.politologue.com\r\n#Vous pouvez utiliser ces données sans problème et une référence à https://coronavirus.politologue.com sera appréciable\r\n-----------------------------------------------\r\n#Certains ne respectent pas la demande de ne pas récupérer trop souvent le fichier pour préserver le serveur (cela ne sert à rien de récupérer toutes les 3 min), le fichier présente désormais les 30 derniers jours seulement\r\n#Si vous souhaitez avoir accès à l'ensemble, contactez moi, je n'ai pas le temps de faire la chasse à ceux qui ne respectent pas une certaine éthique, alors je fais en sorte de préserver mes ressources\r\n-----------------------------------------------\r\n", "")
    df = pd.read_csv(io.StringIO(file_data), sep=";")
    df['ISO 3166-2 Code'] = df['Pays'].map(DICT_PLACES)
    df = df.dropna()

    df_template = pd.read_csv(DATA_TEMPLATE_URL)
    df_template = df_template.fillna('')
    # df_template['Confirmed']=df_template['Confirmed'].astype(int)
    # df_template['Deaths']=df_template['Deaths'].astype(int)
    # df_template['Recovered']=df_template['Recovered'].astype(int)
    # df_template['Last Update']=''
    df_template.loc[df_template['ISO 3166-2 Code']
                    .str.contains('FR-'), 'Last Update'] = LAST_UPDATE

    print('Starting iteration')
    for day in list_date_list:  # array_dates
        # print(d, end=' - ')
        try:
            df_filtered_by_day = df[df['Date'] == day]
            # Replace values
            for country_region in df_filtered_by_day['ISO 3166-2 Code']:

                # Confirmed
                value_confirmed = df.loc[(df['ISO 3166-2 Code'] == country_region) &
                                         (df['Date'] == day), 'Infections'].values[0]
                df_template.loc[df_template['ISO 3166-2 Code'] ==
                                country_region, 'Confirmed'] = int(value_confirmed)

                # Deaths
                value_deaths = df.loc[(df['ISO 3166-2 Code'] == country_region) &
                                         (df['Date'] == day), 'Deces'].values[0]
                df_template.loc[df_template['ISO 3166-2 Code'] ==
                                country_region, 'Deaths'] = int(value_deaths)


                # Recovered
                value_recovered = df.loc[(df['ISO 3166-2 Code'] == country_region) &
                                         (df['Date'] == day), 'Guerisons'].values[0]
                df_template.loc[df_template['ISO 3166-2 Code'] ==
                                country_region, 'Recovered'] = int(value_recovered)

                # To template
                df_filtered = df_template.loc[df_template['ISO 3166-2 Code'].str.contains('FR-')]
                df_filtered.to_csv(PATH_CSV+day+'.csv', index=False)

        except Exception as e:
            print(day, e)

    print('Ended iteration')


if __name__ == "__main__":
    print("======================FRANCIA======================")
    load_and_generatecsv(['2021-06-14', '2021-05-18'])
