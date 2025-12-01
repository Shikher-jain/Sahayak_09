import mysql.connector
from mysql.connector import Error

# Fill in your MySQL connection details here
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'sahayak_db'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        return conn
    except Error as e:
        print(f"MySQL connection error: {e}")
        return None

def create_files_table():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS uploaded_files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255),
                filetype VARCHAR(50),
                uploader VARCHAR(100),
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()

def save_file_metadata(filename, filetype, uploader):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO uploaded_files (filename, filetype, uploader)
            VALUES (%s, %s, %s)
        ''', (filename, filetype, uploader))
        conn.commit()
        cursor.close()
        conn.close()

def list_uploaded_files():
    conn = get_db_connection()
    files = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM uploaded_files ORDER BY upload_time DESC')
        files = cursor.fetchall()
        cursor.close()
        conn.close()
    return files

# Call this once at startup
create_files_table()
