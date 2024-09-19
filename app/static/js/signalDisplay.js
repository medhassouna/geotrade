// signalDisplay.js

// Function to update Buy/Sell signals display
// It updates the UI to reflect the current trading signal (Buy/Sell) and related information
export const updateSignalDisplay = (data) => {
  const signalText = document.getElementById("signal");
  const signalBox = document.getElementById("signalBox");

  // If there's no valid signal, hide the signal box
if (!data.signal || data.signal === "Hold") {
  signalBox.style.display = "none"; // Hide signal box if no signal or Hold signal
} else {
  // Display the signal and update the class based on whether it's a Buy or Sell signal
  signalBox.style.display = "block";
  signalBox.className = data.signal.includes("Sell") ? "sell" : "buy"; // Apply class based on signal

  // Just use the signal as it is, since it already contains the confidence level
  signalText.textContent = data.signal;

  // Set text color based on the signal type
  signalText.style.color = data.signal.includes("Sell") ? "red" : "green";
}


  // Set volatility
  document.getElementById("volatility").textContent = `Volatility: ${data.volatility ? data.volatility.toFixed(2) : "N/A"}`;

  // Update the predicted price display (if available), or show "N/A"
  document.getElementById("predicted_price").textContent = `Predicted Price: ${data.predicted_price ? data.predicted_price.toFixed(2) : "N/A"}`;

  // Update the current price display (if available), or show "N/A"
  document.getElementById("current_price").textContent = `Current Price: ${data.current_price ? data.current_price.toFixed(2) : "N/A"}`;

  // Update the RSI value display (if available), or show "N/A"
  document.getElementById("rsi_value").textContent = `Relative Strength Index: ${data.rsi && data.rsi.length > 0 ? data.rsi[data.rsi.length - 1].toFixed(2) : "N/A"}`;

  // Update the entry price display if there's a Buy or Sell signal, otherwise show "N/A"
  document.getElementById("entry_price").textContent = `Entry Price: ${data.signal && data.entry_price ? data.entry_price.toFixed(2) : "N/A"}`;

  // Update the stop loss display (if available), or show "N/A"
  document.getElementById("stop_loss").textContent = `Stop Loss: ${data.stop_loss ? data.stop_loss.toFixed(2) : "N/A"}`;

  // Update the take profit display (if available), or show "N/A"
  document.getElementById("take_profit").textContent = `Take Profit: ${data.take_profit ? data.take_profit.toFixed(2) : "N/A"}`;
};


