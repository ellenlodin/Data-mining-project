# view_data.py
import pandas as pd
import os

def view_data(filename, n=5):
    filepath = os.path.join("data", "row", filename)
    if not os.path.exists(filepath):
        print(f"Filen {filepath} finns inte. Kontrollera namnet.")
        return
    df = pd.read_csv(filepath)
    print(f"\nVisar de första {n} raderna från {filepath}:\n")
    print(df.head(n))

if __name__ == "__main__":
    # Ändra detta till den fil du vill inspektera
    file_to_view = "who_WHS10_4.csv"
    
    # Antal rader att visa (default = 5)
    view_data(file_to_view, n=10)
