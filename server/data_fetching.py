import yfinance as yf
import pandas as pd

# Function to fetch ETH-USD data for the past 30 days at 15-minute intervals
def fetch_eth_data_15min():
    print("Fetching ETH-USD data for 30 days (15-minute interval)...")
    data_15min = yf.download(tickers='ETH-USD', period='30d', interval='15m')

    if data_15min.empty:
        print("No data fetched for 15-minute interval.")
        return None

    # Optionally, save the data to CSV
    data_15min.to_csv('/models/eth_usd_15min.csv', index=True)

    print(f"Fetched 15-minute interval data: {data_15min.tail()}")
    return data_15min


# Function to fetch ETH-USD data for the past 3 months at hourly intervals
def fetch_eth_data_hourly():
    print("Fetching ETH-USD data for 3 months (hourly interval)...")
    data_hourly = yf.download(tickers='ETH-USD', period='3mo', interval='1h')

    if data_hourly.empty:
        print("No data fetched for hourly interval.")
        return None

    # Optionally, save the data to CSV
    data_hourly.to_csv('/models/eth_usd_hourly.csv', index=True)

    print(f"Fetched hourly interval data: {data_hourly.tail()}")
    return data_hourly


# Function to fetch ETH-USD data for a specified interval (generic)
def fetch_eth_data(period='30d', interval='5m'):
    print(f"Fetching ETH-USD data for {period} with {interval} interval from yfinance...")
    data = yf.download(tickers='ETH-USD', period=period, interval=interval)
    
    if data.empty:
        print(f"No data fetched for {interval} interval.")
        return None

    print(f"Fetched data for {interval} interval: {data.tail()}")
    return data
