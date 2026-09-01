import psycopg2
import dotenv
import os
import json
dotenv.load_dotenv()

DB_CONFIG = {
    "host": os.getenv("WAREHOUSE_HOST"),
    "port": os.getenv("WAREHOUSE_PORT"),
    "dbname": os.getenv("WAREHOUSE_DB"),
    "user": os.getenv("WAREHOUSE_USER"),
    "password": os.getenv("WAREHOUSE_PASSWORD"),
}

def load_weather_data(run_date):

    with open(os.path.join("data/raw", f"raw_weather_data_for_{run_date}.json"), "r", encoding='UTF-8') as f:
        data = json.load(f)

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_weather_data (
    id serial PRIMARY KEY,
    obs_date DATE UNIQUE,
    max_temp NUMERIC(10, 2),
    min_temp NUMERIC(10, 2),
    precipitation_sum NUMERIC(10, 2),
    loaded_at TIMESTAMPTZ DEFAULT NOW()
  )
 """)

    daily = data["daily"]
    records = zip(
        daily["time"],
        daily["temperature_2m_max"],
        daily["temperature_2m_min"],
        daily["precipitation_sum"],
    )
    #Zip takes several variables and pairs up their elements by position

    for obs_date, max_temp, min_temp, precipitation_sum in records:
        cursor.execute("""
        INSERT INTO raw_weather_data(obs_date, max_temp, min_temp, precipitation_sum)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (obs_date) DO UPDATE SET  
            max_temp = EXCLUDED.max_temp,
            min_temp = EXCLUDED.min_temp,
            precipitation_sum = EXCLUDED.precipitation_sum,
            loaded_at = NOW()
        """, (obs_date, max_temp, min_temp, precipitation_sum))

        #ON CONFLICT (obs_date) DO UPDATE SET makes it so that the unique row is updated instead of throwing an error
        #EXCLUDED is a special Postgres pseudo-table holding the row that failed to insert
        #loaded_at = NOW() stamps with current time


    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_weather_data("2026-08-26")