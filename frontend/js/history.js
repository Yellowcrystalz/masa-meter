function updateHistory() {
    fetch("/api/history")
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response failed " + response.statusText);
            }

            return response.json();
        })
        .then(data => {
            const historyTable = document.querySelector(".history");
            historyTable.innerHTML = "";

            data.forEach(entry => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${entry.id}</td>
                    <td>${entry.date}</td>
                    <td>${entry.username}</td>
                `;

                historyTable.appendChild(row);
            })
        })
        .catch(error => console.error(error));
}

updateHistory();
setInterval(updateHistory, 5000);
