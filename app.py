from flask import Flask, render_template, request, jsonify
import sqlite3
import datetime
import moment

app = Flask(__name__)
DATABASE = 'balances.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
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

create_table()

@app.route('/accounts')
def get_accounts():
    try:
        conn = get_db_connection()
        accounts = conn.execute('SELECT DISTINCT account_name FROM balances').fetchall()
        conn.close()
        return jsonify([{'account_name': row['account_name']} for row in accounts])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            account_name = request.form['account_name']
            balance = float(request.form['balance']) 
            date = datetime.date.today().strftime("%Y-%m-%d") 

            conn = get_db_connection()
            conn.execute('INSERT INTO balances (account_name, balance, date) VALUES (?,?,?)', 
                         (account_name, balance, date))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Account updated successfully'}), 201 
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    conn = get_db_connection()
    accounts = conn.execute('SELECT DISTINCT account_name FROM balances').fetchall()
    conn.close()
    return render_template('index.html', accounts=accounts)

@app.route('/data')
def data():
    try:
        conn = get_db_connection()
        data = conn.execute('SELECT * FROM balances ORDER BY date').fetchall()
        conn.close()

        chart_data = {}
        for row in data:
            data_dict = dict(row)
            if data_dict['account_name'] not in chart_data:
                chart_data[data_dict['account_name']] = {'x':[], 'y':[]}
            parsed_date = moment(data_dict['date'], "YYYY-MM-DD").format() 
            chart_data[data_dict['account_name']]['x'].append(parsed_date)
            chart_data[data_dict['account_name']]['y'].append(data_dict['balance'])
        return jsonify(chart_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
