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
CONFIRMED = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
RECOVERED = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
DEATHS = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

def query():
	print(CONFIRMED)
	confirmed = pd.read_csv(CONFIRMED)
	print(RECOVERED)
	recovered = pd.read_csv(RECOVERED)
	print(DEATHS)
	deaths = pd.read_csv(DEATHS)
	confirmed = confirmed.drop(["Province/State", "Lat", "Long"], axis=1)
	recovered = recovered.drop(["Province/State", "Lat", "Long"], axis=1)
	deaths = deaths.drop(["Province/State", "Lat", "Long"], axis=1)


	# CONFIRMED
	# Unpivot date columns
	confirmed_melt = pd.melt(confirmed, id_vars=["Country/Region"], value_vars=list(confirmed.columns)[1:])
	# Rename columns
	confirmed_melt.columns = ["Country_Region", "Date", "Confirmed"]
	# Ensure date have appropriate format
	confirmed_melt["Date"] = pd.to_datetime(confirmed_melt["Date"])
	# Sort by Country and Date
	confirmed_melt = confirmed_melt.sort_values(by=["Country_Region", "Date"])
	confirmed_melt = confirmed_melt[confirmed_melt["Country_Region"].isin(COUNTRIES)]
	# del confirmed

	# RECOVERED
	# Unpivot date columns
	recovered_melt = pd.melt(recovered, id_vars=["Country/Region"], value_vars=list(confirmed.columns)[1:])
	# Rename columns
	recovered_melt.columns = ["Country_Region", "Date", "Recovered"]
	# Ensure date have appropriate format
	recovered_melt["Date"] = pd.to_datetime(recovered_melt["Date"])
	# Sort by Country and Date
	recovered_melt = recovered_melt.sort_values(by=["Country_Region", "Date"])
	recovered_melt = recovered_melt[recovered_melt["Country_Region"].isin(COUNTRIES)]
	# del recovered

	# DEATHS
	# Unpivot date columns
	deaths_melt = pd.melt(deaths, id_vars=["Country/Region"], value_vars=list(confirmed.columns)[1:])
	# Rename columns
	deaths_melt.columns = ["Country_Region", "Date", "Deaths"]
	# Ensure date have appropriate format
	deaths_melt["Date"] = pd.to_datetime(deaths_melt["Date"])
	# Sort by Country and Date
	deaths_melt = deaths_melt.sort_values(by=["Country_Region", "Date"])
	deaths_melt = deaths_melt[deaths_melt["Country_Region"].isin(COUNTRIES)]
	# del deaths

	# MERGE
	print("Merging tables...")
	data = confirmed_melt.merge(recovered_melt, how='inner', on=["Country_Region", "Date"])
	data = data.merge(deaths_melt, how='inner', on=["Country_Region", "Date"])

	# ACTIVE
	print("Compute active cases...")
	data["Active"] = data["Confirmed"] - (data["Recovered"] + data["Deaths"])
	data.to_csv("dashboard/data/covid19.csv")

	# AGREGATION
	print("Agregate data...")
	data_agregated = data.groupby("Country_Region").max()
	data_agregated = data_agregated.reset_index()

	return data_agregated

