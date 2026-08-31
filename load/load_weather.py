import psycopg2
import dotenv
import os
import json
dotenv.load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

def load_weather_data(json_file="raw_weather_data.json"):

    with open(json_file, "r", encoding='UTF-8') as f:
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

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_weather_data("data/raw/raw_weather_data_for_2026-08-26.json")