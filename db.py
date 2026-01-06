# db.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",              # 🔁 Replace if you use a different username
        password="",              # 🔁 Add password if you set one in phpMyAdmin
        database="yogatune_db"       # ✅ The name of the database you created
    )
