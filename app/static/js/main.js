// main.js

import { initializeSocket } from './socketHandler.js'; // Handles WebSocket initialization and data fetching
import { updateChart } from './chartUpdater.js'; // Updates the chart with data

// Create a WebSocket connection using Socket.IO
const socket = io();

window.onload = function () {
  // Initialize WebSocket and start listening for updates
  initializeSocket(socket, updateChart);
};
