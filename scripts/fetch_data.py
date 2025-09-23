# script_fetch_selected_indicators.py

import requests
import pandas as pd
import os

BASE_URL = "https://ghoapi.azureedge.net/api/"

def fetch_indicator_data(indicator_code):
    url = BASE_URL + indicator_code
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    df = pd.json_normalize(data['value'])
    return df

if __name__ == "__main__":
    os.makedirs("data/row", exist_ok=True)

    selected_indicators = [
        "MDG_0000000007", "who_AIR_60" # Exempel: HIV prevalence among adults 15–49          # Exempel: Suicide mortality rate
    ]

    for code in selected_indicators:
        df = fetch_indicator_data(code)
        filename = os.path.join("data", "raw", f"who_{code}.csv")
        df.to_csv(filename, index=False)
        print(f"Sparade {filename} ({len(df)} rader)")
