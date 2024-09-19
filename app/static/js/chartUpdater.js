// chartUpdater.js

// Import necessary functions from other modules
import { calculateFibonacciLevels } from './fibonacciCalculator.js'; // Calculates Fibonacci levels
import { updateSignalDisplay } from './signalDisplay.js'; // Updates the display of buy/sell signals
import { updatePlot } from './plotManager.js'; // Updates the chart with new data

// Main function to update the chart with the provided data
export const updateChart = (data) => {
  // console.log("Received data for chart update:", data); // Debugging received data

  // Extract key values from the data object, setting defaults if values are NaN
  const actualPrice = isNaN(data.current_price) ? 0 : data.current_price;
  const signalPrice = isNaN(data.entry_price) ? 0 : data.entry_price;
  const takeProfit = isNaN(data.take_profit) ? 0 : data.take_profit;
  const stopLoss = isNaN(data.stop_loss) ? 0 : data.stop_loss;

  // console.log("Actual Price:", actualPrice); // Debugging actual price
  // console.log("Signal Price:", signalPrice, "Take Profit:", takeProfit, "Stop Loss:", stopLoss); // Debugging TP and SL

  // Prepare real price data points with time values for the x-axis
  const realPrices = data.prices.map((price, i) => ({
    x: new Date(Date.now() - (data.prices.length - i) * 15 * 60 * 1000), // Create time intervals
    y: price, // Price values
  }));
  
  // console.log("Real Prices Data:", realPrices); // Debugging real prices

  // Set the color of the markers based on the RSI value
  const markerColors = data.rsi.map((rsiValue) => {
    return rsiValue > 70
      ? "rgba(0, 255, 0, 0.2)" // Green for overbought
      : rsiValue < 30
      ? "rgba(255, 0, 0, 0.2)" // Red for oversold
      : "rgba(128, 128, 128, 0.2)"; // Grey for neutral RSI
  });

  // console.log("Marker Colors (RSI):", markerColors); // Debugging RSI marker colors

  // Structure the RSI data for display on the chart
  const rsiData = {
    x: realPrices.slice(realPrices.length - data.rsi.length).map((d) => d.x), // Align the x-axis with real prices
    y: data.rsi, // RSI values
    mode: "markers", // Display as markers
    name: "Relative Strength Index", // Name in the legend
    marker: { color: markerColors, size: 15, opacity: 0.4, symbol: "circle" }, // Marker settings
    yaxis: "y2", // Place on the secondary y-axis
  };

  // console.log("RSI Data:", rsiData); // Debugging RSI data

  // Structure the predicted price data for future values
  const predictedPrices = data.predicted_prices.map((price, i) => ({
    x: new Date(Date.now() + (i + 1) * 15 * 60 * 1000), // Future time intervals
    y: price, // Predicted price values
  }));

  // console.log("Predicted Prices Data:", predictedPrices); // Debugging predicted prices

  // Get the high and low prices from the last week to calculate Fibonacci levels
  const lastWeekPrices = data.prices.slice(-7 * 24 * 4); // Last 7 days of data (assuming 5-minute intervals)
  const high = Math.max(...lastWeekPrices); // Highest price in the last week
  const low = Math.min(...lastWeekPrices); // Lowest price in the last week

  // Debugging high and low prices
  console.log("Last Week's High:", high, "Last Week's Low:", low);

  // Determine uptrend based on whether current price is closer to the week's high or low
  const uptrend = actualPrice > (high + low) / 2; 
  console.log("Uptrend Status:", uptrend ? "Uptrend" : "Downtrend"); // Debugging uptrend status

  // Update the trend label in the HTML
  const trendLabel = document.getElementById('trend_label');
  trendLabel.textContent = `Trend: ${uptrend ? "Uptrend" : "Downtrend"}`;
  trendLabel.style.color = uptrend ? "green" : "red"; // Green for uptrend, red for downtrend

  // Calculate Fibonacci levels based on whether the market is trending up or down
  const fibonacciLevels = calculateFibonacciLevels(high, low, uptrend);

  console.log("Fibonacci Levels:", fibonacciLevels); // Debugging Fibonacci levels

  // Create the trace for real prices on the chart
  const trace1 = {
    x: realPrices.map((d) => d.x), // Time values on x-axis
    y: realPrices.map((d) => d.y), // Real price values
    mode: "lines+markers", // Display as lines and markers
    name: "Real Prices", // Name in the legend
    line: { color: "blue" }, // Line color
  };

  // Create the trace for predicted prices on the chart
  const trace2 = {
    x: predictedPrices.map((d) => d.x), // Future time values
    y: predictedPrices.map((d) => d.y), // Predicted price values
    mode: "lines", // Display as lines
    name: "Predicted Prices", // Name in the legend
    line: { dash: "dot", color: "red" }, // Dashed red line
  };

  // Create traces for Fibonacci levels on the chart
  const trace3 = fibonacciLevels.map((level) => ({
    type: "scatter", // Display as scatter plot
    x: [new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), new Date()], // Last 7 days
    y: [level.value, level.value], // Fibonacci level value on y-axis
    mode: "lines", // Display as lines
    line: { dash: "dot", color: "orange" }, // Dashed orange line
    name: `${level.name} Fibonacci`, // Name for each level in the legend
  }));

  // Combine all the data traces (real prices, predicted prices, and Fibonacci levels) into one array
  const dataTraces = [trace1, trace2, ...trace3, rsiData];

  // console.log("Data Traces for Plot:", dataTraces); // Debugging all data traces

  // Define layout updates for shapes (TP, SL) and annotations (high/low prices)
  const layoutUpdate = {
    shapes: [
      // TP (Take Profit) rectangle
      signalPrice && takeProfit && {
        type: "rect",
        xref: "x",
        yref: "y",
        x0: realPrices[realPrices.length - 1].x, // Start from the last real price
        x1: predictedPrices[predictedPrices.length - 1].x, // End at the last predicted price
        y0: signalPrice, // Signal price as the bottom of the rectangle
        y1: takeProfit, // Take Profit price as the top of the rectangle
        fillcolor: "rgba(0, 255, 0, 0.2)", // Green transparent fill
        line: { width: 0 }, // No border
      },
      // SL (Stop Loss) rectangle
      signalPrice && stopLoss && {
        type: "rect",
        xref: "x",
        yref: "y",
        x0: realPrices[realPrices.length - 1].x, // Start from the last real price
        x1: predictedPrices[predictedPrices.length - 1].x, // End at the last predicted price
        y0: signalPrice, // Signal price as the top of the rectangle
        y1: stopLoss, // Stop Loss price as the bottom of the rectangle
        fillcolor: "rgba(255, 0, 0, 0.2)", // Red transparent fill
        line: { width: 0 }, // No border
      },
    ].filter(Boolean), // Ensure only valid shapes are included

    annotations: [
      // Annotation for the highest price of the week
      {
        x: new Date(), // Current date
        y: high, // Position at the highest price
        xref: "x",
        yref: "y",
        text: `Highest Price: $${high.toFixed(2)}`,
        showarrow: true,
        arrowhead: 6,
        ax: 0,
        ay: -40,
        font: { color: "green" },
      },
      // Annotation for the lowest price of the week
      {
        x: new Date(), // Current date
        y: low, // Position at the lowest price
        xref: "x",
        yref: "y",
        text: `Lowest Price: $${low.toFixed(2)}`,
        showarrow: true,
        arrowhead: 6,
        ax: 0,
        ay: 40,
        font: { color: "red" },
      },
    ],
  };

  // console.log("Layout Update:", layoutUpdate); // Debugging layout updates

  // Call the updatePlot function to update the chart with the new data and layout
  updatePlot('tradingChart', dataTraces, layoutUpdate);

  // Call the updateSignalDisplay function to update the signal display (e.g., Buy/Sell signals)
  updateSignalDisplay(data);
};
