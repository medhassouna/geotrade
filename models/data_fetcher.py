# ../models/data_fetcher.py
import yfinance as yf
import pandas as pd

# Chemins pour sauvegarder les fichiers CSV
hourly_csv_path = '../models/eth_usd_hourly.csv'
min15_csv_path = '../models/eth_usd_15min.csv'

# Télécharge les données ETH-USD pour les 30 derniers jours avec un intervalle d'une heure
print("Fetching ETH-USD data for 3 month (hourly interval)...")
data_hourly = yf.download('ETH-USD', period='3mo', interval='1h')

# Vérifie si des données ont été récupérées
if not data_hourly.empty:
    # Sauvegarde des données horaires en tant que CSV
    print(f"Saving hourly data to {hourly_csv_path}")
    data_hourly.to_csv(hourly_csv_path)
else:
    print("No hourly data fetched.")

# Télécharge les données ETH-USD pour les 30 derniers jours avec un intervalle de 15 minutes
print("Fetching ETH-USD data for 30 days (15-minute interval)...")
data_15min = yf.download('ETH-USD', period='1mo', interval='15m')

# Vérifie si des données ont été récupérées
if not data_15min.empty:
    # Sauvegarde des données 15 minutes en tant que CSV
    print(f"Saving 15-minute data to {min15_csv_path}")
    data_15min.to_csv(min15_csv_path)
else:
    print("No 15-minute data fetched.")

# Affiche les statistiques pour les deux ensembles de données
print("\nHourly Data Statistics:")
print(data_hourly.describe())

print("\n15-Minute Data Statistics:")
print(data_15min.describe())
