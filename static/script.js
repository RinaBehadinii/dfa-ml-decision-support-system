let weatherCategory = null;

fetch('/recommend', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({})
}).then(response => response.json()).then(data => {
    if (data.weather) {
        const weatherInfo = `Current Weather: ${data.category} (Temp: ${data.weather.temperature}°C, Wind: ${data.weather.windspeed} km/h)`;
        document.getElementById('weatherInfo').innerText = weatherInfo;
        weatherCategory = data.category;
        document.getElementById('recommendButton').disabled = false;
    } else {
        document.getElementById('weatherInfo').innerText = `Error: ${data.status}`;
    }
});

document.getElementById('recommendButton').addEventListener('click', function () {
    fetch('/recommend', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({})
    }).then(response => response.json()).then(data => {
        if (data.status === 'Accepted') {
            document.getElementById('result').innerText = 'Accepted Outfit: ' + data.outfit.join(', ');
            document.getElementById('feedbackForm').style.display = 'block';
            document.getElementById('top').value = data.outfit[0];
            document.getElementById('bottom').value = data.outfit[1];
            document.getElementById('outerwear').value = data.outfit[2];
        } else {
            document.getElementById('result').innerText = 'Error: ' + data.status;
        }
    });
});

document.getElementById('feedbackForm').addEventListener('submit', function (e) {
    e.preventDefault();
    fetch('/feedback', {
        method: 'POST',
        body: new URLSearchParams(new FormData(e.target))
    }).then(() => {
        alert('Feedback submitted. Thank you!');
        document.getElementById('feedbackForm').reset();
    });
});

