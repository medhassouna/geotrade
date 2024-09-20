// socketHandler.js

// Function to initialize the WebSocket connection and request data every 10 seconds
export const initializeSocket = (socket, updateChart, interval = 10000) => {
  // Listen for updates from the server on the "update_chart" event
  socket.on("update_chart", (data) => {
    console.log("Received update from server:", data);
    updateChart(data);
  });

  // Handle connection errors
  socket.on("connect_error", (err) => {
    console.error("Connection error:", err);
  });

  socket.on("disconnect", () => {
    console.warn("Disconnected from server.");
  });

  // Clear any previous interval to prevent multiple intervals
  let requestInterval = setInterval(() => {
    socket.emit("request_data");
    console.log("Requesting data from server...");
  }, interval);

  // Return a function to stop the interval if needed
  return () => clearInterval(requestInterval);
};
