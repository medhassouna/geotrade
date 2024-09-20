import numpy as np
import csv
import datetime

# File path for logging volatility data
log_file_path = './models/prediction_log.csv'

# Function to calculate volatility based on price changes over a specified window
def calculate_volatility(prices, window=5):
    """
    Calculate rolling volatility (standard deviation of price changes) over the given window.
    
    Parameters:
    - prices: List of historical price data.
    - window: The rolling window size for volatility calculation. Default is 5.
    
    Returns:
    - volatility: The calculated standard deviation of price changes.
    """
    if len(prices) < window:
        return 0.0
    log_returns = np.diff(np.log(prices))  # Calculate log returns
    volatility = np.std(log_returns[-window:])  # Standard deviation over the window
    return volatility

# Function to adjust predictions based on volatility
def adjust_predictions_for_volatility(predicted_prices, volatility, threshold=0.02):
    """
    Adjust predictions based on volatility. If volatility is high, adjust the predicted prices
    to be more conservative by shrinking the range of predictions.
    
    Parameters:
    - predicted_prices: List of predicted prices from the model.
    - volatility: The calculated volatility.
    - threshold: The volatility threshold above which predictions are adjusted.
    
    Returns:
    - adjusted_prices: The adjusted list of predictions, with dampened values if volatility is high.
    """
    if volatility > threshold:
        print(f"High volatility detected: {volatility}. Adjusting predictions.")
        dampening_factor = 0.95  # Reduce predictions by 5% in case of high volatility
        adjusted_prices = [price * dampening_factor for price in predicted_prices]
        return adjusted_prices
    return predicted_prices

# Log the calculated volatility
def log_volatility(volatility, model_type):
    """
    Log the volatility for each prediction model.
    
    :param volatility: The calculated volatility value.
    :param model_type: "15-minute" or "Hourly" model for identification.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file_path, mode='a', newline='') as log_file:
        writer = csv.writer(log_file)
        writer.writerow([timestamp, f'{model_type} Volatility', volatility])

# Calculate and log volatility for 15-minute and hourly models
def calculate_and_log_volatility(prices_15min, prices_hourly):
    """
    Calculate volatility for 15-minute and hourly models, and log to file.
    """
    volatility_15min = calculate_volatility(prices_15min, window=5)
    log_volatility(volatility_15min, "15-minute")

    volatility_hourly = calculate_volatility(prices_hourly, window=5)
    log_volatility(volatility_hourly, "Hourly")

    return volatility_15min, volatility_hourly

# Calculate and log volatility for 15-minute and hourly models
def calculate_and_log_volatility_for_models(prices_15min, prices_hourly):
    """
    This function calculates the volatility for both 15-minute and hourly models and logs the values.
    It uses the `calculate_and_log_volatility` function from this module.
    """
    return calculate_and_log_volatility(prices_15min, prices_hourly)
