function updateLeaderboard() {
    fetch("/api/leaderboard")
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response failed " + response.statusText);
            }

            return response.json();
        })
        .then(data => {
            const historyTable = document.querySelector(".leaderboard");
            historyTable.innerHTML = "";

            var position = 1;
            data.forEach(entry => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${position}</td>
                    <td>${entry.username}</td>
                    <td>${entry.count}</td>
                `;

                historyTable.appendChild(row);
                position++;
            })
        })
        .catch(error => console.error(error));
}

updateLeaderboard();
setInterval(updateLeaderboard, 5000);
