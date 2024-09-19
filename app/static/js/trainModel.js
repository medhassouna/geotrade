document.getElementById('trainButton').addEventListener('click', function() {
    const selectedModel = document.getElementById('modelSelector').value;

    // Show progress bar
    document.getElementById('progressContainer').style.display = 'block';

    // Send request to start training
    const socket = io();  // Assuming Socket.IO is used for real-time communication
    socket.emit('start_training', { model: selectedModel });

    // Update the progress bar
    socket.on('training_progress', (progress) => {
        document.getElementById('trainingProgress').value = progress;
        document.getElementById('progressPercent').textContent = `${progress}%`;
    });

    // Handle training completion
    socket.on('training_complete', () => {
        alert('Model training completed!');
        document.getElementById('trainingProgress').value = 100;
        document.getElementById('progressPercent').textContent = '100%';
    });
});
