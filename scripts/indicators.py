# script_fetch_all_indicators.py
import requests
import pandas as pd
import os

BASE_URL = "https://ghoapi.azureedge.net/api/"

def get_all_indicators():
    url = BASE_URL + "Indicator"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    df = pd.json_normalize(data['value'])
    return df

if __name__ == "__main__":
    # Skapa mappen data/raw om den inte finns
    os.makedirs("data/raw", exist_ok=True)

    indicators = get_all_indicators()
    filepath = os.path.join("data", "raw", "who_all_indicators.csv")
    indicators.to_csv(filepath, index=False)
    print(f"Sparade {len(indicators)} indikatorer till {filepath}")
