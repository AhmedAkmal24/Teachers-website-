"""Test script to verify database connection and authentication.

Run this script to check if users can be properly authenticated.
"""
import os
import sys
import sqlite3
from werkzeug.security import check_password_hash

# Path to the database
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'teachers.sqlite')

def test_database_connection():
    """Test if we can connect to the database and retrieve users."""
    try:
        conn = sqlite3.connect(DB_PATH)
        print(f"Successfully connected to database at {DB_PATH}")
        
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables in database: {[table[0] for table in tables]}")
        
        cursor.execute("SELECT id, name, email, role FROM user")
        users = cursor.fetchall()
        print(f"Found {len(users)} users in database:")
        
        for user in users:
            print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Role: {user[3]}")
        
        return users, conn
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return None, None

def test_password_verification(conn, email, password):
    """Test if a password can be verified against the stored hash."""
    if not conn:
        print("No database connection.")
        return False
    
    try:
        cursor = conn.cursor()
        
        # First, try exact match
        cursor.execute("SELECT id, name, password FROM user WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        # If no exact match, try case-insensitive match
        if not user:
            print(f"No exact match for email: {email}, trying case-insensitive search...")
            cursor.execute("SELECT id, name, password FROM user WHERE LOWER(email) = LOWER(?)", (email,))
            user = cursor.fetchone()
        
        if not user:
            print(f"No user found with email: {email}")
            return False
        
        user_id, name, password_hash = user
        print(f"Testing password for user: {name} (ID: {user_id})")
        
        # Check password
        if check_password_hash(password_hash, password):
            print("Password verification SUCCESS")
            return True
        else:
            print("Password verification FAILED")
            return False
            
    except Exception as e:
        print(f"Error verifying password: {str(e)}")
        return False

def main():
    """Main function to run the tests."""
    print("=== Database Authentication Test ===")
    
    users, conn = test_database_connection()
    if not users or not conn:
        print("Failed to retrieve users from database.")
        return
    
    # Test each user with a test password
    if len(sys.argv) > 2:
        email = sys.argv[1]
        password = sys.argv[2]
        test_password_verification(conn, email, password)
    else:
        # Default test with a known user
        print("\nTesting authentication for sample users...")
        for email, test_password in [
            ('test@example.com', 'password123'),  # Update with actual test data
            ('teacher@example.com', 'teacherpass'),  # Update with actual test data
            ('ahmedakmal2217@gmail.com', 'teacherpass')  # Update with actual test data
        ]:
            print(f"\nTesting login for {email}")
            test_password_verification(conn, email, test_password)
    
    conn.close()

if __name__ == "__main__":
    main()
