import pandas as pd
import sys
import os

def remove_tildes(string):

    string_a = "áéíóúäëïöüâêîôûã"  # character to be replaced
    string_b = "aeiouaeiouaeioua"  # character to replace with

    for index, tilde in enumerate(string_a):
        string = string.replace(tilde, string_b[index])
    return string


def load_and_generatecsv(list_date_list):
    init_date = pd.to_datetime("2020/02/26", format="%Y/%m/%d")

    root_relative = '../../'

    confirmed_url = "https://raw.githubusercontent.com/elhenrico/covid19-Brazil-timeseries/master/confirmed-cases.csv"
    deaths_url = "https://raw.githubusercontent.com/elhenrico/covid19-Brazil-timeseries/master/deaths.csv"
    dsrp_github = os.path.abspath(root_relative+"latam_covid_19_data/templates/daily_reports.csv")


    confirmed = pd.read_csv(confirmed_url, engine='python')
    deaths = pd.read_csv(deaths_url, engine='python')
    compare = pd.read_csv(dsrp_github,encoding='latin-1', engine='python')

    brazil_compare = compare[compare['ISO 3166-2 Code'].str.contains('BR-')]


    # confirmed.iloc[:, 0] = confirmed.iloc[:, 0].apply(remove_tildes)
    # deaths.iloc[:, 0] = deaths.iloc[:, 0].apply(remove_tildes)

    confirmed = confirmed.rename(columns={"Unnamed: 0": "Subdivision", "Unnamed: 1": "ISO 3166-2 Code"})
    deaths = deaths.rename(columns={"Unnamed: 0": "Subdivision", "Unnamed: 1": "ISO 3166-2 Code"})

    confirmed['ISO 3166-2 Code']='BR-' + confirmed['ISO 3166-2 Code'].astype(str)
    deaths['ISO 3166-2 Code']='BR-' + deaths['ISO 3166-2 Code'].astype(str)

    sub_brazil = sorted(brazil_compare['ISO 3166-2 Code'].unique())
    sub_repo = sorted(confirmed.iloc[:, 1].unique())

    # Subdivisiones other than those listed in the main repo
    other_subdivisions = list(set(sub_repo) - (set(sub_brazil)))

    confirmed = confirmed[~confirmed['ISO 3166-2 Code'].isin(other_subdivisions)].sort_values("ISO 3166-2 Code")
    deaths = deaths[~deaths['ISO 3166-2 Code'].isin(other_subdivisions)].sort_values("ISO 3166-2 Code")

    #del confirmed["Code"]
    #del deaths["Code"]

    confirmed_columns = confirmed.columns[2:]
    deaths_columns = deaths.columns[2:]

    columns_order = ["ISO 3166-2 Code", "Country", "Subdivision",
                    "Last Update", "Confirmed", "Deaths", "Recovered"]

    # print(confirmed)

    # print(deaths)
    
    for column in confirmed_columns:
        try:
            day, month = map(int, column.split("/"))
            date = f"{2020}-{month:02}-{day:02}"

            actual_date = pd.to_datetime(date, format="%Y/%m/%d")

            if actual_date < init_date:
                print("Skipping:", actual_date)
                continue

            daily_report_path = os.path.abspath(root_relative+"latam_covid_19_data/templates/daily_reports.csv")
            daily_report = pd.read_csv(daily_report_path, engine='python')

            brazil = daily_report[daily_report['ISO 3166-2 Code'].str.contains('BR-')]
            brazil_index = daily_report[daily_report['ISO 3166-2 Code'].str.contains('BR-')].index

            del brazil["Deaths"]
            del brazil["Confirmed"]

            confirmed_subset = confirmed.loc[:, ['ISO 3166-2 Code', column]]
            deaths_subset = deaths.loc[:, ["ISO 3166-2 Code", column]]
            confirmed_subset = confirmed_subset.rename(columns={column: "Confirmed"})
            deaths_subset = deaths_subset.rename(columns={column: "Deaths"})
            dc = pd.merge(confirmed_subset, deaths_subset, how="left", on="ISO 3166-2 Code")  # Deaths confirmed
            final = pd.merge(brazil, dc, how="left", on="ISO 3166-2 Code").fillna('')
            final = final[columns_order].set_index(brazil_index)

            final["Last Update"] = date

            daily_report.update(final)

            daily_report.Deaths = daily_report.Deaths.fillna(0)
            daily_report.Confirmed = daily_report.Confirmed.fillna(0)
            daily_report.Recovered = daily_report.Recovered.fillna(0)


            daily_report.Deaths = daily_report.Deaths.astype(str)
            daily_report.Confirmed = daily_report.Confirmed.astype(str)
            daily_report.Recovered = daily_report.Recovered.astype(str)

            daily_report.Deaths = daily_report.Deaths.astype(float,errors='ignore')
            daily_report.Confirmed = daily_report.Confirmed.astype(float,errors='ignore')
            daily_report.Recovered = daily_report.Recovered.astype(float,errors='ignore')

            daily_report.Deaths = daily_report.Deaths.astype(int,errors='ignore')
            daily_report.Confirmed = daily_report.Confirmed.astype(int,errors='ignore')
            daily_report.Recovered = daily_report.Recovered.astype(int,errors='ignore')


            path_data = os.path.abspath(root_relative+f"utils/scripts/data_collection/data2/brazil_temporal/{date}.csv")
            #print(daily_report[daily_report.Country=="Brazil"])
            daily_report = daily_report[daily_report['ISO 3166-2 Code'].str.contains('BR-')]
            daily_report.to_csv(path_data, index=False,encoding='utf-8')

            print(date,end=' - ')
        except Exception as e:
            print(e)

if __name__ == "__main__":
    load_and_generatecsv(['2020-04-04','2020-04-03'])
