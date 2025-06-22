import streamlit as st
import json as js
import hashlib as hsh
import os
import pandas as pd

def hash_password(password):
    return hsh.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists('users.json'):
        return {}

    with open('users.json','r') as file:
        return js.load(file)


def save_users(users):
    with open('users.json','w') as file:
        js.dump(users,file)

def authenticate(username,password):
    users = load_users()

    if username in users and users[username] == hash_password(password):
        return True
    return False


def load_known_users():
    df = pd.read_csv(r"C:\Users\neelh\Jupyter Related\Recsys project\data\movie_data.csv")
    return set(df['userId'].unique()) #set for fast lookup

def register_user(username,password):
    users = load_users()

    known_users = load_known_users()

    if username not in known_users: #checks the username in users
        return False

    if username in users:
        return False


    users[username] = hash_password(password)

    save_users(users)
    return True





