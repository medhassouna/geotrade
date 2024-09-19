import numpy as np

# Calcul robuste de la volatilité à partir des rendements logarithmiques
def calculate_volatility(prices, window=5, use_exponential_weighting=False, clean_data=True):
    """
    Calcule une volatilité robuste à partir des rendements logarithmiques des prix.

    - prices: Liste des prix ou tableau numpy à partir desquels calculer la volatilité.
    - window: Période de temps sur laquelle calculer la volatilité. Par exemple, 10 périodes.
    - use_exponential_weighting: Si True, utilise une moyenne mobile exponentielle pour donner plus de poids aux rendements récents.
    - clean_data: Si True, nettoie les NaN et outliers avant le calcul.

    Retourne la volatilité calculée sous forme d'écart-type annualisé ou par période définie.
    """
    
    # Vérifier que les données sont suffisantes pour le calcul
    if len(prices) < window + 1:
        raise ValueError(f"Not enough price data to calculate volatility for window {window}. Minimum required: {window + 1}")

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
    periods_per_year = 365 * 24 * 12  # Si on suppose 5 min par période dans les cryptos
    annualized_volatility = volatility * np.sqrt(periods_per_year)

    print(f"Volatility calculated: {volatility}, Annualized Volatility: {annualized_volatility}")
    return annualized_volatility


# Générer des signaux de trading basés sur les prix, RSI, niveaux Fibonacci et la volatilité
def generate_signal_with_confidence(current_price, predicted_price, rsi_value, fibonacci_levels, prices):
    """
    Génère un signal de trading basé sur les niveaux Fibonacci, l'RSI et la volatilité.

    - current_price: Prix actuel.
    - predicted_price: Prix prédit.
    - rsi_value: Valeur actuelle du RSI.
    - fibonacci_levels: Niveaux Fibonacci calculés pour la période.
    - prices: Série de prix (pour le calcul de la volatilité).

    Retourne un signal ("Buy", "Sell", "Hold") en fonction des critères, et une confiance en pourcentage.
    """
    
    # Calculer la volatilité des prix
    volatility = calculate_volatility(prices, window=5, use_exponential_weighting=True)

    # Tolérance ajustée en fonction de la volatilité
    tolerance = 0.005 * (1 + volatility)  # Ajustement de la tolérance basé sur la volatilité

    # Vérifier si le prix actuel est proche des niveaux de Fibonacci
    near_resistance = any(
        abs(current_price - level) / level < tolerance for level in fibonacci_levels.values()
    )

    # Ne pas générer de signal si l'RSI est dans une zone risquée ou si le prix est proche d'une résistance
    if rsi_value > 70 or rsi_value < 30 or near_resistance:
        print(f"RSI trop élevé/bas ou prix proche d'une résistance, pas de signal. RSI: {rsi_value}, Proximité Fibonacci: {near_resistance}")
        return "Hold", 0  # No signal and confidence 0

    # Calcul du niveau de confiance basé sur l'écart du prix prédit et la volatilité
    price_difference = abs(predicted_price - current_price)
    confidence = (price_difference / (current_price * tolerance)) * 100  # Confiance basée sur l'écart et la volatilité

    # Cap the confidence to 100%
    confidence = min(confidence, 100)

    # Décision d'achat/vente basée sur le prix prédit, ajusté pour la volatilité
    if predicted_price > current_price * (1 + tolerance):  # Signal d'achat ajusté pour la volatilité
        return f"Buy", confidence
    elif predicted_price < current_price * (1 - tolerance):  # Signal de vente ajusté pour la volatilité
        return f"Sell", confidence
    else:
        return "Hold", 0  # No confidence for Hold signals


# Calcul du stop-loss et du take-profit en fonction du signal et de la volatilité
def calculate_stop_loss_take_profit(entry_price, signal, volatility):
    """
    Ajuste dynamiquement les niveaux de stop-loss et de take-profit en fonction de la volatilité du marché.

    - entry_price: Le prix d'entrée pour le trade.
    - signal: Le signal généré ("Buy", "Sell", ou "Hold").
    - volatility: La volatilité actuelle du marché.

    Retourne les niveaux de stop-loss et de take-profit ajustés.
    """

    if signal == "Buy":
        stop_loss = entry_price * (1 - 0.02 * (1 + volatility))  # 2% en dessous, ajusté pour la volatilité
        take_profit = entry_price * (1 + 0.05 * (1 + volatility))  # 5% au-dessus, ajusté pour la volatilité
    elif signal == "Sell":
        stop_loss = entry_price * (1 + 0.02 * (1 + volatility))  # 2% au-dessus, ajusté pour la volatilité
        take_profit = entry_price * (1 - 0.05 * (1 + volatility))  # 5% en dessous, ajusté pour la volatilité
    else:
        stop_loss = take_profit = None

    print(f"Calculated Stop Loss: {stop_loss}, Take Profit: {take_profit}, Volatility: {volatility}")
    return stop_loss, take_profit
