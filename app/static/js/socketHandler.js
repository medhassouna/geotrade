// socketHandler.js

// Function to initialize the WebSocket connection and request data every 10 seconds
export const initializeSocket = (socket, updateChart) => {
  // Listen for updates from the server on the "update_chart" event
  socket.on("update_chart", updateChart);

  // Request data from the server every 10 seconds
  setInterval(() => {
    socket.emit("request_data");
  }, 10000); // 10 seconds interval
};
