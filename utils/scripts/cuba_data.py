import pandas as pd 
import requests
import json
import os

api_subdivision_url = "https://covid19cuba-api.herokuapp.com/provincias_text"
api_summary_url = "https://covid19cuba-api.herokuapp.com/summary"


string_a = "áéíóúäëïöüâêîôûã"  # character to be replaced
string_b = "aeiouaeiouaeioua"  # character to replace with
string_a += string_a.upper()
string_b += string_b.upper()

def remove_tildes(string):
    for index, tilde in enumerate(string_a):
        string = string.replace(tilde, string_b[index])
    return string


subdivisions_content = requests.get(api_subdivision_url).content.decode()
summary_content = requests.get(api_summary_url).content.decode()

subdivisions_json = json.loads(subdivisions_content)
summary_json = json.loads(summary_content)

print(subdivisions_content)
print(summary_content)

confirmed = pd.DataFrame(subdivisions_json["provincias"], columns=["Subdivision", "Confirmed"])
confirmed = confirmed[~confirmed.Subdivision.isnull()]
confirmed.Subdivision = confirmed.Subdivision.apply(remove_tildes)

date = summary_json["Updated"].replace("/", "-")

daily_report_file = f"../../latam_covid_19_data/latam_covid_19_daily_reports/{date}.csv"

daily_report = pd.read_csv(daily_report_file)
cuba = daily_report[daily_report.Country=="Cuba"]
cuba_index = cuba.index
cuba["Last Update"] = date
cuba.Subdivision = cuba.Subdivision.apply(remove_tildes)


del cuba["Confirmed"]

cuba = pd.merge(cuba, confirmed, how="left", on="Subdivision").set_index(cuba_index)

daily_report.update(cuba)

daily_report.Deaths = daily_report.Deaths.fillna(0)
daily_report.Confirmed = daily_report.Confirmed.fillna(0)
daily_report.Recovered = daily_report.Recovered.fillna(0)

daily_report.Deaths = daily_report.Deaths.astype("int64")
daily_report.Confirmed = daily_report.Confirmed.astype("int64")
daily_report.Recovered = daily_report.Recovered.astype("int64")

print(daily_report[daily_report.Country=="Cuba"])

os.system("git pull")
daily_report.to_csv(daily_report_file, index=False)
os.system(f"git add {daily_report_file}")
os.system("git commit -m 'Update Cuba'")