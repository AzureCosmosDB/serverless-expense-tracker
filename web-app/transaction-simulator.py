import requests
import random

TRANSACTION_URL = "http://localhost:7071/api/SubmitTransaction"
users = ["User1", "User2"]
categories = ["Food", "Shopping", "Entertainment"]

for _ in range(10):
    data = {
        "userId": random.choice(users),
        "amount": random.randint(50, 1500),
        "category": random.choice(categories)
    }
    requests.post(TRANSACTION_URL, json=data)
