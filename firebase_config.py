import json
import os
from datetime import datetime

DB_FILE = 'data/database.json'

def init_db():
    """Initialize the JSON database"""
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({'users': {}, 'carbon_records': [], 'leaderboard': {}}, f)

def load_db():
    """Load database"""
    init_db()
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    """Save database"""
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def save_user(user_data):
    """Save user"""
    db = load_db()
    db['users'][user_data['email']] = {
        'name': user_data['name'],
        'email': user_data['email'],
        'created_at': datetime.now().isoformat(),
        'total_points': 0,
        'badges': []
    }
    save_db(db)
    return True

def save_carbon_data(email, carbon_data):
    """Save carbon calculation"""
    db = load_db()
    record = {
        'user_email': email,
        'transport': carbon_data.get('transport', 0),
        'energy': carbon_data.get('energy', 0),
        'food': carbon_data.get('food', 0),
        'shopping': carbon_data.get('shopping', 0),
        'waste': carbon_data.get('waste', 0),
        'total_footprint': carbon_data.get('total', 0),
        'date': datetime.now().isoformat(),
        'ai_prediction': carbon_data.get('prediction', ''),
        'ai_tips': carbon_data.get('tips', [])
    }
    db['carbon_records'].append(record)
    save_db(db)
    return True

def get_user_history(email):
    """Get user history"""
    db = load_db()
    history = [r for r in db['carbon_records'] if r['user_email'] == email]
    return history

def get_leaderboard():
    """Get leaderboard"""
    db = load_db()
    user_totals = {}
    for record in db['carbon_records']:
        email = record['user_email']
        if email not in user_totals:
            user_totals[email] = 0
        user_totals[email] += record['total_footprint']
    
    sorted_users = sorted(user_totals.items(), key=lambda x: x[1])
    return sorted_users[:10]

def update_points(email, points):
    """Update points"""
    db = load_db()
    if email in db['users']:
        db['users'][email]['total_points'] = db['users'][email].get('total_points', 0) + points
    save_db(db)
    return True