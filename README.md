Trading Dashboard
# Geotrade

GeoTrade is a cryptocurrency and trading dashboard that uses machine learning models to predict price movements. It allows users to visualize trading data, train machine learning models on different datasets, and track the progress of model training in real time via a web interface.

## Features

- **Real-time Trading Data Visualization**: View live cryptocurrency price trends using real-time data.
- **Trading Signals**: Buy/Sell signals are generated using price predictions, Fibonacci levels, RSI, and market volatility.
- **Machine Learning Model Training**: Train models (e.g., ETH/USD, BTC/USD) directly from the dashboard interface.
- **Progress Tracking**: Monitor the training progress with a real-time progress bar.
- **Support for Multiple Models**: Choose between different trading pairs (e.g., ETH/USD, BTC/USD, XAU/USD) for predictions.

## Getting Started

### Prerequisites

- **Python 3.9+**
- **Docker** and **Docker Compose**
- **Git**

### Installing

1. Clone the repository:
    ```bash
    git clone https://github.com/medhassouna/geotrade.git
    cd geotrade
    ```

2. Set up your environment:
    - Install dependencies:
      ```bash
      pip install -r requirements.txt
      ```

3. (Optional) Configure `.env`:
   - Create a `.env` file for any necessary environment variables such as model paths, Flask settings, etc.

4. Start the application with Docker:
    ```bash
    docker-compose up --build
    ```

## Usage

Once the application is running, open your browser and navigate to `http://localhost:8080`. 

### Features:

- **View Trading Data**: Visualize price, volatility, and other indicators.
- **Train Models**: Select a trading pair (e.g., ETH/USD) and train a machine learning model directly from the dashboard. The progress bar will show the real-time progress of the training process.
- **Real-time Updates**: The application updates the trading chart and signals every 10 seconds.

## Project Structure

```bash
geotrade/
│
├── server/
│   ├── data_fetching.py          # Fetches real-time trading data from APIs
│   ├── data_processing.py        # Preprocesses the data for model training
│   ├── model_inference.py        # Contains ONNX model inference logic
│   ├── routes.py                 # Flask route handlers
│   ├── signal_generation.py      # Generates Buy/Sell signals using indicators
│   ├── fibonacci.py              # Calculates Fibonacci levels
│   └── train_lstm.py             # LSTM model training script
│
├── static/
│   ├── css/
│   │   └── style.css             # Frontend styles
│   ├── js/
│   │   ├── main.js               # Main frontend logic
│   │   ├── signalDisplay.js      # Signal update logic
│   │   └── socketHandler.js      # WebSocket handler for real-time updates
│
├── templates/
│   └── index.html                # Main HTML file for the web interface
├── Dockerfile                    # Dockerfile for the application
├── docker-compose.yml            # Docker Compose configuration
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
└── .env                          # Environment variables (optional)

