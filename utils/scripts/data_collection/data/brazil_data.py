import pandas as pd
import sys
import os

init_date = pd.to_datetime("2020/03/25", format="%Y/%m/%d")

confirmed_url = "https://raw.githubusercontent.com/elhenrico/covid19-Brazil-timeseries/master/confirmed-cases.csv"
deaths_url = "https://raw.githubusercontent.com/elhenrico/covid19-Brazil-timeseries/master/deaths.csv"
dsrp_github="https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/daily_reports/2020-03-08.csv"


confirmed = pd.read_csv(confirmed_url)
deaths = pd.read_csv(deaths_url)
compare = pd.read_csv(dsrp_github)

brazil_compare = compare[compare['Country']=="Brazil"]

string_a = "áéíóúäëïöüâêîôûã"  # character to be replaced
string_b = "aeiouaeiouaeioua"  # character to replace with

def remove_tildes(string):
    for index, tilde in enumerate(string_a):
        string = string.replace(tilde, string_b[index])
    return string


confirmed.iloc[:,0] = confirmed.iloc[:,0].apply(remove_tildes)
deaths.iloc[:,0] = deaths.iloc[:,0].apply(remove_tildes)

confirmed = confirmed.rename(columns={"Unnamed: 0": "Subdivision", "Unnamed: 1": "Code"})
deaths = deaths.rename(columns={"Unnamed: 0": "Subdivision", "Unnamed: 1": "Code"})

sub_brazil = sorted(brazil_compare.Subdivision.unique())
sub_repo = sorted(confirmed.iloc[:,0].unique())

other_subdivisions = list(set(sub_repo) - (set(sub_brazil)))  # Subdivisiones other than those listed in the main repo

confirmed = confirmed[~confirmed.Subdivision.isin(other_subdivisions)].sort_values("Subdivision")
deaths = deaths[~deaths.Subdivision.isin(other_subdivisions)].sort_values("Subdivision")

del confirmed["Code"]
del deaths["Code"]

confirmed_columns = confirmed.columns[1:]
deaths_columns = deaths.columns[1:]

columns_order = ["ISO 3166-2 Code", "Country", "Subdivision", "Last Update", "Confirmed", "Deaths", "Recovered"]

for column in confirmed_columns:
    day, month = map(int, column.split("/"))
    date = f"{2020}-{month:02}-{day:02}"

    actual_date = pd.to_datetime(date, format="%Y/%m/%d")

    if actual_date < init_date:
        print("Skipping:", actual_date)
        continue

    daily_report_path = f"latam_covid_19_data/daily_reports/{date}.csv"
    daily_report = pd.read_csv(daily_report_path)

    brazil = daily_report[daily_report.Country=="Brazil"]
    brazil_index = daily_report[daily_report.Country=="Brazil"].index
    
    del brazil["Deaths"]
    del brazil["Confirmed"]

    confirmed_subset = confirmed.loc[:, ["Subdivision", column]]
    deaths_subset = deaths.loc[:, ["Subdivision", column]]
    confirmed_subset = confirmed_subset.rename(columns={column: "Confirmed"})
    deaths_subset = deaths_subset.rename(columns={column: "Deaths"})
    dc = pd.merge(confirmed_subset, deaths_subset, how="left", on="Subdivision")  # Deaths confirmed
    final = pd.merge(brazil, dc, how="left", on="Subdivision").fillna(0)
    final = final[columns_order].set_index(brazil_index)

    final["Last Update"] = date
    
    daily_report.update(final)

    daily_report.Deaths = daily_report.Deaths.fillna(0)
    daily_report.Confirmed = daily_report.Confirmed.fillna(0)
    daily_report.Recovered = daily_report.Recovered.fillna(0)

    daily_report.Deaths = daily_report.Deaths.astype("int64")
    daily_report.Confirmed = daily_report.Confirmed.astype("int64")
    daily_report.Recovered = daily_report.Recovered.astype("int64")

    path_data=f"utils/scripts/data_collection/data/brazil_temporal/{date}.csv"
    print(daily_report[daily_report.Country=="Brazil"])
    daily_report.to_csv(path_data, index=False)