// Function to update the performance chart with accuracy over time
export const updatePerformanceChart = (data) => {
    // Get the performance chart container
    const chartElement = document.getElementById('performanceChart');
  
    // Prepare the new data for the chart
    const performanceData = {
      x: [new Date(data.timestamp)],  // Time when performance was logged
      y: [data.accuracy],             // Accuracy value
      mode: "lines+markers",
      name: "Accuracy over time",
      marker: { color: "blue" }
    };
  
    // If the chart already exists, update it, otherwise create a new one
    if (chartElement.data) {
      Plotly.extendTraces('performanceChart', { x: [[new Date(data.timestamp)]], y: [[data.accuracy]] }, [0]);
    } else {
      const layout = {
        title: 'Model Accuracy Over Time',
        xaxis: { title: 'Timestamp' },
        yaxis: { title: 'Accuracy (%)' },
      };
  
      Plotly.newPlot('performanceChart', [performanceData], layout);
    }
  };
  