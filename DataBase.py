import sqlite3
import json

def init_db():
    conn = sqlite3.connect('artifacts.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS artifacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            museum TEXT,
            city TEXT,
            country TEXT,
            latitude REAL,
            longitude REAL,
            status TEXT,
            year_taken INTEGER,
            description TEXT
        )
    ''')
    
    # Insert sample data
    sample_artifacts = [
        ('Rosetta Stone', 'British Museum', 'London', 'United Kingdom', 
         51.5194, -0.1270, 'Contested', 1801, 'Key to deciphering hieroglyphs'),
        ('Bust of Nefertiti', 'Neues Museum', 'Berlin', 'Germany',
         52.5200, 13.3967, 'Contested', 1912, 'Famous limestone bust')
    ]
    
    c.executemany('''
        INSERT OR IGNORE INTO artifacts 
        (name, museum, city, country, latitude, longitude, status, year_taken, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_artifacts)
    
    conn.commit()
    conn.close()

def get_all_artifacts():
    conn = sqlite3.connect('artifacts.db')
    c = conn.cursor()
    c.execute('SELECT * FROM artifacts')
    artifacts = c.fetchall()
    conn.close()
    return artifacts