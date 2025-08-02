import json
import os
from datetime import datetime
from hashlib import sha256

# Path to store simulated data
DATA_FILE = "simulated_candidate_data.json"

def anonymize_email(email):
    """Returns a hashed version of the email"""
    return sha256(email.encode()).hexdigest()

def store_candidate_data(candidate_data, responses):
    """Store anonymized candidate data with timestamp"""
    anonymized_data = {
        "id": anonymize_email(candidate_data["email"]),
        "timestamp": datetime.utcnow().isoformat(),
        "experience": candidate_data["experience"],
        "position": candidate_data["position"],
        "location": candidate_data["location"],
        "tech_stack": candidate_data["tech_stack"],
        "responses": responses
    }

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.append(anonymized_data)

    with open(DATA_FILE, "w") as f:
        json.dump(existing_data, f, indent=4)

def delete_all_candidate_data():
    """Simulate GDPR-style deletion"""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)        