// MIT License
// 
// Copyright (c) 2025 Justin Nguyen
// 
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

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
setInterval(updateHistory, 300000);
