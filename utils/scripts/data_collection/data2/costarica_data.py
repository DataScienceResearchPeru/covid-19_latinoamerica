import pandas as pd 
import requests
import json
import sys
import os


def load_and_generatecsv(list_date_list):
    api_url = "https://coronaviruscr.com/api/reports"

    root_relative = '../../'

    json_data = requests.get(api_url).content.decode()

    parsed = json.loads(json_data)["data"]

    for entry in parsed:
        date = entry["date"]
        
        locations = entry["byLocation"]
        print(date,end=' - ')
        confirmed = pd.DataFrame(
                    zip(locations.keys(), locations.values()),
                    columns=["Subdivision", "Confirmed"]
                )
        
        confirmed.Subdivision = confirmed.Subdivision.str.title()
        confirmed.Subdivision = confirmed.Subdivision.str.replace("Sanjose", "San Jose")
        confirmed = confirmed[confirmed.Subdivision!="Unknown"]
        confirmed = confirmed.sort_values("Subdivision")
        
        #print(confirmed)
        
        daily_report_file = os.path.abspath(root_relative+f"latam_covid_19_data/daily_reports/{date}.csv")
        #print(f"Opening {daily_report_file}")
        daily_report = pd.read_csv(daily_report_file, engine='python')
        cr = daily_report[daily_report.Country=="Costa Rica"]
        cr_index = cr.index
        del cr["Confirmed"]
        cr["Last Update"] = date
        ncr = pd.merge(cr, confirmed, how="left", on="Subdivision").set_index(cr_index)
        
        daily_report.update(ncr)
        
        
        daily_report.Deaths = daily_report.Deaths.fillna(0)
        daily_report.Confirmed = daily_report.Confirmed.fillna(0)
        daily_report.Recovered = daily_report.Recovered.fillna(0)

        daily_report.Deaths = daily_report.Deaths.astype("int64")
        daily_report.Confirmed = daily_report.Confirmed.astype("int64")
        daily_report.Recovered = daily_report.Recovered.astype("int64")
        
        #print(daily_report[daily_report.Country=="Costa Rica"])
        # os.system("git pull")
        daily_report=daily_report[daily_report.Country=="Costa Rica"]
        
        daily_report.to_csv(os.path.abspath(root_relative+f"utils/scripts/data_collection/data2/costarica_temporal/{date}.csv"), index=False)
        # os.system(f"git add {daily_report_file}")
        # os.system("git commit -m 'Update Costa rica'")

        
if __name__ == "__main__":
    load_and_generatecsv(['2020-05-17','2020-05-18'])
    