# Ref --> https://github.com/CSSEGISandData/COVID-19
BASE = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/"

# API
API_URL = "https://covid19data-jk.herokuapp.com/api/ecowas"

# Local CSV
GEO_DATA = 'dashboard/data/ecowas-gps.csv'

# Time series data
CONFIRMED = BASE+"csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
RECOVERED = BASE+"csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
DEATHS = BASE+"csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

KPIs = [CONFIRMED, RECOVERED, DEATHS]


# Aggregated data
URL = BASE+"csse_covid_19_daily_reports/{}.csv"


# ECOWAS countries list
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


# Columns to remove
REMOVED = ['FIPS', 'Admin2', 'Province_State', 'Combined_Key', 'Last_Update', 'Lat', 'Long_', 'Incident_Rate', 'Case_Fatality_Ratio']
