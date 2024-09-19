# ../models/train_lstm.py
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import DataLoader, TensorDataset
from ..routes import update_training_progress  # Import the progress function for real-time updates

# LSTM Model Definition
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        predictions = self.fc(lstm_out[:, -1, :])
        return predictions

# Function to create sequences from data
def create_sequences(data, seq_length):
    sequences = []
    for i in range(len(data) - seq_length):
        sequences.append(data[i:i + seq_length])
    return np.array(sequences)

# Function to train a model and send progress to the front-end
def train_model(model, train_loader, epochs=10):
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    total_batches = len(train_loader) * epochs
    processed_batches = 0

    for epoch in range(epochs):
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            processed_batches += 1
            progress = (processed_batches / total_batches) * 100
            update_training_progress(progress)  # Send real-time progress to the front-end

        print(f'Epoch {epoch+1}, Loss: {loss.item()}')

# Function to save a model to ONNX format
def save_model_to_onnx(model, seq_length, filename):
    dummy_input = torch.randn(1, seq_length - 1, 1)  # Adjust shape as needed
    torch.onnx.export(model, dummy_input, filename,
                      input_names=['input'], output_names=['output'])

# Load and preprocess data
def load_and_preprocess_data(file_path, seq_length):
    df = pd.read_csv(file_path)
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1, 1))

    # Create sequences
    data_sequences = create_sequences(scaled_data, seq_length)
    X = torch.tensor(data_sequences[:, :-1]).float()
    y = torch.tensor(data_sequences[:, -1]).float()

    # Prepare data for training
    train_data = TensorDataset(X, y)
    train_loader = DataLoader(train_data, batch_size=32, shuffle=True)

    return train_loader, scaler

# Main function to start model training based on user selection
def start_training(model_type):
    seq_length = 60  # Using 60 as the sequence length for both models

    if model_type == "eth_usd_lstm_15min":
        # Load and preprocess 15-minute interval data
        print("Training LSTM model on 15-minute interval data...")
        train_loader_15min, scaler_15min = load_and_preprocess_data('eth_usd_15min.csv', seq_length)

        # Define and train the 15-minute LSTM model
        input_size = 1
        hidden_size = 50
        output_size = 1
        model_15min = LSTMModel(input_size, hidden_size, output_size)
        train_model(model_15min, train_loader_15min, epochs=10)
        save_model_to_onnx(model_15min, seq_length, "eth_usd_lstm_15min.onnx")

    elif model_type == "eth_usd_lstm_hourly":
        # Load and preprocess hourly interval data
        print("Training LSTM model on hourly interval data...")
        train_loader_hourly, scaler_hourly = load_and_preprocess_data('eth_usd_hourly.csv', seq_length)

        # Define and train the hourly LSTM model
        input_size = 1
        hidden_size = 50
        output_size = 1
        model_hourly = LSTMModel(input_size, hidden_size, output_size)
        train_model(model_hourly, train_loader_hourly, epochs=10)
        save_model_to_onnx(model_hourly, seq_length, "eth_usd_lstm_hourly.onnx")

    print(f"{model_type} has been trained and saved.")
