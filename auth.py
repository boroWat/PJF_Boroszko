import hashlib
import csv
import os

import pandas as pd


# Define the path to the CSV file
users_csv_path = os.path.join('data', 'users.csv')

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register_user(username, password, role, IdMenago, IdDyr):
    user_id = generate_new_user_id()  # You need to implement this function
    password_hash = hash_password(password)
    with open(users_csv_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, username, password_hash, role, IdMenago, IdDyr])
    print(f"User {username} registered successfully.")

def check_login(username, password):
    password_hash = hash_password(password)
    with open(users_csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Username'] == username and row['PasswordHash'] == password_hash:
                print(f"User {username} logged in successfully.")
                return True
    print("Invalid username or password.")
    return False

def generate_new_user_id():
    users_csv_path = os.path.join('data', 'users.csv')
    
    # Check if the CSV file exists and is not empty
    if os.path.exists(users_csv_path) and os.path.getsize(users_csv_path) > 0:
        users_df = pd.read_csv(users_csv_path)

        # Ensure the UserID column exists and has at least one entry
        if 'UserID' in users_df.columns and not users_df['UserID'].empty:
            # Find the max UserID, increment by 1 and return
            return str(users_df['UserID'].max() + 1)
        else:
            # If the UserID column is empty, start from 1
            return "1"
    else:
        # If the file doesn't exist or is empty, start with UserID 1
        return "1"

