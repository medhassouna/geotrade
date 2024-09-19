# /server/fibonacci.py

# Determine trend based on the last 7 days' high and low prices compared to the current price
def determine_trend(data):
    current_price = data['Close'].iloc[-1]
    high = data['Close'].max()
    low = data['Close'].min()
    
    # If the current price is closer to the high, it's an uptrend; otherwise, downtrend
    return current_price > (high + low) / 2

# Calculate Fibonacci levels based on whether it's an uptrend or downtrend
def calculate_fibonacci_levels(data, uptrend):
    high = data['Close'].max()
    low = data['Close'].min()
    range_price = high - low

    if uptrend:
        # Fibonacci levels in uptrend
        levels = {
            '0%': low,
            '23.6%': low + 0.236 * range_price,
            '38.2%': low + 0.382 * range_price,
            '50%': (high + low) / 2,
            '61.8%': low + 0.618 * range_price,
            '100%': high
        }
    else:
        # Fibonacci levels in downtrend
        levels = {
            '0%': high,
            '23.6%': high - 0.236 * range_price,
            '38.2%': high - 0.382 * range_price,
            '50%': (high + low) / 2,
            '61.8%': high - 0.618 * range_price,
            '100%': low
        }
    
    return levels
