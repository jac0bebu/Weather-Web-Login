import json
import os
import bcrypt

# Use absolute path for user file
USER_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json')

# Ensure data directory exists
os.makedirs(os.path.dirname(USER_FILE), exist_ok=True)

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    """Verify password against bcrypt hash"""
    return bcrypt.checkpw(password.encode(), hashed.encode())

def load_users():
    """Load users from JSON file"""
    try:
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r") as file:
                return json.load(file)
    except json.JSONDecodeError:
        # If JSON file is corrupted, backup the old file and create new empty one
        if os.path.exists(USER_FILE):
            backup_file = USER_FILE + '.backup'
            os.rename(USER_FILE, backup_file)
    except Exception as e:
        print(f"Error loading users: {e}")
    
    # Return empty dict if file doesn't exist or on error
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

def initialize_admin():
    """Create default admin account if none exists"""
    users = load_users()
    if "admin@weather.com" not in users:
        users["admin@weather.com"] = {
            "password": hash_password("Admin@123"),
            "role": "admin",
            "username": "Admin",
            "full_name": "Weather Admin"
        }
        save_users(users)
