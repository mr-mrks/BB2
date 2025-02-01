from flask import Flask, render_template, request, jsonify
import sqlite3
import datetime
import moment  # Added for date parsing

app = Flask(__name__)
DATABASE = 'balances.db'  # SQLite database file

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            balance REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table() # Create table if not exists

@app.route('/accounts')
def get_accounts():
    conn = get_db_connection()
    accounts = conn.execute('SELECT DISTINCT account_name FROM balances').fetchall()
    conn.close()
    return jsonify(accounts)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        account_name = request.form['account_name']
        balance = float(request.form['balance'])
        date = datetime.date.today().strftime("%Y-%m-%d") # ISO format for easy sorting

        conn = get_db_connection()
        conn.execute('INSERT INTO balances (account_name, balance, date) VALUES (?, ?, ?)', (account_name, balance, date))
        conn.commit()
        conn.close()
        return "Account updated" # or a redirect for better UX

    conn = get_db_connection()
    accounts = conn.execute('SELECT DISTINCT account_name FROM balances').fetchall()
    conn.close()
    return render_template('index.html', accounts=accounts)


@app.route('/data')
def data():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM balances ORDER BY date').fetchall()
    conn.close()

    # Prepare data for Chart.js (example)
    chart_data = {}
    for row in data:
        if row['account_name'] not in chart_data:
            chart_data[row['account_name']] = {'x': [], 'y': []}
        # Use moment.js for date parsing (assuming YYYY-MM-DD format)
        parsed_date = moment(row['date'], "YYYY-MM-DD").format()  
        chart_data[row['account_name']]['x'].append(parsed_date)
        chart_data[row['account_name']]['y'].append(row['balance'])
    return jsonify(chart_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') # Accessible from network
