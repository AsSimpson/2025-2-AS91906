import json
import os
import time
from tkinter import messagebox

class DataManager:
    """Handles all data operations including leaderboard, player data, and store"""
    
    def __init__(self):
        self.leaderboard = self.load_leaderboard()
        self.player_gold_coins = self.load_player_gold_coins()
        self.store_items = {
            "Extra Life": {"price": 50, "description": "Add 1 extra life to your game"},
            "Time Extension": {"price": 30, "description": "Add 5 seconds to timer"},
            "Score Multiplier": {"price": 100, "description": "Double points for 3 questions"},
            "Hint System": {"price": 75, "description": "Get hints for difficult questions"}
        }

    def load_leaderboard(self):
        """Load leaderboard from file"""
        if os.path.exists("leaderboard.json"):
            try:
                with open("leaderboard.json", "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    def load_player_gold_coins(self):
        """Load player gold coins from file"""
        if os.path.exists("player_gold_coins.json"):
            try:
                with open("player_gold_coins.json", "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_player_gold_coins(self):
        """Save player gold coins to file"""
        try:
            with open("player_gold_coins.json", "w") as f:
                json.dump(self.player_gold_coins, f)
        except:
            messagebox.showerror("Error", "Failed to save player gold coins!")

    def get_player_gold_coins(self, player_name):
        """Get gold coins for specific player"""
        return self.player_gold_coins.get(player_name, 0)

    def add_gold_coins(self, player_name, amount):
        """Add gold coins to specific player"""
        if player_name not in self.player_gold_coins:
            self.player_gold_coins[player_name] = 0
        self.player_gold_coins[player_name] += amount
        self.save_player_gold_coins()

    def update_leaderboard(self, player_name, score, difficulty):
        """Update leaderboard with current score"""
        self.leaderboard.append({
            "player_name": player_name,
            "score": score,
            "difficulty": difficulty,
            "timestamp": time.ctime()
        })
        self.leaderboard = sorted(self.leaderboard, key=lambda x: x["score"], reverse=True)[:5]
        try:
            with open("leaderboard.json", "w") as f:
                json.dump(self.leaderboard, f)
        except:
            messagebox.showerror("Error", "Failed to save leaderboard!")

    def delete_all_records(self):
        """Delete all leaderboard records"""
        if not self.leaderboard:
            return False, "No records to delete."
        
        self.leaderboard = []
        try:
            with open("leaderboard.json", "w") as f:
                json.dump(self.leaderboard, f)
            return True, "All leaderboard records have been deleted successfully!"
        except:
            return False, "Failed to delete records!"

    def buy_item(self, player_name, item_name):
        """Buy item from store"""
        if item_name in self.store_items:
            price = self.store_items[item_name]["price"]
            player_coins = self.get_player_gold_coins(player_name)
            if player_coins >= price:
                self.player_gold_coins[player_name] -= price
                self.save_player_gold_coins()
                return True, f"You bought {item_name} for {price} coins!"
            else:
                return False, f"You need {price} coins to buy {item_name}!"
        return False, "Item not found!"

    def calculate_coins_earned_in_game(self, player_name, score, game_mode):
        """Calculate gold coins earned during this game session"""
        if not player_name:
            return 0
        
        if game_mode == "square_root":
            return max(1, score // 5)
        elif game_mode == "integration":
            return max(1, score // 15)
        elif game_mode == "pokemon_battle":
            return max(1, score // 8)
        else:
            correct_answers = score // 10
            combo_bonuses = (correct_answers // 3) * 5
            return (correct_answers * 2) + combo_bonuses 