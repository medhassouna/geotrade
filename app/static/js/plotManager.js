// plotManager.js

// Function to update the Plotly chart
// 'chartId' is the ID of the chart DOM element, 'dataTraces' contains the data to plot, and 'layoutUpdate' contains layout changes
export const updatePlot = (chartId, dataTraces, layoutUpdate) => {
  const chart = document.getElementById(chartId); // Get the chart element by ID

  // Check if the chart already has data (if it's been initialized)
  if (chart.data) {
    // Preserve the current x and y axis ranges to avoid resetting the zoom level
    const chartLayout = chart.layout;
    layoutUpdate.xaxis = { range: chartLayout.xaxis.range, autorange: false };
    layoutUpdate.yaxis = { range: chartLayout.yaxis.range, autorange: false };
    // Update the existing chart with new data and layout changes
    Plotly.update(chartId, dataTraces, layoutUpdate);
  } else {
    // If the chart hasn't been initialized yet, create a new one with the provided layout
    const layout = {
      title: "ETH/USD Trading Chart", // Chart title
      xaxis: { title: "Date/Time" }, // X-axis title (time)
      yaxis: { title: "Price (USD)", tickprefix: "$", showline: true, zeroline: false }, // Y-axis (price)
      yaxis2: { title: "RSI", overlaying: "y", side: "right", range: [0, 100] }, // Secondary y-axis for RSI
      shapes: layoutUpdate.shapes, // Shapes (e.g., TP/SL rectangles)
      annotations: layoutUpdate.annotations, // Annotations (e.g., high/low prices)
      legend: { orientation: "h", x: 0.5, y: -0.3, xanchor: "center", yanchor: "bottom" }, // Horizontal legend
    };
    // Create the new chart using Plotly.react (optimized for reactivity)
    Plotly.react(chartId, dataTraces, layout);
  }
};
