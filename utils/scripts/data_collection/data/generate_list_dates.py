import os
import datetime

path='latam_covid_19_data/daily_reports'
# Generate dates from files existing
date_list_csv = []
path, dirs, files = next(os.walk(path))
numero_archivos = len(files)
# print('There is {} files on the path and one is README. We iterate {} times...'.format(
#     numero_archivos, numero_archivos-1))
# dates
base = (datetime.datetime.today()).date()
numdays = numero_archivos-1
date_list_csv = [str(base - datetime.timedelta(days=x))+str('.csv')
                    for x in range(numdays)]
# print('Adding {} dates in a list...'.format(len(date_list_csv)))
date_list = []
for d in date_list_csv:
    date_list.append(d[:-4])
print("List of dates:", date_list)


print( date_list)