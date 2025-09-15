from flask import Flask, render_template, jsonify
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'postgres',
    'port': 5432,
    'database': 'app_reviews',
    'user': 'dbt',
    'password': 'dbt'
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_table_info():
    """Get information about all tables in the analytics schema"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        # Get all tables in the analytics schema
        cursor.execute("""
            SELECT table_name, table_type
            FROM information_schema.tables 
            WHERE table_schema = 'analytics'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        return [{'name': table[0], 'type': table[1]} for table in tables]
    except Exception as e:
        print(f"Error getting table info: {e}")
        return []
    finally:
        conn.close()

def get_table_data(table_name, limit=100):
    """Get data from a specific table"""
    conn = get_db_connection()
    if not conn:
        return None, "Database connection failed"
    
    try:
        cursor = conn.cursor()
        # Get column information
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_schema = 'analytics' AND table_name = %s
            ORDER BY ordinal_position;
        """, (table_name,))
        columns = cursor.fetchall()
        
        # Get data
        cursor.execute(f"SELECT * FROM analytics.{table_name} LIMIT %s;", (limit,))
        rows = cursor.fetchall()
        
        return {
            'columns': [{'name': col[0], 'type': col[1], 'nullable': col[2]} for col in columns],
            'rows': rows,
            'row_count': len(rows)
        }, None
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()

@app.route('/')
def index():
    """Main page showing all available tables"""
    tables = get_table_info()
    return render_template('index.html', tables=tables)

@app.route('/table/<table_name>')
def view_table(table_name):
    """View specific table data"""
    data, error = get_table_data(table_name)
    if error:
        return render_template('error.html', error=error)
    
    return render_template('table.html', 
                         table_name=table_name, 
                         columns=data['columns'], 
                         rows=data['rows'],
                         row_count=data['row_count'])

@app.route('/api/table/<table_name>')
def api_table_data(table_name):
    """API endpoint for table data"""
    data, error = get_table_data(table_name)
    if error:
        return jsonify({'error': error}), 500
    
    return jsonify({
        'table_name': table_name,
        'columns': data['columns'],
        'rows': data['rows'],
        'row_count': data['row_count']
    })

@app.route('/api/tables')
def api_tables():
    """API endpoint for table list"""
    tables = get_table_info()
    return jsonify({'tables': tables})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
