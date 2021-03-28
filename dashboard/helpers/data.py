# coding : utf-8

import datetime
import pandas as pd


# ecowas
COUNTRIES = [
    "Togo",
    "Benin",
    "Ghana",
    "Burkina Faso",
    "Niger",
    "Nigeria",
    "Senegal",
    "Mali",
    "Guinea-Bissau",
    "Guinea",
    "Gambia",
    "Cabo Verde",
    "Liberia",
    "Sierra Leone",
    "Cote d\'Ivoire"
]
# columns
REMOVED = ["FIPS", "Admin2", "Province_State", "Combined_Key", "Last_Update", "Incident_Rate", "Case_Fatality_Ratio"]
# ref --> https://github.com/CSSEGISandData/COVID-19
URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}.csv"


def get_date(current_day):
    day = current_day.day
    if len(str(day))==1:
        day = "0"+str(day)

    month = current_day.month
    if len(str(month))==1:
        month = "0"+str(month)

    year = str(current_day.year)
    today = f"{month}-{day}-{year}"
    update_date = f"{day}-{month}-{year}"
    format_date = f"{year}-{month}-{day}"
    
    return today, update_date, format_date

def get_data(url=URL):
    try: # today date
        now = datetime.datetime.now()
        format_date, human_date, save_date = get_date(now)
        dt = pd.read_csv(url.format(format_date))
    except: # yesterday
        yesterday = datetime.datetime.now() - datetime.timedelta(1)
        format_date, human_date, save_date = get_date(yesterday)
        dt = pd.read_csv(url.format(format_date))
    dt_ecowas = dt[dt["Country_Region"].isin(COUNTRIES)]
    dt_ecowas = dt_ecowas.drop(REMOVED, axis=1)
    dt_ecowas = dt_ecowas.reset_index().drop(["index"], axis=1)
    # Compute bulles size on the map
    quartiles = [dt_ecowas["Confirmed"].quantile(q) for q in [.25, .5, .75, 1]]
    def get_size(v):
        if v < quartiles[0]:
            return 1
        if v < quartiles[1]:
            return 2
        if v < quartiles[2]:
            return 3
        if v <= quartiles[3]:
            return 4
    dt_ecowas["MapSize"] = dt_ecowas["Confirmed"].apply(get_size)

    dt_ecowas.to_csv(f"dashboard/data/{save_date}-ecowas-covid19.csv", index=False)

    return dt_ecowas, human_date
