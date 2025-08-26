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
                    <td>${formatDate(entry.date)}</td>
                    <td>${entry.username}</td>
                `;

                historyTable.appendChild(row);
            })
        })
        .catch(error => console.error(error));
}

function formatDate(dateString) {
    const date = new Date(dateString)
    dateString = date.toLocaleString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit"
    })

    return dateString
}

updateHistory();
