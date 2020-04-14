# LATAM COVID-19 Data Repository

# Time series

It is the compilation of all daily reports in one file for easy access. 
It contains the same columns as the daily reports except the `Last Update` column is renamed to `Date`, so it may contain multiple rows for each country.
Is a single file `latam_covid_19_time_series.csv` in the root of this folder.


# Daily reports
Are located in `daily_reports/` with filenames in format `YYYY-MM-DD.csv`.

## Columns

-   `ISO 3166-2 Code`: Código ISO de cada país. (Revisar este [archivo](https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/blob/master/utils/iso3312_latinamerica.csv)) Sirve para obtener más data del país como latitud, longitud y proximamente referenciar con otras bases de datos variables climáticas, económicas, demográficas.
-   `Country`: Ubicación geográfica nivel 1 (país)
-   `Subdivision`: Ubicación geográfica nivel 2
-   `Last Update`: Fecha en la cuál se modifica la fila
-   `Confirmed`: Número de contagiados
-   `Deaths`: Número de pacientes fallecidos
-   `Recovered`: Número de pacientes recuperados


# Country reports
Are located in `per_country/` with filenames in format `CC.csv` with CC being the 2 letter Country Code following ISO_3166-1 alfa-2.

## Columns

-   `ISO 3166-2 Code`: Código ISO de cada país. (Revisar este [archivo](https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/blob/master/utils/iso3312_latinamerica.csv)) Sirve para obtener más data del país como latitud, longitud y proximamente referenciar con otras bases de datos variables climáticas, económicas, demográficas.
-   `Country`: Ubicación geográfica nivel 1 (país)
-   `Subdivision`: Ubicación geográfica nivel 2
-   `Age`
-   `Gender`
-   `First Symptoms`
-   `Date Confirmed`
-   `Hospital code`


## Disclaimer
This GitHub repo and its contents herein, including all data, mapping, and analysis is provided to the public strictly for educational and academic research purposes. Reliance on the Website for medical guidance or use of the Website in commerce is strictly prohibited.
