import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import DataLoader, TensorDataset
import argparse
import threading

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

# Function to train a model
def train_model(model, train_loader, epochs=10):
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(epochs):
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        print(f'Epoch {epoch+1}, Loss: {loss.item()}')

# Function to save a model to ONNX format
def save_model_to_onnx(model, seq_length, filename):
    dummy_input = torch.randn(1, seq_length - 1, 1)  # Adjust shape as needed
    torch.onnx.export(model, dummy_input, filename, input_names=['input'], output_names=['output'])

# Load and preprocess data
def load_and_preprocess_data(file_path, seq_length):
    print(f"Loading data from {file_path}")
    df = pd.read_csv(file_path)
    print(f"Data loaded. First few rows:\n{df.head()}")
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

# Function to start model training
def start_training(model_type, csv_path, model_name, seq_length=60):
    # Load and preprocess data
    print(f"Training LSTM model on {model_type} interval data...")
    train_loader, _ = load_and_preprocess_data(csv_path, seq_length)

    # Define the LSTM model
    input_size = 1
    hidden_size = 50
    output_size = 1
    model = LSTMModel(input_size, hidden_size, output_size)

    # Train the model
    train_model(model, train_loader, epochs=10)

    # Save the model to ONNX format
    save_model_to_onnx(model, seq_length, f"{model_name}.onnx")
    print(f"{model_name} has been trained and saved.")

# Main function to handle command-line arguments and run both models simultaneously
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Train LSTM models for 15min and hourly ETH-USD data.')
    parser.add_argument('--run_both', action='store_true', help='Run both 15min and hourly models simultaneously')
    
    args = parser.parse_args()

    # Paths for the data files
    csv_path_15min = 'D:/trading_scripts/geotrade/models/eth_usd_15min.csv'
    csv_path_hourly = 'D:/trading_scripts/geotrade/models/eth_usd_hourly.csv'

    # Run both models simultaneously
    if args.run_both:
        print("Running both 15min and hourly models...")

        # Thread for 15min model
        thread_15min = threading.Thread(target=start_training, args=("15-minute", csv_path_15min, "eth_usd_lstm_15min"))

        # Thread for hourly model
        thread_hourly = threading.Thread(target=start_training, args=("hourly", csv_path_hourly, "eth_usd_lstm_hourly"))

        # Start both threads
        thread_15min.start()
        thread_hourly.start()

        # Wait for both threads to finish
        thread_15min.join()
        thread_hourly.join()

        print("Both models have been trained.")
    else:
        # Default: Run one model (you can choose which one)
        start_training("15-minute", csv_path_15min, "eth_usd_lstm_15min")
