// fibonacciCalculator.js

// Function to calculate Fibonacci levels based on high and low prices and trend direction
// 'high' is the highest price in the range, 'low' is the lowest, and 'uptrend' is a boolean indicating market direction
export const calculateFibonacciLevels = (high, low, uptrend) => {
  const range = high - low; // Calculate the price range between the high and low

  // If the market is in an uptrend, calculate Fibonacci levels starting from the low
  if (uptrend) {
    return [
      { name: "0%", value: low }, // 0% level at the lowest price
      { name: "23.6%", value: low + range * 0.236 }, // 23.6% retracement level
      { name: "38.2%", value: low + range * 0.382 }, // 38.2% retracement level
      { name: "50%", value: (high + low) / 2 }, // 50% retracement level (mid-point)
      { name: "61.8%", value: low + range * 0.618 }, // 61.8% retracement level
      { name: "100%", value: high }, // 100% level at the highest price
    ];
  } 
  // If the market is in a downtrend, calculate Fibonacci levels starting from the high
  else {
    return [
      { name: "0%", value: high }, // 0% level at the highest price
      { name: "23.6%", value: high - range * 0.236 }, // 23.6% retracement level
      { name: "38.2%", value: high - range * 0.382 }, // 38.2% retracement level
      { name: "50%", value: (high + low) / 2 }, // 50% retracement level (mid-point)
      { name: "61.8%", value: high - range * 0.618 }, // 61.8% retracement level
      { name: "100%", value: low }, // 100% level at the lowest price
    ];
  }
};
