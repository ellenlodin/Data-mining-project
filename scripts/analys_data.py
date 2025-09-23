# findings.py
import pandas as pd
import os
import matplotlib.pyplot as plt

def analyze_findings(filename):
    analysed_path = os.path.join("data", "clean", filename)
    if not os.path.exists(analysed_path):
        print(f"Filen {analysed_path} finns inte. Se till att du har kört analyze_data.py först.")
        return
    
    # Läs in filen
    df = pd.read_csv(analysed_path)
    
    # ==============================
    # 1. Top 10 länder högst/lägst PM25_mean
    # ==============================
    country_means = df.groupby("SpatialDim")["PM25_mean"].mean().sort_values(ascending=False)
    top10 = country_means.head(10)
    bottom10 = country_means.tail(10)
    
    print("\n🌍 Top 10 länder med högst genomsnittlig PM2.5:")
    print(top10)
    
    print("\n🌍 Top 10 länder med lägst genomsnittlig PM2.5:")
    print(bottom10)
    
    # ==============================
    # 2. Rankning av världsdelar
    # ==============================
    region_means = df.groupby("ParentLocationCode")["PM25_mean"].mean().sort_values(ascending=False)
    
    print("\n🌎 Ranking av världsdelar efter PM2.5 (högst → lägst):")
    print(region_means)
    
    # ==============================
    # 3. Top 10 största förändringar (ökning/minskning)
    # ==============================
    # Ta första och sista värdet per land
    country_change = (
        df.groupby("SpatialDim")
        .apply(lambda x: x.sort_values("TimeDim").iloc[-1]["PM25_mean"] - x.sort_values("TimeDim").iloc[0]["PM25_mean"])
        .sort_values(ascending=False)
    )
    
    top10_increase = country_change.head(10)
    top10_decrease = country_change.tail(10)
    
    print("\n📈 Top 10 länder med störst ÖKNING i PM2.5:")
    print(top10_increase)
    
    print("\n📉 Top 10 länder med störst MINSKNING i PM2.5:")
    print(top10_decrease)
    
    # ==============================
    # 4. Graf över utvecklingen
    # ==============================
    plt.figure(figsize=(14, 8))
    for country, sub_df in df.groupby("SpatialDim"):
        plt.plot(sub_df["TimeDim"], sub_df["PM25_mean"], label=country, alpha=0.4)
    
    plt.title("Utveckling av PM2.5 (alla länder)")
    plt.xlabel("År")
    plt.ylabel("PM2.5 (µg/m³, population-weighted mean)")
    plt.grid(True, alpha=0.3)
    plt.legend(ncol=6, fontsize=6, frameon=False)
    
    # Skapa findings-mapp om den inte finns
    findings_dir = os.path.join("data", "findings")
    os.makedirs(findings_dir, exist_ok=True)
    
    plot_path = os.path.join(findings_dir, "PM25_trends_all_countries.png")
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close()
    
    print(f"\n📊 Graf sparad till: {plot_path}")

if __name__ == "__main__":
    # Ändra till din analyserade fil
    file_to_analyze = "sorted_cleaned_who_SDGPM25.csv"
    analyze_findings(file_to_analyze)
