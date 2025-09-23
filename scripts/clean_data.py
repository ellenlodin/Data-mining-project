# analyze_data.py
import pandas as pd
import os

def analyze_and_sort(filename):
    processed_path = os.path.join("data", "processed", filename)
    if not os.path.exists(processed_path):
        print(f"Filen {processed_path} finns inte. Se till att du har kört view_data.py först.")
        return
    
    # Läs in filen
    df = pd.read_csv(processed_path)

    # 🔹 Ta bort rader där SpatialDim = UNKNOWN
    df = df[df["SpatialDim"] != "UNKNOWN"]
    
    # Sortera efter land (SpatialDim) och år (TimeDim)
    df_sorted = df.sort_values(by=["SpatialDim", "TimeDim"]).reset_index(drop=True)
    
    # 🔹 Lägg till MinMax-skalad kolumn (0–1) på PM25_mean
    min_val = df_sorted["PM25_mean"].min()
    max_val = df_sorted["PM25_mean"].max()
    df_sorted["PM25_scaled_0_1"] = (df_sorted["PM25_mean"] - min_val) / (max_val - min_val)
    
    # Skapa analysed-mapp om den inte finns
    analysed_dir = os.path.join("data", "clean")
    os.makedirs(analysed_dir, exist_ok=True)
    
    # Visa lite info
    print(f"\n✅ Filen {filename} inläst, rensad på UNKNOWN, sorterad efter land och år, och MinMax-skalad (0–1).")
    print(f"Antal unika länder: {df_sorted['SpatialDim'].nunique()}")
    print(f"Exempel på länder: {df_sorted['SpatialDim'].unique()[:10]}\n")
    print("Förhandsvisning:\n")
    print(df_sorted.head(10))
    
    # Spara en sorterad version
    sorted_path = os.path.join(analysed_dir, f"sorted_{filename}")
    df_sorted.to_csv(sorted_path, index=False)
    print(f"\n📂 Sorterad & skalad data sparad till: {sorted_path}")

if __name__ == "__main__":
    # Ändra till din rensade fil
    file_to_analyze = "cleaned_who_SDGPM25.csv"
    analyze_and_sort(file_to_analyze)
