## Utilities

### mergeFiles.py
Very simple utility to merge all csv files in a directory into a single csv and adds a "Date" column based a date extracted from the filename.


The code below creates a file called "merged.csv".

`
python mergeFiles.py --path "../covid-19_latinoamerica/latam_covid_19_data/latam_covid_19_daily_reports/" --output "merged"
`

#### Dependencies:
pandas, numpy


<!-- LICENSE -->

## License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Latin America Covid-19 Data Repository' Scripts</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Data Science Research Peru</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.