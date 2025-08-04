import json
import time

class LivesSystem:
    """Class to handle lives system for both player and enemy"""
    
    def __init__(self, max_lives=3):
        self.max_lives = max_lives
        self.player_lives = max_lives
        self.enemy_lives = max_lives
    
    def reset_player_lives(self):
        """Reset player lives to maximum"""
        self.player_lives = self.max_lives
    
    def reset_enemy_lives(self):
        """Reset enemy lives to maximum"""
        self.enemy_lives = self.max_lives
    
    def reset_all_lives(self):
        """Reset both player and enemy lives"""
        self.player_lives = self.max_lives
        self.enemy_lives = self.max_lives
    
    def reduce_player_lives(self, amount=1):
        """Reduce player lives by specified amount"""
        self.player_lives = max(0, self.player_lives - amount)
        return self.player_lives
    
    def reduce_enemy_lives(self, amount=1):
        """Reduce enemy lives by specified amount"""
        self.enemy_lives = max(0, self.enemy_lives - amount)
        return self.enemy_lives
    
    def get_player_lives(self):
        """Get current player lives"""
        return self.player_lives
    
    def get_enemy_lives(self):
        """Get current enemy lives"""
        return self.enemy_lives
    
    def is_player_defeated(self):
        """Check if player is defeated (0 lives)"""
        return self.player_lives <= 0
    
    def is_enemy_defeated(self):
        """Check if enemy is defeated (0 lives)"""
        return self.enemy_lives <= 0
    
    def get_player_life_display(self):
        """Get player life display string"""
        return "Lives: " + "❤️ " * self.player_lives
    
    def get_enemy_life_display(self):
        """Get enemy life display string"""
        return "Enemy Lives: " + "💙 " * self.enemy_lives

class GameConfig:
    """Centralized configuration class for all game attributes"""
    
    def __init__(self):
        # Time limits for different game modes
        self.time_limits = {
            "algebra": 20,
            "square_root": 40,
            "integration": 40,
            "differentiation": 40,
            "pokemon_battle": 30
        }
        
        # Lives configuration
        self.max_lives = 3
        self.enemy_max_lives = 3
        
        # Scoring configuration
        self.base_score = 10
        self.streak_bonus = 5
        self.correct_answer_coins = 3
        self.victory_bonus = 50
        
        # Difficulty multipliers
        self.difficulty_multipliers = {
            "easy": 1.0,
            "medium": 1.5,
            "hard": 2.0
        }
        
        # UI Configuration
        self.colors = {
            "easy": "#4CAF50",
            "medium": "#FF9800", 
            "hard": "#f44336",
            "success": "#006400",
            "error": "#8B0000",
            "warning": "#FFD700"
        }
        
        # Sound configuration
        self.sound_enabled = True
        self.correct_sound_freq = 1000
        self.incorrect_sound_freq = 500
        
        # Animation settings
        self.flash_duration = 300  # milliseconds
        self.score_animation_duration = 300
        self.time_warning_threshold = 3
        
        # Game modes
        self.game_modes = ["algebra", "square_root", "integration", "differentiation", "pokemon_battle"]
        self.difficulty_levels = ["easy", "medium", "hard"]
    
    def get_time_limit(self, game_mode):
        """Get time limit for specific game mode"""
        return self.time_limits.get(game_mode, 10)
    
    def set_time_limit(self, game_mode, time_limit):
        """Set time limit for specific game mode"""
        self.time_limits[game_mode] = time_limit
    
    def get_score_multiplier(self, difficulty):
        """Get score multiplier for difficulty level"""
        return self.difficulty_multipliers.get(difficulty, 1.0)
    
    def get_color(self, color_type):
        """Get color for specific type"""
        return self.colors.get(color_type, "#000000")
    
    def update_difficulty_multiplier(self, difficulty, multiplier):
        """Update difficulty multiplier"""
        self.difficulty_multipliers[difficulty] = multiplier
    
    def get_all_config(self):
        """Get all configuration as dictionary"""
        return {
            "time_limits": self.time_limits,
            "max_lives": self.max_lives,
            "enemy_max_lives": self.enemy_max_lives,
            "base_score": self.base_score,
            "difficulty_multipliers": self.difficulty_multipliers,
            "colors": self.colors,
            "sound_enabled": self.sound_enabled,
            "flash_duration": self.flash_duration
        }
    
    def load_config_from_file(self, filename):
        """Load configuration from JSON file"""
        try:
            with open(filename, 'r') as f:
                config_data = json.load(f)
                self.time_limits.update(config_data.get("time_limits", {}))
                self.max_lives = config_data.get("max_lives", 3)
                self.enemy_max_lives = config_data.get("enemy_max_lives", 3)
                self.base_score = config_data.get("base_score", 10)
                self.difficulty_multipliers.update(config_data.get("difficulty_multipliers", {}))
                self.colors.update(config_data.get("colors", {}))
                self.sound_enabled = config_data.get("sound_enabled", True)
                self.flash_duration = config_data.get("flash_duration", 300)
        except FileNotFoundError:
            print(f"Config file {filename} not found, using defaults")
        except json.JSONDecodeError:
            print(f"Invalid JSON in config file {filename}, using defaults")
    
    def save_config_to_file(self, filename):
        """Save configuration to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.get_all_config(), f, indent=2)
        except Exception as e:
            print(f"Failed to save config: {e}")

# Game constants
DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
DIFFICULTY_COLORS = {"easy": "#4CAF50", "medium": "#FF9800", "hard": "#f44336"}
GAME_MODES = ["algebra", "square_root"]

# Time limits for different game modes
ALGEBRA_TIME = 10
SQUARE_ROOT_TIME = 15
INTEGRATION_TIME = 20
DIFFERENTIATION_TIME = 20
POKEMON_BATTLE_TIME = 15 
