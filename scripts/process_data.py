# view_data.py
import pandas as pd
import os

def view_data(filename, n=5):
    raw_path = os.path.join("data", "raw", filename)
    if not os.path.exists(raw_path):
        print(f"Filen {raw_path} finns inte. Kontrollera namnet.")
        return
    
    # Läs in filen
    df = pd.read_csv(raw_path)
    
    # Behåll bara de viktiga kolumnerna
    important_cols = [
        "SpatialDim", "ParentLocationCode", 
        "TimeDim", "Dim1", "NumericValue", "Low", "High"
    ]
    df = df[important_cols]

    # Filtrera fram endast totalvärden för länderna
    df = df[df["Dim1"] == "RESIDENCEAREATYPE_TOTL"]

    # Ta bort Dim1-kolumnen eftersom den inte längre behövs
    df = df.drop(columns=["Dim1"])

    # Byt namn på kolumner så de matchar WHO:s beskrivning
    df = df.rename(columns={
        "NumericValue": "PM25_mean",
        "Low": "PM25_lower_CI",
        "High": "PM25_upper_CI"
    })
    
    # Skapa processed-mapp om den inte finns
    processed_dir = os.path.join("data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    
    # Spara rensad version
    processed_path = os.path.join(processed_dir, f"cleaned_{filename}")
    df.to_csv(processed_path, index=False)
    
    print(f"✅ Rensad data (endast TOTAL och utan Dim1) sparad till: {processed_path}\n")
    print(f"Visar de första {n} raderna:\n")
    print(df.head(n))

if __name__ == "__main__":
    # Ändra detta till den fil du vill inspektera
    file_to_view = "who_SDGPM25.csv"
    
    # Antal rader att visa (default = 5)
    view_data(file_to_view, n=10)
