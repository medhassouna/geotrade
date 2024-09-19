import os
import numpy as np
import onnxruntime as ort

# Load ONNX models for 15-minute and hourly data
model_15min_path = os.getenv('MODEL_15MIN_PATH', '/models/eth_usd_lstm_15min.onnx')  # Use environment variable or default path
model_hourly_path = os.getenv('MODEL_HOURLY_PATH', '/models/eth_usd_lstm_hourly.onnx')

print(f"Loading 15-minute ONNX model from: {model_15min_path}")
ort_session_15min = ort.InferenceSession(model_15min_path)
print("15-minute model loaded successfully.")

print(f"Loading hourly ONNX model from: {model_hourly_path}")
ort_session_hourly = ort.InferenceSession(model_hourly_path)
print("Hourly model loaded successfully.")

# Predict prices using the 15-minute and hourly ONNX models
def predict_prices_multi_horizon(scaled_data_15min, scaled_data_hourly, scaler_15min, scaler_hourly):
    """
    Generate predictions using both 15-minute and hourly models and combine the results.
    """
    # Step 1: Predict using the 15-minute model
    predicted_prices_15min = predict_with_model(scaled_data_15min, scaler_15min, ort_session_15min, 59)
    
    # Step 2: Predict using the hourly model
    predicted_prices_hourly = predict_with_model(scaled_data_hourly, scaler_hourly, ort_session_hourly, 59)

    # Step 3: Combine predictions (you can average them or apply another logic)
    combined_predictions = [(p1 + p2) / 2 for p1, p2 in zip(predicted_prices_15min, predicted_prices_hourly)]

    return combined_predictions


# Helper function to make predictions using a given ONNX model
def predict_with_model(scaled_data, scaler, model_session, sequence_length):
    """
    Make predictions using an ONNX model with the specified session and sequence length.
    """
    # Step 1: Verify the input data
    if len(scaled_data) < sequence_length:
        raise ValueError(f"Insufficient data: At least {sequence_length} data points are required for prediction.")

    # Ensure there are no NaN values in the input data
    if np.any(np.isnan(scaled_data)):
        raise ValueError("Input data contains NaN values. Please clean the data before passing it to the model.")

    # Step 2: Prepare the input for the model (Use the last sequence_length data points)
    input_data = scaled_data[-sequence_length:].reshape(1, sequence_length, 1).astype(np.float32)
    predicted_price_list = []

    # Step 3: Run predictions for the next 60 time steps
    for i in range(60):
        # Run the model on the input data
        outputs = model_session.run(None, {'input': input_data})
        predicted_price_scaled = outputs[0][0][0]  # Extract the predicted value (scaled)

        # Step 4: Inverse scaling to get the actual predicted price
        predicted_price = scaler.inverse_transform([[predicted_price_scaled]])[0][0]
        predicted_price_list.append(predicted_price)

        # Step 5: Prepare the input for the next prediction (shift the data and append the new prediction)
        input_data = np.roll(input_data, -1)  # Shift data to the left
        input_data[0, -1, 0] = predicted_price_scaled  # Append the new predicted value

    return predicted_price_list


# Volatility and prediction adjustments
def calculate_volatility(prices, window=5):
    """
    Calculate rolling volatility (standard deviation of price changes) over the given window.
    """
    if len(prices) < window:
        return 0.0
    log_returns = np.diff(np.log(prices))  # Calculate log returns
    volatility = np.std(log_returns[-window:])  # Standard deviation over the window
    return volatility


def adjust_predictions_for_volatility(predicted_prices, volatility, threshold=0.02):
    """
    Adjust predictions based on volatility. If volatility is high, we can adjust the predicted prices
    to be more conservative by shrinking the range of predictions. This can help reduce over-trading
    in highly volatile markets.
    
    Parameters:
    - predicted_prices: List of predicted prices
    - volatility: The calculated volatility
    - threshold: The level of volatility above which we adjust predictions
    """
    if volatility > threshold:
        print(f"High volatility detected: {volatility}. Adjusting predictions.")
        # Apply a dampening factor to the predicted prices
        dampening_factor = 0.95  # Reduce predictions by 5% if high volatility is detected
        adjusted_prices = [price * dampening_factor for price in predicted_prices]
        return adjusted_prices
    return predicted_prices
