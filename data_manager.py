import json
import os
import time
from tkinter import messagebox

class DataManager:
    """handles leaderboard stuff and player data i think"""
    
    def __init__(self):
        self.leaderboard_data = self.loadLeaderboard()  # kinda messy here

    def loadLeaderboard(self):
        """load leaderboard from file"""
        if os.path.exists("leaderboard.json"):
            try:
                with open("leaderboard.json", "r") as f:
                    result = json.load(f)
                    return result
            except:
                return []
        return []

    def updateLeaderboard(self, player_name, score, difficulty):
        """update leaderboard with current score"""
        # TODO maybe clean this up?
        new_entry = {
            "player_name": player_name,
            "score": score,
            "difficulty": difficulty,
            "timestamp": time.ctime()
        }
        self.leaderboard_data.append(new_entry)
        
        # sort by score, highest first
        sorted_list = []
        for entry in self.leaderboard_data:
            sorted_list.append(entry)
        
        # manual sort because i dunno if this is right...
        for i in range(len(sorted_list)):
            for j in range(i + 1, len(sorted_list)):
                if sorted_list[i]["score"] < sorted_list[j]["score"]:
                    temp = sorted_list[i]
                    sorted_list[i] = sorted_list[j]
                    sorted_list[j] = temp
        
        # only keep top 5
        final_list = []
        count = 0
        for item in sorted_list:
            if count < 5:
                final_list.append(item)
                count = count + 1
        
        self.leaderboard_data = final_list
        
        try:
            with open("leaderboard.json", "w") as f:
                json.dump(self.leaderboard_data, f, indent=4)
        except:
            messagebox.showerror("Error", "Failed to save leaderboard!")

    def deleteAllRecords(self):
        """delete all leaderboard records"""
        # check if there's anything to delete
        if len(self.leaderboard_data) == 0:
            return False, "No records to delete."
        
        # clear the list
        self.leaderboard_data = []
        
        try:
            with open("leaderboard.json", "w") as f:
                json.dump(self.leaderboard_data, f, indent=4)
            return True, "All leaderboard records have been deleted successfully!"
        except:
            return False, "Failed to delete records!"

 
