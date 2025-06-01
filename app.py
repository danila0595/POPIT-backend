from flask import Flask, request, jsonify, send_file
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешить CORS

def init_db():
    conn = sqlite3.connect('submissions.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            object_type TEXT NOT NULL,
            heating_duration TEXT NOT NULL,
            floors INTEGER NOT NULL,
            ceiling_height INTEGER NOT NULL,
            heated_area INTEGER,
            heated_volume INTEGER,
            average_temperature INTEGER,
            need_hot_water BOOLEAN,
            people_count INTEGER,
            electricity_cost INTEGER,
            power_capacity INTEGER,
            comments TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.form
    conn = sqlite3.connect('submissions.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO submissions (
            full_name, email, address, phone, object_type,
            heating_duration, floors, ceiling_height,
            heated_area, heated_volume, average_temperature,
            need_hot_water, people_count, electricity_cost,
            power_capacity, comments
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('full_name'),
        data.get('email'),
        data.get('address'),
        data.get('phone'),
        data.get('object_type'),
        data.get('heating_duration'),
        data.get('floors'),
        data.get('ceiling_height'),
        data.get('heated_area') or None,
        data.get('heated_volume') or None,
        data.get('average_temperature') or None,
        data.get('need_hot_water') == 'true',
        data.get('people_count') or None,
        data.get('electricity_cost') or None,
        data.get('power_capacity') or None,
        data.get('comments')
    ))
    conn.commit()
    conn.close()
    return "Спасибо! Данные успешно отправлены."

@app.route('/data')
def show_data():
    conn = sqlite3.connect('submissions.db')
    c = conn.cursor()
    c.execute('SELECT * FROM submissions')
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/download-db')
def download_db():
    return send_file('submissions.db', as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)
