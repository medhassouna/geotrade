import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Preprocess the data by scaling the prices (Min-Max Scaling) for both 15-minute and hourly data
def preprocess(data, timeframe='15min'):
    """
    Pré-traite les données en appliquant un MinMaxScaler sur la colonne 'Close'.
    Peut traiter les données pour différents timeframes (par ex. 15min, 1h).
    
    - `data`: Le DataFrame à traiter.
    - `timeframe`: Indique le type de données (par défaut '15min', peut être '1h' ou d'autres).
    
    Retourne les données mises à l'échelle et le scaler utilisé pour une future transformation inverse.
    """

    print(f"Preprocessing data for {timeframe} timeframe...")

    # Vérifier si la colonne 'Close' est présente dans les données
    if 'Close' not in data.columns:
        raise ValueError(f"La colonne 'Close' n'existe pas dans les données fournies pour {timeframe}.")

    # Extraire les prix de clôture et gérer les données manquantes
    prices = data['Close'].fillna(method='ffill')  # Remplir les valeurs manquantes par propagation en avant
    prices = prices.fillna(method='bfill')  # Si nécessaire, remplir les valeurs en arrière

    # Appliquer le scaling MinMaxScaler
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(prices.values.reshape(-1, 1))

    # Logging pour le debug
    print(f"Data scaled for {timeframe} (first 5 entries): {data_scaled[:5]}")

    return data_scaled, scaler

# Calculate RSI (Relative Strength Index) for both 15-minute and hourly data
def calculate_rsi(prices, window=14, timeframe='15min'):
    """
    Calcule l'indice de force relative (RSI) sur une fenêtre donnée.
    Peut traiter les données pour différents timeframes (par ex. 15min, 1h).
    
    - `prices`: Le tableau de prix à utiliser pour le calcul du RSI.
    - `window`: La fenêtre de calcul pour le RSI (14 par défaut).
    - `timeframe`: Indique le type de données (par ex. '15min' ou '1h').
    
    Retourne une série RSI remplie.
    """

    print(f"Calculating RSI for {timeframe} timeframe...")

    # Calculer la variation des prix
    delta = prices.diff()

    # Calculer les gains et les pertes
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    # Gérer le cas où toutes les pertes sont nulles (éviter la division par zéro)
    loss = loss.replace(0, np.nan)  # Remplacer les 0 par NaN pour éviter la division par zéro

    # Calcul du RSI en tenant compte des gains et pertes moyens
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # Remplir les NaN restants (au début de la série, ou en cas de division par 0)
    rsi_filled = rsi.fillna(50)  # RSI neutre à 50 pour les périodes sans données suffisantes

    # Logging pour le debug
    print(f"RSI calculated for {timeframe} (first 5 entries): {rsi_filled.head()}")

    return rsi_filled

# Calculate robust volatility for both 15-minute and hourly data
def calculate_volatility(prices, window=5, timeframe='15min', use_exponential_weighting=False, clean_data=True):
    """
    Calcule une volatilité robuste à partir des rendements logarithmiques des prix.
    
    - `prices`: Liste des prix à partir desquels calculer la volatilité.
    - `window`: Période de temps sur laquelle calculer la volatilité.
    - `timeframe`: Indique le type de données (par ex. '15min' ou '1h').
    - `use_exponential_weighting`: Si True, utilise une moyenne mobile exponentielle pour donner plus de poids aux rendements récents.
    - `clean_data`: Si True, traite les NaN et les outliers avant le calcul.
    
    Retourne la volatilité calculée sous forme d'écart-type annualisé ou par période définie.
    """

    print(f"Calculating volatility for {timeframe} timeframe...")

    # Vérifier que les données sont suffisantes pour le calcul
    if len(prices) < window + 1:
        raise ValueError(f"Not enough price data to calculate volatility for {timeframe} with window {window}. Minimum required: {window + 1}")

    # Nettoyage des données
    prices = np.asarray(prices)
    if clean_data:
        # Remplacer les NaN par la valeur précédente ou la moyenne
        prices = np.nan_to_num(prices, nan=np.nanmean(prices))

        # Suppression des outliers extrêmes (basé sur un z-score)
        z_scores = (prices - np.mean(prices)) / np.std(prices)
        prices = prices[np.abs(z_scores) < 3]  # On garde seulement les z-scores inférieurs à 3

    # Calcul des rendements logarithmiques
    log_returns = np.diff(np.log(prices))

    # Calcul de la volatilité avec ou sans pondération exponentielle
    if use_exponential_weighting:
        # Moyenne mobile exponentielle pour pondérer plus les rendements récents
        weights = np.exp(np.linspace(-1., 0., window))
        weights /= weights.sum()  # Normaliser les poids
        weighted_avg = np.convolve(log_returns[-window:], weights, mode='valid')
        volatility = np.std(weighted_avg)
    else:
        # Volatilité simple : écart-type des rendements logarithmiques
        volatility = np.std(log_returns[-window:])

    # Annualisation de la volatilité si nécessaire
    periods_per_year = 365 * 24 * (12 if timeframe == '15min' else 1)  # Adjust periods based on timeframe
    annualized_volatility = volatility * np.sqrt(periods_per_year)

    print(f"Volatility calculated for {timeframe}: {volatility}, Annualized Volatility: {annualized_volatility}")
    return annualized_volatility
