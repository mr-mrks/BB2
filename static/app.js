// In app.js (create a separate JavaScript file)

const accountSelect = document.getElementById('account_select');
const updateForm = document.getElementById('updateForm');
const accountNameInput = document.getElementById('account_name');
const balanceInput = document.getElementById('balance');

// Fetch initial account list and populate dropdown
fetch('/accounts') 
    .then(response => response.json())
    .then(accounts => {
        accounts.forEach(account => {
            const option = document.createElement('option');
            option.value = account.account_name;
            option.text = account.account_name;
            accountSelect.appendChild(option);
        });

        // Handle account selection
        accountSelect.addEventListener('change', () => {
            const selectedAccount = accountSelect.value;
            accountNameInput.value = selectedAccount; 
            updateForm.style.display = 'block'; 
        });
    });

// ... (rest of your Chart.js code)

// Handle form submission (update balance)
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
    .then(response => response.json())
    .then(data => {
        // Update chart (you might need to refresh the chart data)
        // ... (your chart updating logic)
    });
});
