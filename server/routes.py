from flask import render_template
from . import app, socketio
from .data_fetching import fetch_eth_data_15min, fetch_eth_data_hourly
from .data_processing import preprocess, calculate_rsi, calculate_volatility
from .fibonacci import determine_trend, calculate_fibonacci_levels
from .model_inference import predict_prices_multi_horizon
from .signal_generation import generate_signal_with_confidence, calculate_stop_loss_take_profit

# Serve the index.html
@app.route('/')
def index():
    print("Serving index.html")
    return render_template('index.html')

# Handle model training
@socketio.on('start_training')
def handle_training_request(data):
    model_type = data.get('model', 'eth_usd_lstm_15min')
    print(f"Training model: {model_type}")
    start_training(model_type)

# Send progress updates to the front-end
def update_training_progress(progress):
    socketio.emit('training_progress', progress)

# Handle data and predictions for both 15-minute and hourly data
@socketio.on('request_data')
def handle_data_request():
    print("Received data request from frontend.")

    # **1. Fetch both 15-minute and hourly data**
    data_15min = fetch_eth_data_15min()
    data_hourly = fetch_eth_data_hourly()

    if data_15min is None or data_hourly is None:
        print("No data fetched, aborting the request.")
        return  # Early exit if no data was fetched

    # **2. Get the current price from the 15-minute data**
    current_price = data_15min['Close'].iloc[-1]
    print(f"Current Price: {current_price}")

    # **3. Preprocess the 15-minute and hourly data**
    prices_scaled_15min, scaler_15min = preprocess(data_15min)
    prices_scaled_hourly, scaler_hourly = preprocess(data_hourly)

    # **4. Predict the next prices using both 15-minute and hourly models**
    predicted_prices_15min = predict_prices_multi_horizon(prices_scaled_15min, prices_scaled_hourly, scaler_15min, scaler_hourly)
    print(f"Predicted Prices (15min): {predicted_prices_15min[-5:]}")

    # **5. Calculate Fibonacci levels and determine the trend for both timeframes**
    last_7_days_data_15min = data_15min[-7 * 24 * 4:]  # Last 7 days of 15-minute data (96 intervals per day)
    last_30_days_data_hourly = data_hourly[-30 * 24:]  # Last 30 days of hourly data

    # Calculate Fibonacci levels for both timeframes
    uptrend_15min = determine_trend(last_7_days_data_15min)
    fibonacci_levels_15min = calculate_fibonacci_levels(last_7_days_data_15min, uptrend_15min)

    uptrend_hourly = determine_trend(last_30_days_data_hourly)
    fibonacci_levels_hourly = calculate_fibonacci_levels(last_30_days_data_hourly, uptrend_hourly)

    print(f"Fibonacci Levels (15min): {fibonacci_levels_15min}")
    print(f"Fibonacci Levels (hourly): {fibonacci_levels_hourly}")

    # **6. Calculate RSI for both timeframes**
    rsi_15min = calculate_rsi(data_15min['Close'])
    rsi_hourly = calculate_rsi(data_hourly['Close'])

    print(f"RSI (15min): {rsi_15min.iloc[-1]}")
    print(f"RSI (hourly): {rsi_hourly.iloc[-1]}")

    # **7. Calculate Volatility for both timeframes**
    volatility_15min = calculate_volatility(data_15min['Close'])
    volatility_hourly = calculate_volatility(data_hourly['Close'])

    print(f"Volatility (15min): {volatility_15min}")
    print(f"Volatility (hourly): {volatility_hourly}")

    # **8. Generate trading signals and confidence levels based on 15-minute and hourly data**
    signal_15min, confidence_15min = generate_signal_with_confidence(current_price, predicted_prices_15min[-1], rsi_15min.iloc[-1], fibonacci_levels_15min, data_15min['Close'])
    signal_hourly, confidence_hourly = generate_signal_with_confidence(current_price, predicted_prices_15min[-1], rsi_hourly.iloc[-1], fibonacci_levels_hourly, data_hourly['Close'])

    # **Combine signals for a final decision**
    signal_combined = "Hold"
    confidence_combined = (confidence_15min + confidence_hourly) / 2
    if signal_15min == "Buy" and signal_hourly == "Buy":
        signal_combined = f"Buy: {confidence_combined:.2f}%"
    elif signal_15min == "Sell" and signal_hourly == "Sell":
        signal_combined = f"Sell: {confidence_combined:.2f}%"

    entry_price = current_price if signal_combined != "Hold" else None
    print(f"Trading Signal (combined): {signal_combined}, Entry Price: {entry_price}")

    # **9. Calculate stop loss and take profit based on the combined signal**
    stop_loss, take_profit = calculate_stop_loss_take_profit(entry_price, signal_combined.split(":")[0], (volatility_15min + volatility_hourly) / 2)
    print(f"Stop Loss: {stop_loss}, Take Profit: {take_profit}")

    # **10. Emit the data back to the client**
    socketio.emit('update_chart', {
        'prices': data_15min['Close'].tolist(),
        'predicted_price': predicted_prices_15min[-1],  # Sending 15min predictions
        'predicted_prices': predicted_prices_15min,  # Sending the full 15min prediction list
        'current_price': current_price,
        'rsi': rsi_15min.tolist(),  # Sending 15min RSI
        'signal': signal_combined,  # Sending the combined signal
        'confidence': confidence_combined,  # Sending the confidence level
        'entry_price': entry_price,
        'stop_loss': stop_loss,
        'take_profit': take_profit,
        'fibonacci_levels': fibonacci_levels_15min,  # Sending 15min Fibonacci levels
        'volatility': volatility_15min  # Sending 15min volatility (you can choose to send a combined volatility)
    })

    print(f"Data emitted to frontend: Signal: {signal_combined}, Confidence: {confidence_combined}, Entry Price: {entry_price}, Stop Loss: {stop_loss}, Take Profit: {take_profit}, Volatility: {volatility_15min}")
