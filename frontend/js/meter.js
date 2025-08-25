function updateMeter() {
    fetch("/api/meter")
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response failed " + response.statusText);
            }

            return response.json();
        })
        .then(data => {
            const meter = data[0].meter;
            const meterElement = document.querySelector(".meter");
            meterElement.textContent = meter;
        })
        .catch(error => console.error(error));
}

updateMeter();
// setInterval(updateMeter, 5000);
