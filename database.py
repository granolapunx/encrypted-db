import os
import sqlite3
from cryptography.fernet import Fernet
from key_derivation import derive_key

def init_db(db_path: str): #This function initializes the database and creates the necessary tables.
    """Initializes the database and creates the necessary tables."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE if NOT EXISTS Records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            encrypted_data BLOB NOT NULL,
            salt BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()

init_db("records.db")

def insert_record(db_path: str, data: str, password: str): #This function inserts a new record into the database with encrypted data using the provided password.
    """Inserts a new record into the database with encrypted data."""
    salt = os.urandom(16)
    key = derive_key(password, salt)
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Records (encrypted_data, salt) VALUES (?, ?)",
        (encrypted_data, salt)
    )
    conn.commit()
    conn.close()

def retrieve_records(db_path: str, password: str): #This function retrieves and decrypts all records from the database using the provided password.
    """Retrieves and decrypts all records from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT encrypted_data, salt FROM Records")
    records = cursor.fetchall()
    conn.close()
    
    decrypted_records = []
    for encrypted_data, salt in records:
        key = derive_key(password, salt)
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data).decode()
        decrypted_records.append(decrypted_data)
    
    return decrypted_records

## This is a test to see if the database functions work correctly when the module is imported.