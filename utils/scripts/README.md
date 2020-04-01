## Utilities

### mergeFiles.py
Very simple utility to merge all csv files in a directory into a single csv and adds a "Date" column based a date extracted from the filename.

The code below creates a file called "merged.csv".

`
python mergeFiles.py --path "../covid-19_latinoamerica/latam_covid_19_data/latam_covid_19_daily_reports/" --output "merged"
`

