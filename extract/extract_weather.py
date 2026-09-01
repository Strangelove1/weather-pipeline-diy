import requests
import json
import os


#"latitude":52.23009,"longitude":21.017075 - example coordinates for Warsaw, Poland

def get_weather_data(latitude, longitude, daily=("temperature_2m_max,temperature_2m_min,precipitation_sum"), timezone="auto", past_days=1, forecast_days=1):

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily={daily}&timezone={timezone}&past_days={past_days}&forecast_days={forecast_days}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None
        
def run_weather_report(report_date):

 weather_data = get_weather_data(52.23009, 21.017075)

 os.makedirs("data/raw", exist_ok=True)
 target = os.path.join("data/raw", f"raw_weather_data_for_{report_date}.json") 

 with open(target, "w", encoding="utf-8") as f:

    json.dump(weather_data, f, ensure_ascii=False, indent=2)

 print(f"Downloaded  {len(weather_data)} records from weather API")

if __name__ == "__main__":
    run_weather_report("2026-08-26")