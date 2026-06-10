import json
import os
from datetime import datetime, timedelta

class DataManager:
    def __init__(self):
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        self.users_file = f"{self.data_dir}/users.json"
        self.users = self.load_users()
    
    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def save_users(self):
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def get_user(self, user_id):
        user_id = str(user_id)
        if user_id not in self.users:
            self.users[user_id] = {
                "level": "a1",
                "words_learned": {},
                "sentences_learned": [],
                "daily_words": 0,
                "daily_sentences": 0,
                "last_reset": str(datetime.now().date()),
                "score": 0,
                "streak": 0,
                "last_active": str(datetime.now().date()),
                "achievements": [],
                "weak_words": [],
                "weekly_challenges": {},
                "total_study_time": 0,
                "joined_date": str(datetime.now().date())
            }
            self.save_users()
        return self.users[user_id]
    
    def update_user(self, user_id, data):
        self.users[str(user_id)] = data
        self.save_users()
    
    def load_words(self, level):
        try:
            with open(f"{self.data_dir}/words_{level}.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def load_sentences(self, level):
        try:
            with open(f"{self.data_dir}/sentences_{level}.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def get_all_words_count(self):
        count = 0
        for level in ["a1", "a2", "b1", "b2", "c1", "c2"]:
            count += len(self.load_words(level))
        return count
    
    def get_all_sentences_count(self):
        count = 0
        for level in ["a1", "a2", "b1", "b2", "c1", "c2"]:
            count += len(self.load_sentences(level))
        return count