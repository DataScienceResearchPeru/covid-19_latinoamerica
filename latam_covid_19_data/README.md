# LATAM COVID-19 Data Repository

Folders:

- Daily Report
- Per Patient
- Templates
- Time Series

# Daily reports

Are located in `daily_reports/` with filenames in format `YYYY-MM-DD.csv`.

## Columns

- `ISO 3166-2 Code`: Código ISO de cada país. (Revisar este [archivo](https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/blob/master/utils/iso3312_latinamerica.csv)) Sirve para obtener más data del país como latitud, longitud y proximamente referenciar con otras bases de datos variables climáticas, económicas, demográficas.
- `Country`
- `Subdivision`: Subdivision of the country
- `Last Update`: (WARNING, internal use, don't pay attention)
- `Confirmed`: Covid-19 confirmed cases
- `Deaths`: Covid-19 deaths cases
- `Recovered`: Covid-19 recovered cases

# Country reports

(Warning: we're waiting official data, but there's data for few countries)
Are located in `per_country/` with filenames in format `CC.csv` where `CC` is two first letters of the Country Code following ISO_3166-2 alfa-2. (You can find them in [Wikipedia](https://en.wikipedia.org/wiki/ISO_3166-1))

## Columns

- `ISO 3166-2 Code`: Código ISO de cada país. (Revisar este [archivo](https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/blob/master/utils/iso3312_latinamerica.csv)) Sirve para obtener más data del país como latitud, longitud y proximamente referenciar con otras bases de datos variables climáticas, económicas, demográficas.
- `Country`
- `Subdivision`: Subdivision of the country
- `Age`
- `Gender`
- `First Symptoms`
- `Date Confirmed`
- `Hospital code`

# Templates

[]

## Files

[]

# Time series

It is the compilation of all daily reports in one file for easy access. Acumulative data. Files: `time_series_confirmed.csv` & `time_series_deaths.csv` & `time_series_recovered.csv`

## Columns

- `ISO 3166-2 Code`: Código ISO de cada país. (Revisar este [archivo](https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/blob/master/utils/iso3312_latinamerica.csv)) Sirve para obtener más data del país como latitud, longitud y proximamente referenciar con otras bases de datos variables climáticas, económicas, demográficas.
- `Country`
- `Subdivision`: Subdivision of the country
- `Dates`: Each date as a column like `2020-02-28`
