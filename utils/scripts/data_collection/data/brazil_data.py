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
    init_date = pd.to_datetime("2020/03/25", format="%Y/%m/%d")

    confirmed_url = "https://raw.githubusercontent.com/elhenrico/covid19-Brazil-timeseries/master/confirmed-cases.csv"
    deaths_url = "https://raw.githubusercontent.com/elhenrico/covid19-Brazil-timeseries/master/deaths.csv"
    dsrp_github = "latam_covid_19_data/templates/daily_reports.csv"


    confirmed = pd.read_csv(confirmed_url)
    deaths = pd.read_csv(deaths_url)
    compare = pd.read_csv(dsrp_github)

    brazil_compare = compare[compare['Country'] == "Brazil"]


    confirmed.iloc[:, 0] = confirmed.iloc[:, 0].apply(remove_tildes)
    deaths.iloc[:, 0] = deaths.iloc[:, 0].apply(remove_tildes)

    confirmed = confirmed.rename(
        columns={"Unnamed: 0": "Subdivision", "Unnamed: 1": "Code"})
    deaths = deaths.rename(
        columns={"Unnamed: 0": "Subdivision", "Unnamed: 1": "Code"})

    sub_brazil = sorted(brazil_compare.Subdivision.unique())
    sub_repo = sorted(confirmed.iloc[:, 0].unique())

    # Subdivisiones other than those listed in the main repo
    other_subdivisions = list(set(sub_repo) - (set(sub_brazil)))

    confirmed = confirmed[~confirmed.Subdivision.isin(
        other_subdivisions)].sort_values("Subdivision")
    deaths = deaths[~deaths.Subdivision.isin(
        other_subdivisions)].sort_values("Subdivision")

    del confirmed["Code"]
    del deaths["Code"]

    confirmed_columns = confirmed.columns[1:]
    deaths_columns = deaths.columns[1:]

    columns_order = ["ISO 3166-2 Code", "Country", "Subdivision",
                    "Last Update", "Confirmed", "Deaths", "Recovered"]

    for column in confirmed_columns:
        day, month = map(int, column.split("/"))
        date = f"{2020}-{month:02}-{day:02}"

        actual_date = pd.to_datetime(date, format="%Y/%m/%d")

        if actual_date < init_date:
            print("Skipping:", actual_date)
            continue

        daily_report_path = f"latam_covid_19_data/daily_reports/{date}.csv"
        daily_report = pd.read_csv(daily_report_path)

        brazil = daily_report[daily_report.Country == "Brazil"]
        brazil_index = daily_report[daily_report.Country == "Brazil"].index

        del brazil["Deaths"]
        del brazil["Confirmed"]

        confirmed_subset = confirmed.loc[:, ["Subdivision", column]]
        deaths_subset = deaths.loc[:, ["Subdivision", column]]
        confirmed_subset = confirmed_subset.rename(columns={column: "Confirmed"})
        deaths_subset = deaths_subset.rename(columns={column: "Deaths"})
        dc = pd.merge(confirmed_subset, deaths_subset, how="left",
                    on="Subdivision")  # Deaths confirmed
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

        path_data = f"utils/scripts/data_collection/data/brazil_temporal/{date}.csv"
        # print(daily_report[daily_report.Country=="Brazil"])
        daily_report = daily_report[daily_report.Country == "Brazil"]
        daily_report.to_csv(path_data, index=False)



if __name__ == "__main__":
    load_and_generatecsv(['2020-05-22', '2020-05-21', '2020-05-20', '2020-05-19', '2020-05-18', 
    '2020-05-17', '2020-05-16', '2020-05-15', '2020-05-14', '2020-05-13', '2020-05-12', '2020-05-11',
     '2020-05-10', '2020-05-09', '2020-05-08', '2020-05-07', '2020-05-06', '2020-05-05', '2020-05-04', 
     '2020-05-03', '2020-05-02', '2020-05-01', '2020-04-30', '2020-04-29', '2020-04-28', '2020-04-27', '2020-04-26', 
     '2020-04-25', '2020-04-24', '2020-04-23', '2020-04-22', '2020-04-21', '2020-04-20', '2020-04-19', '2020-04-18',
      '2020-04-17', '2020-04-16', '2020-04-15', '2020-04-14', '2020-04-13', '2020-04-12', '2020-04-11', '2020-04-10',
       '2020-04-09', '2020-04-08', '2020-04-07', '2020-04-06', '2020-04-05', '2020-04-04', '2020-04-03'])
