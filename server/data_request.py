from .data_fetching import fetch_eth_data_15min, fetch_eth_data_hourly
from .data_processing import preprocess, calculate_rsi, calculate_volatility
from .fibonacci import determine_trend, calculate_fibonacci_levels
from .model_inference import predict_prices_multi_horizon
from .signal_generation import generate_signal_with_confidence, calculate_stop_loss_take_profit
from .performance_evaluation import evaluate_performance, save_actual_signals, save_predicted_signals
from flask_socketio import emit

def handle_data_request():
    """
    Fetch data, process it, generate predictions, and emit results to the client.
    Save actual and predicted signals, and evaluate performance.
    """
    # Fetch data
    data_15min = fetch_eth_data_15min()
    data_hourly = fetch_eth_data_hourly()

    if data_15min is None or data_hourly is None:
        print("No data fetched, aborting the request.")
        return

    # Get the current price
    current_price = data_15min['Close'].iloc[-1]

    # Preprocess data
    prices_scaled_15min, scaler_15min = preprocess(data_15min)
    prices_scaled_hourly, scaler_hourly = preprocess(data_hourly)

    # Predict prices
    predicted_prices_15min = predict_prices_multi_horizon(prices_scaled_15min, prices_scaled_hourly, scaler_15min, scaler_hourly)

    # Calculate Fibonacci levels
    last_7_days_data_15min = data_15min[-7 * 24 * 4:]
    last_30_days_data_hourly = data_hourly[-30 * 24:]
    fibonacci_levels_15min = calculate_fibonacci_levels(last_7_days_data_15min, determine_trend(last_7_days_data_15min))
    fibonacci_levels_hourly = calculate_fibonacci_levels(last_30_days_data_hourly, determine_trend(last_30_days_data_hourly))

    # Calculate RSI
    rsi_15min = calculate_rsi(data_15min['Close'])
    rsi_hourly = calculate_rsi(data_hourly['Close'])

    # Calculate Volatility
    volatility_15min = calculate_volatility(data_15min['Close'])
    volatility_hourly = calculate_volatility(data_hourly['Close'])

    # Generate signals and confidence for 15-minute and hourly data
    signal_15min, confidence_15min = generate_signal_with_confidence(current_price, predicted_prices_15min[-1], rsi_15min.iloc[-1], fibonacci_levels_15min, data_15min['Close'])
    signal_hourly, confidence_hourly = generate_signal_with_confidence(current_price, predicted_prices_15min[-1], rsi_hourly.iloc[-1], fibonacci_levels_hourly, data_hourly['Close'])

    # Combine signals for a final decision
    signal_combined = "Hold"
    confidence_combined = (confidence_15min + confidence_hourly) / 2
    if signal_15min == "Buy" and signal_hourly == "Buy":
        signal_combined = f"Buy: {confidence_combined:.2f}%"
    elif signal_15min == "Sell" and signal_hourly == "Sell":
        signal_combined = f"Sell: {confidence_combined:.2f}%"

    entry_price = current_price if signal_combined != "Hold" else None

    # Calculate stop loss and take profit based on the combined signal
    stop_loss, take_profit = calculate_stop_loss_take_profit(entry_price, signal_combined.split(":")[0], (volatility_15min + volatility_hourly) / 2)

    # **Save actual and predicted signals**
    actual_signals = [signal_combined]  # Saving the combined signal instead of individual timeframe signals
    predicted_signals = [signal_combined]  # Assuming the predicted signal is the same as the combined decision

    save_actual_signals(actual_signals)  # Saving combined signal as actual signal
    save_predicted_signals(predicted_signals)  # Saving combined signal as predicted signal

    # Evaluate performance
    evaluate_performance(actual_signals, predicted_signals)

    # Emit the data to the frontend
    emit('update_chart', {
        'prices': data_15min['Close'].tolist(),
        'predicted_prices': predicted_prices_15min,
        'current_price': current_price,
        'rsi': rsi_15min.tolist(),
        'signal': signal_combined,
        'confidence': confidence_combined,
        'entry_price': entry_price,
        'stop_loss': stop_loss,
        'take_profit': take_profit,
        'fibonacci_levels': fibonacci_levels_15min,
        'volatility': volatility_15min
    })

    print(f"Data emitted to frontend: Signal: {signal_combined}, Confidence: {confidence_combined}, Entry Price: {entry_price}, Stop Loss: {stop_loss}, Take Profit: {take_profit}, Volatility: {volatility_15min}")
