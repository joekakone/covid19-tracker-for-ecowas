# coding : utf-8

import datetime
import pandas as pd


# ecowas
COUNTRIES = [
    'Togo',
    'Benin',
    'Ghana',
    'Burkina Faso',
    'Niger',
    'Nigeria',
    'Senegal',
    'Mali',
    'Guinea-Bissau',
    'Guinea',
    'Gambia',
    'Cabo Verde',
    'Liberia',
    'Sierra Leone',
    'Cote d\'Ivoire'
]
# columns
REMOVED = ['FIPS', 'Admin2', 'Province_State', 'Combined_Key', 'Last_Update', 'Lat', 'Long_', 'Incident_Rate', 'Case_Fatality_Ratio']
# ref --> https://github.com/CSSEGISandData/COVID-19
URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}.csv'


def get_date():
    # today date
    now = datetime.datetime.now()

    day = now.day # day
    if (day - 1) != 0:
        day -= 1
    if len(str(day))==1:
        day = '0'+str(day)
    month = now.month
    if len(str(month))==1:
        month = '0'+str(month)
    year = str(now.year)
    today = f'{month}-{day}-{year}'
    update_date = f'{day}-{month}-{year}'
    format_date = f'{year}-{month}-{day}'
    
    return today, update_date, format_date

def get_data(url=URL):
    today, update_date, format_date = get_date()
    full_url = url.format(today) # build dataset url

    dt = pd.read_csv(full_url)
    dt_ecowas = dt[dt['Country_Region'].isin(COUNTRIES)]
    dt_ecowas = dt_ecowas.drop(REMOVED, axis=1)
    dt_ecowas = dt_ecowas.reset_index().drop(['index'], axis=1)


    dt_ecowas.to_csv(f'dashboard/data/{format_date}-ecowas-covid19.csv', index=False)

    return dt_ecowas, update_date
