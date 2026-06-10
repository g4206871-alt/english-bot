from datetime import datetime, timedelta

class SpacedRepetition:
    """سیستم مرور با فاصله (Spaced Repetition)"""
    
    INTERVALS = [1, 3, 7, 14, 30]  # روزهای مرور
    
    def __init__(self):
        self.review_data = {}
    
    def add_word(self, user_id, word):
        user_id = str(user_id)
        if user_id not in self.review_data:
            self.review_data[user_id] = {}
        
        self.review_data[user_id][word] = {
            "level": 0,  # سطح مرور (۰ تا ۴)
            "next_review": str(datetime.now().date() + timedelta(days=self.INTERVALS[0])),
            "correct_count": 0,
            "wrong_count": 0,
            "last_reviewed": str(datetime.now().date())
        }
    
    def get_words_for_review(self, user_id):
        """کلماتی که امروز باید مرور شوند"""
        user_id = str(user_id)
        today = str(datetime.now().date())
        review_words = []
        
        if user_id in self.review_data:
            for word, data in self.review_data[user_id].items():
                if data["next_review"] <= today:
                    review_words.append(word)
        
        return review_words
    
    def update_word(self, user_id, word, was_correct):
        user_id = str(user_id)
        if user_id in self.review_data and word in self.review_data[user_id]:
            data = self.review_data[user_id][word]
            
            if was_correct:
                data["correct_count"] += 1
                if data["level"] < len(self.INTERVALS) - 1:
                    data["level"] += 1
            else:
                data["wrong_count"] += 1
                data["level"] = 0  # برگشت به سطح اول
            
            data["last_reviewed"] = str(datetime.now().date())
            data["next_review"] = str(datetime.now().date() + timedelta(days=self.INTERVALS[data["level"]]))
    
    def get_stats(self, user_id):
        user_id = str(user_id)
        if user_id not in self.review_data:
            return {"total": 0, "mastered": 0, "learning": 0}
        
        total = len(self.review_data[user_id])
        mastered = sum(1 for d in self.review_data[user_id].values() if d["level"] >= 4)
        learning = total - mastered
        
        return {"total": total, "mastered": mastered, "learning": learning}