// signalDisplay.js

// Function to update Buy/Sell signals display
export const updateSignalDisplay = (data) => {
  const signalText = document.getElementById("signal");
  const signalBox = document.getElementById("signalBox");

  // Ensure elements are found
  if (!signalText || !signalBox) {
    console.error("Signal display elements not found in the DOM.");
    return;
  }

  // If there's no valid signal or the signal is 'Hold', hide the signal box
  if (!data.signal || data.signal === "Hold") {
    signalBox.style.display = "none";
  } else {
    // Display the signal box for Buy or Sell
    signalBox.style.display = "block";
    signalBox.className = data.signal.includes("Sell") ? "sell" : "buy";

  // Just use the signal as it is, since it already contains the confidence level
  signalText.textContent = data.signal;

    // Set the signal text color based on the type of signal
    signalText.style.color = data.signal.includes("Sell") ? "red" : "green";
  }

  // Helper function to update element by ID or log error if not found
  const updateElementText = (id, text) => {
    const element = document.getElementById(id);
    if (element) {
      element.textContent = text;
    } else {
      console.error(`Element with id '${id}' not found in the DOM.`);
    }
  };

  // Update volatility
  updateElementText("volatility", `Volatility: ${data.volatility ? data.volatility.toFixed(2) : "N/A"}`);

  // Update predicted price
  updateElementText("predicted_price", `Predicted Price: ${data.predicted_price ? data.predicted_price.toFixed(2) : "N/A"}`);

  // Update current price
  updateElementText("current_price", `Current Price: ${data.current_price ? data.current_price.toFixed(2) : "N/A"}`);

  // Update RSI value
  updateElementText("rsi_value", `Relative Strength Index: ${data.rsi && data.rsi.length > 0 ? data.rsi[data.rsi.length - 1].toFixed(2) : "N/A"}`);

  // Update entry price
  updateElementText("entry_price", `Entry Price: ${data.signal && data.entry_price ? data.entry_price.toFixed(2) : "N/A"}`);

  // Update stop loss
  updateElementText("stop_loss", `Stop Loss: ${data.stop_loss ? data.stop_loss.toFixed(2) : "N/A"}`);

  // Update take profit
  updateElementText("take_profit", `Take Profit: ${data.take_profit ? data.take_profit.toFixed(2) : "N/A"}`);
};

// Function to handle model training progress updates
export const handleModelTrainingProgress = (socket) => {
  const trainingProgressBar = document.getElementById('trainingProgressBar');
  const trainingStatusText = document.getElementById('trainingStatus');

  if (!trainingProgressBar || !trainingStatusText) {
    console.error('Training progress elements not found in the DOM.');
    return;
  }

  // Update progress bar when receiving training progress
  socket.on('training_progress', (progress) => {
    trainingProgressBar.value = progress;
    trainingStatusText.textContent = `Training progress: ${progress.toFixed(2)}%`;
  });

  // Handle training completion
  socket.on('training_complete', () => {
    alert('Model training completed!');
    trainingProgressBar.value = 100;
    trainingStatusText.textContent = 'Training complete! 100%';
  });
};

// Function to initialize model training when 'train' button is clicked
export const initializeTrainingButton = (socket) => {
  const trainButton = document.getElementById('trainButton');
  const modelSelector = document.getElementById('modelSelector');

  if (!trainButton || !modelSelector) {
    console.error('Training button or model selector not found in the DOM.');
    return;
  }

  // Add event listener to the train button
  trainButton.addEventListener('click', () => {
    const selectedModel = modelSelector.value;

    // Show the progress bar
    const progressContainer = document.getElementById('progressContainer');
    if (progressContainer) {
      progressContainer.style.display = 'block';
    }

    // Emit the event to start training
    socket.emit('start_training', { model: selectedModel });
  });
};
