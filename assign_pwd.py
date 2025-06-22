import pandas as pd
import json
import hashlib

#hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# load user ids from your dataset

df = pd.read_csv("data/movie_data.csv")
user_ids = df["userId"].unique().astype(str)

#assign default password to all
users = {}
default_password = "password123"
hashed_pw = hash_password(default_password)


for uid in user_ids:
    users[uid] = hashed_pw

#save to users.json
with open("users.json","w") as f:
    json.dump(users,f)

print("All users now have the same default password")
