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
    
    # Sortera efter land (SpatialDim) och år (TimeDim)
    df_sorted = df.sort_values(by=["SpatialDim", "TimeDim"]).reset_index(drop=True)
    
    # Skapa analysed-mapp om den inte finns
    analysed_dir = os.path.join("data", "analysed")
    os.makedirs(analysed_dir, exist_ok=True)
    
    # Visa lite info
    print(f"\n✅ Filen {filename} inläst och sorterad efter land och år.")
    print(f"Antal unika länder: {df_sorted['SpatialDim'].nunique()}")
    print(f"Exempel på länder: {df_sorted['SpatialDim'].unique()[:10]}\n")
    print("Förhandsvisning:\n")
    print(df_sorted.head(10))
    
    # Spara en sorterad version
    sorted_path = os.path.join(analysed_dir, f"sorted_{filename}")
    df_sorted.to_csv(sorted_path, index=False)
    print(f"\n📂 Sorterad data sparad till: {sorted_path}")

if __name__ == "__main__":
    # Ändra till din rensade fil
    file_to_analyze = "cleaned_who_SDGPM25.csv"
    analyze_and_sort(file_to_analyze)
