import json
import time

class LivesSystem:
    """Class to handle lives system for both player and enemy"""
    
    def __init__(self, playerMaxLives=3, enemyMaxLives=5):
        self.playerMaxLives = playerMaxLives
        self.enemyMaxLives = enemyMaxLives
        self.playerLives = playerMaxLives
        self.enemyLives = enemyMaxLives
    
    def resetPlayerLives(self):
        # resets player lives back to max
        self.playerLives = self.playerMaxLives
    
    def resetEnemyLives(self):
        # resets enemy lives back to max
        self.enemyLives = self.enemyMaxLives
    
    def resetAllLives(self):
        # resets both player and enemy lives
        self.playerLives = self.playerMaxLives
        self.enemyLives = self.enemyMaxLives
    
    def reducePlayerLives(self, amount=1):
        # reduces player lives by specified amount
        new_lives = self.playerLives - amount
        if new_lives < 0:
            new_lives = 0
        self.playerLives = new_lives
        return self.playerLives
    
    def reduceEnemyLives(self, amount=1):
        # reduces enemy lives by specified amount
        new_lives = self.enemyLives - amount
        if new_lives < 0:
            new_lives = 0
        self.enemyLives = new_lives
        return self.enemyLives
    
    def getPlayerLives(self):
        # gets current player lives
        return self.playerLives
    
    def getEnemyLives(self):
        # gets current enemy lives
        return self.enemyLives
    
    def isPlayerDefeated(self):
        # checks if player is defeated (0 lives)
        if self.playerLives <= 0:
            return True
        else:
            return False
    
    def isEnemyDefeated(self):
        # checks if enemy is defeated (0 lives)
        if self.enemyLives <= 0:
            return True
        else:
            return False
    
    def getPlayerLifeDisplay(self):
        # gets player life display string with hearts
        heart_symbols = ""
        for i in range(self.playerLives):
            heart_symbols = heart_symbols + "❤️ "
        return "Lives: " + heart_symbols
    
    def getEnemyLifeDisplay(self):
        # gets enemy life display string with blue hearts
        heart_symbols = ""
        for i in range(self.enemyLives):
            heart_symbols = heart_symbols + "💙 "
        return "Enemy Lives: " + heart_symbols

class GameConfig:
    """Centralized configuration class for all game attributes"""
    
    def __init__(self):
        # centralized config for all game stuff - keeps things organized
        # Time limits for different game modes
        self.timeLimits = {}
        self.timeLimits["algebra"] = 20
        self.timeLimits["square_root"] = 40
        self.timeLimits["integration"] = 40
        self.timeLimits["differentiation"] = 40
        
        # Lives configuration
        self.maxLives = 3
        self.enemyMaxLives = 5
        
        # Scoring configuration
        self.baseScore = 10
        self.streakBonus = 5
        self.victoryBonus = 50
        
        # Difficulty multipliers
        self.difficultyMultipliers = {}
        self.difficultyMultipliers["easy"] = 1.0
        self.difficultyMultipliers["medium"] = 1.5
        self.difficultyMultipliers["hard"] = 2.0
        
        # UI Configuration
        self.colors = {}
        self.colors["easy"] = "#4CAF50"
        self.colors["medium"] = "#FF9800" 
        self.colors["hard"] = "#f44336"
        self.colors["success"] = "#006400"
        self.colors["error"] = "#8B0000"
        self.colors["warning"] = "#FFD700"
        
        # Sound configuration
        self.soundEnabled = True
        self.correctSoundFreq = 1000
        self.incorrectSoundFreq = 500
        
        # Animation settings
        self.flashDuration = 300  # milliseconds
        self.scoreAnimationDuration = 300
        self.timeWarningThreshold = 3
        
        # Game modes
        self.gameModes = []
        self.gameModes.append("algebra")
        self.gameModes.append("square_root")
        self.gameModes.append("integration")
        self.gameModes.append("differentiation")
        
        self.difficultyLevels = []
        self.difficultyLevels.append("easy")
        self.difficultyLevels.append("medium")
        self.difficultyLevels.append("hard")
    
    def getTimeLimit(self, gameMode):
        # gets time limit for specific game mode
        if gameMode in self.timeLimits:
            return self.timeLimits[gameMode]
        else:
            return 10
    
    def setTimeLimit(self, gameMode, timeLimit):
        # sets time limit for specific game mode
        self.timeLimits[gameMode] = timeLimit
    
    def getScoreMultiplier(self, difficulty):
        # gets score multiplier for difficulty level
        if difficulty in self.difficultyMultipliers:
            return self.difficultyMultipliers[difficulty]
        else:
            return 1.0
    
    def getColor(self, colorType):
        # gets color for specific type
        if colorType in self.colors:
            return self.colors[colorType]
        else:
            return "#000000"
    
    def updateDifficultyMultiplier(self, difficulty, multiplier):
        # updates difficulty multiplier
        self.difficultyMultipliers[difficulty] = multiplier
    
    def getAllConfig(self):
        # gets all configuration as dictionary
        config_dict = {}
        config_dict["time_limits"] = self.timeLimits
        config_dict["max_lives"] = self.maxLives
        config_dict["enemy_max_lives"] = self.enemyMaxLives
        config_dict["base_score"] = self.baseScore
        config_dict["difficulty_multipliers"] = self.difficultyMultipliers
        config_dict["colors"] = self.colors
        config_dict["sound_enabled"] = self.soundEnabled
        config_dict["flash_duration"] = self.flashDuration
        return config_dict
    
    def loadConfigFromFile(self, filename):
        # loads configuration from JSON file
        try:
            file_handle = open(filename, 'r')
            config_data = json.load(file_handle)
            file_handle.close()
            
            # Update time limits
            if "time_limits" in config_data:
                for key, value in config_data["time_limits"].items():
                    self.timeLimits[key] = value
            
            # Update other settings
            if "max_lives" in config_data:
                self.maxLives = config_data["max_lives"]
            if "enemy_max_lives" in config_data:
                self.enemyMaxLives = config_data["enemy_max_lives"]
            if "base_score" in config_data:
                self.baseScore = config_data["base_score"]
            if "difficulty_multipliers" in config_data:
                for key, value in config_data["difficulty_multipliers"].items():
                    self.difficultyMultipliers[key] = value
            if "colors" in config_data:
                for key, value in config_data["colors"].items():
                    self.colors[key] = value
            if "sound_enabled" in config_data:
                self.soundEnabled = config_data["sound_enabled"]
            if "flash_duration" in config_data:
                self.flashDuration = config_data["flash_duration"]
                
        except FileNotFoundError:
            print("Config file " + filename + " not found, using defaults")
        except json.JSONDecodeError:
            print("Invalid JSON in config file " + filename + ", using defaults")
    
    def saveConfigToFile(self, filename):
        # saves configuration to JSON file
        try:
            file_handle = open(filename, 'w')
            json.dump(self.getAllConfig(), file_handle, indent=2)
            file_handle.close()
        except Exception as e:
            print("Failed to save config: " + str(e))

# Game constants - these are used throughout the app
DIFFICULTY_LEVELS = []
DIFFICULTY_LEVELS.append("easy")
DIFFICULTY_LEVELS.append("medium")
DIFFICULTY_LEVELS.append("hard")

DIFFICULTY_COLORS = {}
DIFFICULTY_COLORS["easy"] = "#4CAF50"
DIFFICULTY_COLORS["medium"] = "#FF9800"
DIFFICULTY_COLORS["hard"] = "#f44336"

GAME_MODES = []
GAME_MODES.append("algebra")
GAME_MODES.append("square_root")


 
