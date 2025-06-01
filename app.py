from flask import Flask, request, jsonify, send_file
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешить CORS

def init_db():
    conn = sqlite3.connect('submissions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            product TEXT,
            comment TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    try:
        conn = sqlite3.connect('submissions.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO submissions (name, email, phone, product, comment)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['name'], data['email'], data['phone'], data['product'], data.get('comment', '')))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Данные успешно сохранены!'})
    except Exception as e:
        return jsonify({'message': f'Ошибка: {str(e)}'}), 500

@app.route('/download-db')
def download_db():
    return send_file('submissions.db', as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)
