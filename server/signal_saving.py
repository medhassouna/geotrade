import pandas as pd

def save_actual_signals(actual_signals, filepath='/models/actual_signals.csv'):
    """
    Save actual signals to a CSV file.
    :param actual_signals: List of actual signals to save.
    :param filepath: File path where the CSV will be saved.
    """
    df = pd.DataFrame({'signal': actual_signals})
    df.to_csv(filepath, index=False)
    print(f"Actual signals saved to {filepath}")

def save_predicted_signals(predicted_signals, filepath='/models/predicted_signals.csv'):
    """
    Save predicted signals to a CSV file.
    :param predicted_signals: List of predicted signals to save.
    :param filepath: File path where the CSV will be saved.
    """
    df = pd.DataFrame({'signal': predicted_signals})
    df.to_csv(filepath, index=False)
    print(f"Predicted signals saved to {filepath}")
