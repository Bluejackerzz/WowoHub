predictButton.addEventListener('click', async () => {
    const text = userText.value;

    // Check if input is not empty
    if (text.trim() === '') {
        alert("Please enter some text!");
        return;
    }

    // Send request to Flask API
    const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
    });

    // Get response and display results
    const data = await response.json();
    const probabilities = data.probabilities;
    const labels = data.labels;

    // Get top 3 predictions
    const topPredictions = probabilities
        .map((prob, index) => ({ label: labels[index], probability: prob }))
        .sort((a, b) => b.probability - a.probability) // Sort by highest probability
        .slice(0, 3); // Get the top 3 predictions

    // Prepare data for the chart
    const chartData = {
        labels: topPredictions.map(p => p.label), // Top 3 labels
        datasets: [{
            label: 'Political Leaning',
            data: topPredictions.map(p => p.probability * 100), // Convert probabilities to percentage
            backgroundColor: ['#ff9f00', '#00bfff', '#32cd32'], // Colors for bars
            borderColor: ['#ff7f00', '#0080ff', '#228b22'],  // Darker border colors
            borderWidth: 1
        }]
    };

    // Hide the previous chart and clear the canvas if necessary
    const ctx = document.getElementById('predictionChart').getContext('2d');
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height); // Clear any existing chart
    predictionResult.style.display = 'none'; // Hide the previous chart before showing the new one

    // Create the chart
    new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100, // Ensure max value is 100
                    ticks: {
                        stepSize: 10
                    }
                }
            }
        });

    // Show the prediction result with a slight delay to make the chart load first
    setTimeout(() => {
        predictionResult.style.display = 'block'; // Show the chart after creation
    }, 500);

    // Reset the input field for the next input
    userText.value = '';
});


// Add page transition effects when switching between pages
window.addEventListener('beforeunload', () => {
    document.body.classList.add('fade-out');
});

// Remove fade-out class once the page is fully loaded again
window.addEventListener('load', () => {
    document.body.classList.remove('fade-out');
});


const fileInput = document.getElementById('fileInput');
const uploadButton = document.getElementById('uploadButton');

uploadButton.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a file!');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload_sentiment', {
            method: 'POST',
            body: formData,
        });

        // Check if the response is JSON
        const contentType = response.headers.get('Content-Type');
        if (contentType && contentType.includes('application/json')) {
            const result = await response.json();
            console.log('Sentiment analysis result:', result);
            // Process the result (e.g., display the sentiment)
        } else {
            const text = await response.text();
            console.error('Non-JSON response:', text);
            alert(`Unexpected response from the server: ${text}`);
        }
    } catch (error) {
        console.error('Error uploading file:', error);
        alert('An error occurred while uploading the file.');
    }
});


form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please upload a CSV file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload_sentiment', {  // Use /upload_sentiment here
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.error}`);
            return;
        }

        const data = await response.json();
        console.log("Response Data:", data);  // Log the response

        const labels = Object.keys(data);
        const percentages = Object.values(data);

        // Prepare the chart
        if (chartInstance) {
            chartInstance.destroy();
        }
        const ctx = resultsChart.getContext('2d');
        chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: 'Sentiment Distribution',
                    data: percentages,
                    backgroundColor: ['skyblue', 'lightcoral', 'lightgreen'],
                    borderColor: ['dodgerblue', 'red', 'green'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });

        resultsDiv.style.display = 'block';
    } catch (error) {
        alert(`An error occurred: ${error.message}`);
    }
});
