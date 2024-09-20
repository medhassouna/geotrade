import os
import numpy as np
import onnxruntime as ort
import csv
import datetime
from .volatility_adjustment import adjust_predictions_for_volatility, calculate_and_log_volatility  # Importing functions

# Load ONNX models for 15-minute and hourly data
model_15min_path = os.getenv('MODEL_15MIN_PATH', '/models/eth_usd_lstm_15min.onnx')  # Use environment variable or default path
model_hourly_path = os.getenv('MODEL_HOURLY_PATH', '/models/eth_usd_lstm_hourly.onnx')

print(f"Loading 15-minute ONNX model from: {model_15min_path}")
ort_session_15min = ort.InferenceSession(model_15min_path)
print("15-minute model loaded successfully.")

print(f"Loading hourly ONNX model from: {model_hourly_path}")
ort_session_hourly = ort.InferenceSession(model_hourly_path)
print("Hourly model loaded successfully.")

# Predict prices using the 15-minute and hourly ONNX models and log predictions
def predict_prices_multi_horizon(scaled_data_15min, scaled_data_hourly, scaler_15min, scaler_hourly, actual_prices_15min=None, actual_prices_hourly=None):
    """
    Generate predictions using both 15-minute and hourly models, log predictions to file.
    """
    # Step 1: Predict using the 15-minute model
    predicted_prices_15min = predict_with_model(scaled_data_15min, scaler_15min, ort_session_15min, 59)
    log_predictions(predicted_prices_15min, "15-minute", actual_prices_15min)

    # Step 2: Predict using the hourly model
    predicted_prices_hourly = predict_with_model(scaled_data_hourly, scaler_hourly, ort_session_hourly, 59)
    log_predictions(predicted_prices_hourly, "Hourly", actual_prices_hourly)

    # Step 3: Combine predictions (you can average them or apply another logic)
    combined_predictions = [(p1 + p2) / 2 for p1, p2 in zip(predicted_prices_15min, predicted_prices_hourly)]

    return combined_predictions

# Helper function to make predictions using a given ONNX model
def predict_with_model(scaled_data, scaler, model_session, sequence_length):
    """
    Make predictions using an ONNX model with the specified session and sequence length.
    """
    if len(scaled_data) < sequence_length:
        raise ValueError(f"Insufficient data: At least {sequence_length} data points are required for prediction.")

    if np.any(np.isnan(scaled_data)):
        raise ValueError("Input data contains NaN values. Please clean the data before passing it to the model.")

    input_data = scaled_data[-sequence_length:].reshape(1, sequence_length, 1).astype(np.float32)
    predicted_price_list = []

    for _ in range(60):
        outputs = model_session.run(None, {'input': input_data})
        predicted_price_scaled = outputs[0][0][0]
        predicted_price = scaler.inverse_transform([[predicted_price_scaled]])[0][0]
        predicted_price_list.append(predicted_price)
        input_data = np.roll(input_data, -1)
        input_data[0, -1, 0] = predicted_price_scaled

    return predicted_price_list

# Define file path for logging predictions
log_file_path = './models/prediction_log.csv'

# Log predictions to a CSV file for future analysis
def log_predictions(predictions, model_type, actual_prices=None):
    """
    Log predicted prices along with the timestamp and optional actual prices.

    :param predictions: List of predicted prices.
    :param model_type: "15-minute" or "Hourly" model for identification.
    :param actual_prices: Optional. List of actual prices (if available).
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    headers = ['timestamp', 'model_type', 'predicted_price', 'actual_price']

    with open(log_file_path, mode='a', newline='') as log_file:
        writer = csv.writer(log_file)
        if log_file.tell() == 0:
            writer.writerow(headers)

        for i in range(len(predictions)):
            row = [timestamp, model_type, predictions[i], actual_prices[i] if actual_prices else 'N/A']
            writer.writerow(row)