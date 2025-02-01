const accountSelect = document.getElementById('account_select');
const updateForm = document.getElementById('updateForm');
const accountNameInput = document.getElementById('account_name');
const balanceInput = document.getElementById('balance');
const balanceChart = document.getElementById('balanceChart').getContext('2d');

fetch('/accounts')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(accounts => {
        accounts.forEach(account => {
            const option = document.createElement('option');
            option.value = account.account_name;
            option.text = account.account_name;
            accountSelect.appendChild(option);
        });

        accountSelect.addEventListener('change', () => {
            const selectedAccount = accountSelect.value;
            accountNameInput.value = selectedAccount; 
            updateForm.style.display = 'block'; 
        });
    })
    .catch(error => {
        console.error('Error fetching accounts:', error);
        // Display an error message to the user (e.g., using an alert)
    });

fetch('/data')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const datasets = [];

        for (const account in data) {
            datasets.push({
                label: account,
                data: data[account].y,
                xLabels: data[account].x,
                borderColor: getRandomColor(),
                fill: false
            });
        }

        const myChart = new Chart(balanceChart, {
            type: 'line',
            data: {
                datasets: datasets
            },
            options: {
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            parser: 'YYYY-MM-DD', 
                            unit: 'day', 
                            displayFormats: {
                                day: 'MMM D' 
                            }
                        },
                        stacked: true 
                    },
                    y: { stacked: true }
                }
            }
        });
    })
    .catch(error => {
        console.error('Error fetching chart data:', error);
        // Handle the error (e.g., display an error message)
    });

updateForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const accountName = accountNameInput.value;
    const balance = balanceInput.value;

    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ account_name: accountName, balance: balance })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Refresh chart data
        fetch('/data')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(newData => {
                // Update Chart.js data
                myChart.data.datasets.forEach((dataset, index) => {
                    if (dataset.label === accountName) {
                        dataset.data.push(newData[accountName].y[newData[accountName].y.length - 1]);
                        dataset.xLabels.push(newData[accountName].x[newData[accountName].x.length - 1]);
                    }
                });
                myChart.update(); 
            })
            .catch(error => {
                console.error('Error refreshing chart data:', error);
                // Handle the error (e.g., display an error message)
            });
    })
    .catch(error => {
        console.error('Error updating balance:', error);
        // Handle the error (e.g., display an error message)
    });
});

function getRandomColor() {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    return `rgb(${r}, ${g}, ${b})`;
} 
