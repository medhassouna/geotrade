import pandas as pd

def save_actual_signals(signals):
    """
    Save actual signals to a CSV file.
    """
    df = pd.DataFrame({'signal': signals})
    df.to_csv('/models/actual_signals.csv', index=False)
    print("Actual signals saved to actual_signals.csv")


def save_predicted_signals(signals):
    """
    Save predicted signals to a CSV file.
    """
    df = pd.DataFrame({'signal': signals})
    df.to_csv('/models/predicted_signals.csv', index=False)
    print("Predicted signals saved to predicted_signals.csv")    


def get_actual_signals():
    """
    Fetch actual signals from CSV.
    """
    try:
        df_actual = pd.read_csv('/models/actual_signals.csv')
        return df_actual['signal'].tolist()
    except FileNotFoundError:
        print("Actual signals file not found.")
        return []


def get_predicted_signals():
    """
    Fetch predicted signals from CSV.
    """
    try:
        df_predicted = pd.read_csv('/models/predicted_signals.csv')
        return df_predicted['signal'].tolist()
    except FileNotFoundError:
        print("Predicted signals file not found.")
        return []
