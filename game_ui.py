import tkinter as tk
from tkinter import messagebox
import random
import time
import math
from PIL import Image, ImageTk
from question import *

from game_core import LivesSystem, GameConfig, DIFFICULTY_LEVELS, DIFFICULTY_COLORS, GAME_MODES
from game_core import ALGEBRA_TIME, SQUARE_ROOT_TIME, INTEGRATION_TIME, DIFFERENTIATION_TIME, POKEMON_BATTLE_TIME
from data_manager import DataManager
from game_logic import GameLogic
import utils

class MathGame:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.initialize_variables()
        self.load_data()
        self.setup_styles()
        self.create_start_menu()

    def setup_window(self):
        """Initialize the main window"""
        self.root.title("Math Master")
        self.root.geometry("1152x768")  # Scaled down 3:2 ratio (75% of original)
        
        # Load and resize background image to fit window
        try:
            original_bg = Image.open("assets/pokemon_bg3.png")
            # Scale down for better performance while maintaining aspect ratio
            self.bg_image = original_bg.resize((1152, 768), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        except:
            print("Background image not found, using default background")
            self.bg_photo = None

    def initialize_variables(self):
        """Initialize game variables"""
        self.score = 0
        self.streak = 0
        self.lives_system = LivesSystem(3)  # Initialize lives system
        self.time_left = 10
        self.difficulty = "easy"
        self.current_answer = 0
        self.timer_id = None
        self.player_name = ""
        self.timer_frozen = False
        self.frozen_time_left = 0

    def load_data(self):
        """Load game data from files"""
        self.data_manager = DataManager()
        self.game_logic = GameLogic(self.data_manager, utils)

    def setup_styles(self):
        """Setup fonts and colors for consistent UI"""
        self.title_font = ("Comic Sans MS", 20, "bold")
        self.button_font = ("Comic Sans MS", 12)
        self.label_font = ("Comic Sans MS", 14)
        self.bg_color = "#F4F4F4"
        self.button_color = "#4CAF50"
        self.root.configure(bg=self.bg_color)

    def draw_background(self):
        """Draw background image on window"""
        if self.bg_photo:
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.root.configure(bg="#87CEEB")  # Sky blue fallback

    def create_centered_frame(self):
        """Create a centered frame for content"""
        frame = tk.Frame(self.root, bg="#4EC7D7")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        return frame

    def clear_window(self):
        """Clear all widgets from window"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_start_menu(self):
        """Create the main menu"""
        self.clear_window()
        self.draw_background()
        
        start_frame = self.create_centered_frame()
        
        tk.Label(start_frame, text="Math Master", font=self.title_font).grid(row=0, column=0, pady=20)
        
        buttons = [
            ("START GAME", "#4CAF50", "white", self.show_username_page),
            ("View Leaderboard", self.button_color, "white", self.show_leaderboard),
            ("Exit", "#f44336", "white", self.quit_game)
        ]
        
        for i, (text, bg, fg, command) in enumerate(buttons, 1):
            tk.Button(start_frame, text=text, font=self.button_font, bg=bg,
                     fg=fg, command=command).grid(row=i, column=0, pady=10)

    def show_username_page(self):
        """Show username input page"""
        self.clear_window()
        self.root.configure(bg="#4CC7D8")    # Light blue background
        
        username_frame = self.create_centered_frame()
        
        tk.Label(username_frame, text="Enter Your Name", font=self.title_font).grid(row=0, column=0, pady=20)
        tk.Label(username_frame, text="Please enter your name to start the game:", 
                font=self.label_font).grid(row=1, column=0, pady=10)
        
        self.username_entry = tk.Entry(username_frame, font=self.label_font, width=20)
        self.username_entry.grid(row=2, column=0, pady=10)
        self.username_entry.focus()
        self.username_entry.bind("<Return>", self.validate_username)
        
        buttons = [
            ("Continue", self.button_color, "white", self.validate_username),
            ("Back to Menu", "#f44336", "white", self.create_start_menu)
        ]
        
        for i, (text, bg, fg, command) in enumerate(buttons, 3):
            tk.Button(username_frame, text=text, font=self.button_font, bg=bg,
                     fg=fg, command=command).grid(row=i, column=0, pady=10)

    def validate_username(self, event=None):
        """Validate username input"""
        username = self.username_entry.get().strip()
        is_valid, error_message = utils.validate_username(username)
        
        if not is_valid:
            messagebox.showwarning("Name Required", error_message)
            return
        
        self.player_name = username
        self.show_difficulty_selection()

    def show_difficulty_selection(self):
        """Show difficulty selection page"""
        self.clear_window()
        self.root.configure(bg="#4CC7D8")  # Light blue background
        
        difficulty_frame = self.create_centered_frame()
        
        # Header
        tk.Label(difficulty_frame, text=f"Welcome, {self.player_name}!", 
                font=self.title_font).grid(row=0, column=0, pady=10)
        
        player_coins = self.data_manager.get_player_gold_coins(self.player_name)
        tk.Label(difficulty_frame, text=f"💰 Gold Coins: {player_coins}", 
                font=self.label_font, fg="#FFD700").grid(row=1, column=0, pady=5)
        
        tk.Label(difficulty_frame, text="Select Difficulty:", 
                font=self.label_font).grid(row=2, column=0, pady=10)
        
        # Difficulty buttons
        self.difficulty_var = tk.StringVar(value="none")
        difficulty_buttons_frame = tk.Frame(difficulty_frame)
        difficulty_buttons_frame.grid(row=3, column=0, pady=10)
        
        for i, difficulty in enumerate(DIFFICULTY_LEVELS):
            # Set different text colors based on difficulty
            if difficulty == "easy":
                text_color = "darkgreen"
            elif difficulty == "hard":
                text_color = "red"
            else:
                text_color = "white"
            
            tk.Button(difficulty_buttons_frame, text=difficulty.capitalize(), 
                     font=self.title_font, bg="#FF6700", fg=text_color,
                     width=15, height=2, 
                     command=lambda d=difficulty: self.select_difficulty(d)).grid(row=i, column=0, pady=8)
        
        # Action buttons
        action_buttons_frame = tk.Frame(difficulty_frame)
        action_buttons_frame.grid(row=4, column=0, pady=10)
        
        action_buttons = [
            ("Store", self.show_store),
            ("Back", self.show_username_page)
        ]
        
        for i, (text, command) in enumerate(action_buttons):
            tk.Button(action_buttons_frame, text=text, font=self.button_font,
                     width=10, command=command).grid(row=0, column=i, padx=5)

    def select_difficulty(self, difficulty_level):
        """Select difficulty and go to test selection"""
        self.difficulty = difficulty_level
        self.difficulty_var.set(difficulty_level)
        self.show_difficulty_tests()

    def show_difficulty_tests(self):
        """Validate difficulty and show test selection"""
        if not self.difficulty or self.difficulty not in DIFFICULTY_LEVELS:
            messagebox.showwarning("Difficulty Required", "Please select a difficulty level first!")
            return
        
        self.show_test_window()

    def show_test_window(self):
        """Show test selection window"""
        self.clear_window()
        self.root.configure(bg="#E3F2FD")  # Light blue background
        
        test_frame = self.create_centered_frame()
        
        difficulty_display = self.difficulty.capitalize()
        tk.Label(test_frame, text=f"{difficulty_display} Difficulty Tests", 
                font=self.title_font).grid(row=0, column=0, pady=10)
        tk.Label(test_frame, text=f"Player: {self.player_name}", 
                font=self.label_font).grid(row=1, column=0, pady=5)
        
        # Test buttons
        test_buttons = [
            ("Algebra", self.button_color, "white", self.start_game),
            ("Square Root Challenge", self.button_color, "white", self.start_square_root_game),
            ("Integration", self.button_color, "white", self.start_integration_game),
            ("Differentiation", self.button_color, "white", self.start_differentiation_game),
            ("Pokémon Battle", "#FF6B6B", "white", self.start_pokemon_battle_game),
            ("Back", "#f44336", "white", self.show_difficulty_selection)
        ]
        
        for i, (text, bg, fg, command) in enumerate(test_buttons, 2):
            tk.Button(test_frame, text=text, font=self.button_font, bg=bg,
                     fg=fg, command=command).grid(row=i, column=0, pady=10)

    def quit_game(self):
        """Quit the game directly"""
        result = messagebox.askyesno("Exit Game", "Are you sure you want to exit?")
        if result:
            self.root.quit()

    def reset_game_state(self):
        """Reset game state for new game"""
        self.score = 0
        self.streak = 0
        self.lives_system.reset_all_lives()  # Reset both player and enemy lives

    def start_game(self):
        """Start algebra game with Pokémon battle GUI"""
        self.reset_game_state()
        self.game_mode = "algebra"
        self.setup_pokemon_battle_ui()
        self.generate_question()
        self.start_timer()

    def start_square_root_game(self):
        """Start square root game with Pokémon battle GUI"""
        self.reset_game_state()
        self.time_left = SQUARE_ROOT_TIME
        self.game_mode = "square_root"
        self.setup_pokemon_battle_ui()
        self.generate_square_root_question()
        self.start_timer()

    def start_integration_game(self):
        """Start integration game with Pokémon battle GUI"""
        self.reset_game_state()
        self.game_mode = "integration"
        self.setup_pokemon_battle_ui()
        self.generate_integration_question()
        self.start_timer()

    def start_differentiation_game(self):
        """Start differentiation game with Pokémon battle GUI"""
        self.reset_game_state()
        self.game_mode = "differentiation"
        self.setup_pokemon_battle_ui()
        self.generate_differentiation_question()
        self.start_timer()

    def start_pokemon_battle_game(self):
        """Start Pokémon battle game with actual battle background"""
        self.reset_game_state()
        self.game_mode = "pokemon_battle"
        self.setup_pokemon_battle_ui()
        self.generate_pokemon_question()
        self.start_timer()

    def generate_question(self):
        """Generate algebra question based on difficulty"""
        question_text, self.current_answer = self.game_logic.generate_algebra_question(self.difficulty)
        self.question_label.config(text=question_text)
        self.battle_message.config(text="⚡ Pikachu is ready to battle! Answer correctly to attack!")
        self.answer_entry.delete(0, tk.END)

    def generate_square_root_question(self):
        """Generate square root question"""
        question_text, self.current_answer = self.game_logic.generate_square_root_question(self.difficulty)
        self.question_label.config(text=question_text)
        self.battle_message.config(text="⚡ Pikachu is ready to battle! Answer correctly to attack!")
        self.answer_entry.delete(0, tk.END)

    def generate_integration_question(self):
        """Generate integration question based on difficulty"""
        self.current_question = self.game_logic.generate_integration_question(self.difficulty)
        self.question_label.config(text=self.current_question["question"])
        self.battle_message.config(text="⚡ Pikachu is ready to battle! Choose the correct answer to attack!")
        
        # Clear previous options
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Create option buttons
        for option, text in self.current_question["options"].items():
            btn = tk.Button(self.options_frame, text=f"{option}. {text}", 
                           font=("Comic Sans MS", 10), bg="#4CAF50", fg="white",
                           command=lambda opt=option: self.check_integration_answer(opt),
                           width=50, height=1)
            btn.pack(pady=3)

    def generate_differentiation_question(self):
        """Generate differentiation question based on difficulty"""
        self.current_question = self.game_logic.generate_differentiation_question(self.difficulty)
        self.question_label.config(text=self.current_question["question"])
        self.battle_message.config(text="⚡ Pikachu is ready to battle! Choose the correct answer to attack!")
        
        # Clear previous options
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Create option buttons
        for option, text in self.current_question["options"].items():
            btn = tk.Button(self.options_frame, text=f"{option}. {text}", 
                           font=("Comic Sans MS", 10), bg="#4CAF50", fg="white",
                           command=lambda opt=option: self.check_differentiation_answer(opt),
                           width=50, height=1)
            btn.pack(pady=3)

    def generate_pokemon_question(self):
        """Generate Pokémon-themed math question"""
        question_text, self.current_answer = self.game_logic.generate_pokemon_question(self.difficulty)
        self.question_label.config(text=question_text)
        self.battle_message.config(text="⚡ Pikachu is ready to battle! Answer correctly to attack!")
        self.answer_entry.delete(0, tk.END)

    def check_algebra_answer(self, event=None):
        """Check algebra answer with Pokémon battle effects"""
        try:
            user_answer = float(self.answer_entry.get())
            is_correct, message = self.game_logic.check_algebra_answer(user_answer, self.current_answer)
            
            if is_correct:
                # Correct answer - successful attack
                battle_message = self.game_logic.get_battle_messages(True)
                self.battle_message.config(text=battle_message, fg="#006400")  # Dark green for success
                
                # Flash the enemy Pokémon red when hit
                self.flash_enemy_red()
                
                self.handle_correct_answer(2, "Correct!")
            else:
                # Wrong answer - attack misses and player gets hit
                battle_message = self.game_logic.get_battle_messages(False)
                self.battle_message.config(text=battle_message, fg="#8B0000")  # Dark red for failure
                
                # Flash the player's Pokémon red when hit
                self.flash_pokemon_red()
                
                self.handle_wrong_answer("Wrong!", f"Correct answer: {self.current_answer}")
        except ValueError:
            self.show_message_with_timer_freeze("Error", "Please enter a valid number!", "error")
            self.answer_entry.delete(0, tk.END)

    def check_square_root_answer(self, event=None):
        """Check square root answer"""
        try:
            user_answer = float(self.answer_entry.get())
            result = self.game_logic.check_square_root_answer(user_answer, self.current_answer)
            
            if len(result) == 4:  # Correct format
                is_correct, message, points, deviation = result
                if is_correct:
                    # Correct answer - successful attack
                    battle_message = self.game_logic.get_battle_messages(True)
                    self.battle_message.config(text=battle_message, fg="#006400")  # Dark green for success
                    
                    # Flash the enemy Pokémon red when hit
                    self.flash_enemy_red()
                    
                    self.handle_correct_answer(max(1, points // 5), message, deviation, points)
                else:
                    # Wrong answer - attack misses and player gets hit
                    battle_message = self.game_logic.get_battle_messages(False)
                    self.battle_message.config(text=battle_message, fg="#8B0000")  # Dark red for failure
                    
                    # Flash the player's Pokémon red when hit
                    self.flash_pokemon_red()
                    
                    self.handle_wrong_answer(message, f"Deviation: {deviation:.3f}")
            else:
                self.handle_wrong_answer("Invalid input!", "")
                    
        except ValueError:
            self.show_message_with_timer_freeze("Error", "Please enter a valid number!", "error")
            self.answer_entry.delete(0, tk.END)

    def check_integration_answer(self, selected_option):
        """Check integration answer with difficulty-based scoring and Pokémon battle effects"""
        is_correct, message = self.game_logic.check_integration_answer(selected_option, self.current_question)
        
        if is_correct:
            # Different scoring based on difficulty
            if self.difficulty == "easy":
                coins_earned = 3
                message = "Correct! Great job with basic integration!"
            elif self.difficulty == "medium":
                coins_earned = 5
                message = "Excellent! Medium difficulty integration mastered!"
            elif self.difficulty == "hard":
                coins_earned = 8
                message = "Outstanding! Advanced integration conquered!"
            else:
                coins_earned = 3
                message = "Correct! Great job with integration!"
            
            # Correct answer - successful attack
            battle_message = self.game_logic.get_battle_messages(True)
            self.battle_message.config(text=battle_message, fg="#006400")  # Dark green for success
            
            # Flash the enemy Pokémon red when hit
            self.flash_enemy_red()
            
            self.handle_correct_answer(coins_earned, message)
        else:
            # Wrong answer - attack misses and player gets hit
            battle_message = self.game_logic.get_battle_messages(False)
            self.battle_message.config(text=battle_message, fg="#8B0000")  # Dark red for failure
            
            # Flash the player's Pokémon red when hit
            self.flash_pokemon_red()
            
            self.handle_wrong_answer("Incorrect!", f"Correct answer: {self.current_question['answer']}")

    def check_differentiation_answer(self, selected_option):
        """Check differentiation answer with difficulty-based scoring and Pokémon battle effects"""
        is_correct, message = self.game_logic.check_differentiation_answer(selected_option, self.current_question)
        
        if is_correct:
            # Different scoring based on difficulty
            if self.difficulty == "easy":
                coins_earned = 3
                message = "Correct! Great job with basic differentiation!"
            elif self.difficulty == "medium":
                coins_earned = 5
                message = "Excellent! Medium difficulty differentiation mastered!"
            elif self.difficulty == "hard":
                coins_earned = 8
                message = "Outstanding! Advanced differentiation conquered!"
            else:
                coins_earned = 3
                message = "Correct! Great job with differentiation!"
            
            # Correct answer - successful attack
            battle_message = self.game_logic.get_battle_messages(True)
            self.battle_message.config(text=battle_message, fg="#006400")  # Dark green for success
            
            # Flash the enemy Pokémon red when hit
            self.flash_enemy_red()
            
            self.handle_correct_answer(coins_earned, message)
        else:
            # Wrong answer - attack misses and player gets hit
            battle_message = self.game_logic.get_battle_messages(False)
            self.battle_message.config(text=battle_message, fg="#8B0000")  # Dark red for failure
            
            # Flash the player's Pokémon red when hit
            self.flash_pokemon_red()
            
            self.handle_wrong_answer("Incorrect!", f"Correct answer: {self.current_question['answer']}")

    def check_pokemon_answer(self, event=None):
        """Check Pokémon battle answer"""
        try:
            user_answer = float(self.answer_entry.get())
            is_correct, message = self.game_logic.check_pokemon_answer(user_answer, self.current_answer)
            
            if is_correct:
                # Correct answer - successful attack on enemy
                battle_message = self.game_logic.get_battle_messages(True)
                self.battle_message.config(text=battle_message, fg="#006400")  # Dark green for success
                
                # Flash the enemy Pokémon red when hit
                self.flash_enemy_red()
                
                # Use centralized handle_correct_answer function
                self.handle_correct_answer(3, "Correct!")
            else:
                # Wrong answer - attack misses and player gets hit
                battle_message = self.game_logic.get_battle_messages(False)
                self.battle_message.config(text=battle_message, fg="#8B0000")  # Dark red for failure
                
                # Flash the player's Pokémon red when hit
                self.flash_pokemon_red()
                
                self.handle_wrong_answer("Attack missed!", f"Correct answer: {self.current_answer}")
        except ValueError:
            self.show_message_with_timer_freeze("Error", "Please enter a valid number!", "error")
            self.answer_entry.delete(0, tk.END)

    def handle_correct_answer(self, coins_earned, message, deviation=None, points=None):
        """Handle correct answer logic"""
        self.score += points if points else 10
        self.streak += 1
        utils.animate_score_label(self.score_label, self.root)
        self.data_manager.add_gold_coins(self.player_name, coins_earned)
        
        # Handle enemy lives reduction for ALL game modes
        # Reduce enemy lives and update display
        self.lives_system.reduce_enemy_lives(1)
        
        # Force update the enemy lives display
        self.enemy_lives_label.config(text=self.lives_system.get_enemy_life_display())
        
        # Check if enemy is defeated
        if self.lives_system.is_enemy_defeated():
            self.handle_enemy_defeated()
            return  # Exit early to avoid further processing
        
        if self.streak % 3 == 0:
            bonus_coins = 3 if self.game_mode == "square_root" else 5
            self.score += 10 if self.game_mode == "square_root" else 20
            self.data_manager.add_gold_coins(self.player_name, bonus_coins)
            self.show_message_with_timer_freeze("Combo!", 
                f"🔥 Combo x{self.streak}! +{self.score} Bonus Points! +{bonus_coins} Gold Coins!")
        
        utils.play_sound("correct")
        
        if deviation is not None:
            self.show_message_with_timer_freeze("Result", 
                f"{message}\nDeviation: {deviation:.3f}\nPoints earned: {points}\nGold Coins earned: {coins_earned}")
        else:
            self.show_message_with_timer_freeze("Result", f"{message} +{coins_earned} Gold Coins earned!")
        
        self.update_game_display()

    def handle_wrong_answer(self, message, details=""):
        """Handle wrong answer logic"""
        self.score = max(0, self.score - (2 if self.game_mode == "square_root" else 5))
        self.streak = 0
        self.lives_system.reduce_player_lives(1)
        self.lives_label.config(text=self.lives_system.get_player_life_display())
        utils.play_sound("incorrect")
        
        # Update enemy lives display for ALL game modes
        self.enemy_lives_label.config(text=self.lives_system.get_enemy_life_display())
        
        full_message = f"{message}\n{details}" if details else message
        self.show_message_with_timer_freeze("Result", full_message, "error")
        
        if self.lives_system.is_player_defeated():
            self.end_game()
        else:
            self.update_game_display()

    def update_game_display(self):
        """Update game display after answer"""
        self.score_label.config(text=f"Score: {self.score}")
        
        # Update enemy lives display for ALL game modes
        self.enemy_lives_label.config(text=self.lives_system.get_enemy_life_display())
        
        if self.game_mode == "square_root":
            self.time_left = SQUARE_ROOT_TIME
            self.generate_square_root_question()
        elif self.game_mode == "integration":
            self.time_left = INTEGRATION_TIME
            self.generate_integration_question()
        elif self.game_mode == "differentiation":
            self.time_left = DIFFERENTIATION_TIME
            self.generate_differentiation_question()
        elif self.game_mode == "pokemon_battle":
            self.time_left = POKEMON_BATTLE_TIME
            self.generate_pokemon_question()
        else:
            self.time_left = ALGEBRA_TIME
            self.generate_question()
        
        self.time_label.config(text=f"Time: {self.time_left}s")

    def start_timer(self):
        """Start the game timer"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
        # Set appropriate time limit based on game mode
        if hasattr(self, 'game_mode'):
            if self.game_mode == "square_root":
                self.time_left = SQUARE_ROOT_TIME
            elif self.game_mode == "integration":
                self.time_left = INTEGRATION_TIME
            elif self.game_mode == "differentiation":
                self.time_left = DIFFERENTIATION_TIME
            elif self.game_mode == "pokemon_battle":
                self.time_left = POKEMON_BATTLE_TIME
            else:
                self.time_left = ALGEBRA_TIME
        
        self.update_timer()

    def update_timer(self):
        """Update game timer"""
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"Time: {self.time_left}s")
            if self.time_left <= 3:
                utils.animate_time_warning(self.time_label, self.root)
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.lives_system.reduce_player_lives(1)
            self.lives_label.config(text=self.lives_system.get_player_life_display())
            
            # Update enemy lives display for ALL game modes
            self.enemy_lives_label.config(text=self.lives_system.get_enemy_life_display())
            
            utils.play_sound("incorrect")
            if self.lives_system.is_player_defeated():
                self.end_game()
            else:
                if self.game_mode == "square_root":
                    self.time_left = SQUARE_ROOT_TIME
                    self.generate_square_root_question()
                elif self.game_mode == "integration":
                    self.time_left = INTEGRATION_TIME
                    self.generate_integration_question()
                elif self.game_mode == "differentiation":
                    self.time_left = DIFFERENTIATION_TIME
                    self.generate_differentiation_question()
                elif self.game_mode == "pokemon_battle":
                    self.time_left = POKEMON_BATTLE_TIME
                    self.generate_pokemon_question()
                else:
                    self.time_left = ALGEBRA_TIME
                    self.generate_question()
                self.update_timer()

    def freeze_timer(self):
        """Freeze the game timer"""
        if self.timer_id and not self.timer_frozen:
            self.timer_frozen = True
            self.frozen_time_left = self.time_left
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def resume_timer(self):
        """Resume the game timer"""
        if self.timer_frozen:
            self.timer_frozen = False
            self.time_left = self.frozen_time_left
            self.start_timer()

    def show_message_with_timer_freeze(self, title, message, message_type="info"):
        """Show message box with timer freeze/resume"""
        self.freeze_timer()
        
        message_functions = {
            "info": messagebox.showinfo,
            "error": messagebox.showerror,
            "warning": messagebox.showwarning,
            "yesno": messagebox.askyesno
        }
        
        result = message_functions.get(message_type, messagebox.showinfo)(title, message)
        self.resume_timer()
        return result

    def end_game(self):
        """End the game and show results"""
        coins_earned = self.data_manager.calculate_coins_earned_in_game(self.player_name, self.score, self.game_mode)
        result = self.show_message_with_timer_freeze("Game Over", 
            f"You're out of lives!\n\nFinal Score: {self.score}\nGold Coins Earned: {coins_earned}\n\nWould you like to play again?", "yesno")
        self.data_manager.update_leaderboard(self.player_name, self.score, self.difficulty)
        if result:
            self.show_difficulty_selection()
        else:
            self.root.quit()

    def setup_pokemon_battle_ui(self):
        """Setup Pokémon battle game UI with battle background and sprites"""
        self.clear_window()
        
        # Set up the battle background with a pure color
        # Using a Pokémon-themed blue color for the battle arena
        battle_bg_color = "#87CEEB"  # Sky blue color
        
        # Create background label with pure color
        self.battle_bg_label = tk.Label(self.root, bg=battle_bg_color)
        self.battle_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        print("✅ Battle background set to sky blue color!")
        
        # Load Pokémon sprites
        try:
            # Load Pikachu sprite (player)
            pikachu_img = Image.open("assets/pikachu.png")
            pikachu_img = pikachu_img.resize((120, 120), Image.Resampling.LANCZOS)
            self.pikachu_photo = ImageTk.PhotoImage(pikachu_img)
            print("✅ Pikachu sprite loaded successfully!")
            
            # Load enemy Pokémon sprites
            # Squirtle
            squirtle_img = Image.open("assets/turtle.png")
            squirtle_img = squirtle_img.resize((120, 120), Image.Resampling.LANCZOS)
            self.squirtle_photo = ImageTk.PhotoImage(squirtle_img)
            print("✅ Squirtle sprite loaded successfully!")
            
            # Charmander (pokemon_1.png)
            charmander_img = Image.open("assets/pokemon_1.png")
            charmander_img = charmander_img.resize((120, 120), Image.Resampling.LANCZOS)
            self.charmander_photo = ImageTk.PhotoImage(charmander_img)
            print("✅ Charmander sprite loaded successfully!")
            
            # Gengar (pokemon_2.png)
            gengar_img = Image.open("assets/pokemon_2.png")
            gengar_img = gengar_img.resize((120, 120), Image.Resampling.LANCZOS)
            self.gengar_photo = ImageTk.PhotoImage(gengar_img)
            print("✅ Gengar sprite loaded successfully!")
            
            # Eevee (pokemon_3.png)
            eevee_img = Image.open("assets/pokemon_3.png")
            eevee_img = eevee_img.resize((120, 120), Image.Resampling.LANCZOS)
            self.eevee_photo = ImageTk.PhotoImage(eevee_img)
            print("✅ Eevee sprite loaded successfully!")
            
            # Bulbasaur (pokemon_4.png)
            bulbasaur_img = Image.open("assets/pokemon_4.png")
            bulbasaur_img = bulbasaur_img.resize((120, 120), Image.Resampling.LANCZOS)
            self.bulbasaur_photo = ImageTk.PhotoImage(bulbasaur_img)
            print("✅ Bulbasaur sprite loaded successfully!")
            
        except Exception as e:
            print(f"❌ Pokémon sprite error: {e}")
            # Try alternative paths for sprites
            try:
                # Try loading from root directory
                pikachu_img = Image.open("pikachu.png")
                pikachu_img = pikachu_img.resize((120, 120), Image.Resampling.LANCZOS)
                self.pikachu_photo = ImageTk.PhotoImage(pikachu_img)
                print("✅ Pikachu sprite loaded from root directory!")
                
                squirtle_img = Image.open("turtle.png")
                squirtle_img = squirtle_img.resize((120, 120), Image.Resampling.LANCZOS)
                self.squirtle_photo = ImageTk.PhotoImage(squirtle_img)
                print("✅ Squirtle sprite loaded from root directory!")
                
                charmander_img = Image.open("pokemon_1.png")
                charmander_img = charmander_img.resize((120, 120), Image.Resampling.LANCZOS)
                self.charmander_photo = ImageTk.PhotoImage(charmander_img)
                print("✅ Charmander sprite loaded from root directory!")
                
                gengar_img = Image.open("pokemon_2.png")
                gengar_img = gengar_img.resize((120, 120), Image.Resampling.LANCZOS)
                self.gengar_photo = ImageTk.PhotoImage(gengar_img)
                print("✅ Gengar sprite loaded from root directory!")
                
                eevee_img = Image.open("pokemon_3.png")
                eevee_img = eevee_img.resize((120, 120), Image.Resampling.LANCZOS)
                self.eevee_photo = ImageTk.PhotoImage(eevee_img)
                print("✅ Eevee sprite loaded from root directory!")
                
                bulbasaur_img = Image.open("pokemon_4.png")
                bulbasaur_img = bulbasaur_img.resize((120, 120), Image.Resampling.LANCZOS)
                self.bulbasaur_photo = ImageTk.PhotoImage(bulbasaur_img)
                print("✅ Bulbasaur sprite loaded from root directory!")
                
            except Exception as e2:
                print(f"❌ Pokémon sprites not found in root either: {e2}")
                # Fallback sprites if images not found
                self.pikachu_photo = None
                self.squirtle_photo = None
                self.charmander_photo = None
                self.gengar_photo = None
                self.eevee_photo = None
                self.bulbasaur_photo = None
        
        # Select random enemy Pokémon
        self.select_random_enemy()
        
        # Create battle interface overlay
        battle_overlay = tk.Frame(self.root)
        battle_overlay.place(relx=0.5, rely=0.5, anchor="center")
        
        # Top section - Battle info and stats
        top_frame = tk.Frame(battle_overlay, bg="#FED000", relief="raised", bd=3)
        top_frame.pack(fill="x", pady=10)
        
        # Player side (left) - Pikachu
        player_frame = tk.Frame(top_frame, bg="#FED000")
        player_frame.pack(side="left", padx=20, pady=10)
        
        if self.pikachu_photo:
            self.pikachu_label = tk.Label(player_frame, image=self.pikachu_photo, bg="#FED000")
            self.pikachu_label.pack()
        else:
            self.pikachu_label = tk.Label(player_frame, text="⚡ Pikachu", font=("Arial", 16, "bold"), 
                    bg="#FED000", fg="#FFD700")
            self.pikachu_label.pack()
        
        tk.Label(player_frame, text=f"Player: {self.player_name}", 
                font=self.label_font, bg="#FED000").pack()
        
        # Battle stats (center)
        stats_frame = tk.Frame(top_frame, bg="#FED000")
        stats_frame.pack(side="left", padx=40, pady=10)
        
        self.score_label = tk.Label(stats_frame, text=f"Score: {self.score}", 
                                   font=self.label_font, bg="#FED000")
        self.score_label.pack()
        
        self.time_label = tk.Label(stats_frame, text=f"Time: {self.time_left}s", 
                                  font=self.label_font, bg="#FED000")
        self.time_label.pack()
        
        self.lives_label = tk.Label(stats_frame, text=self.lives_system.get_player_life_display(), 
                                   font=self.label_font, fg="red", bg="#FED000")
        self.lives_label.pack()
        
        # Enemy side (right) - Random enemy
        enemy_frame = tk.Frame(top_frame, bg="#FED000")
        enemy_frame.pack(side="right", padx=20, pady=10)
        
        # Display the selected enemy Pokémon
        if hasattr(self, 'current_enemy_photo') and self.current_enemy_photo:
            self.enemy_label = tk.Label(enemy_frame, image=self.current_enemy_photo, bg="#FED000")
            self.enemy_label.pack()
        else:
            # Fallback text based on enemy type
            enemy_text = self.get_enemy_text()
            self.enemy_label = tk.Label(enemy_frame, text=enemy_text, font=("Arial", 16, "bold"), 
                    bg="#FED000", fg=self.get_enemy_color())
            self.enemy_label.pack()
        
        tk.Label(enemy_frame, text="Enemy Trainer", 
                font=self.label_font, bg="#FED000").pack()
        
        # Enemy lives display
        self.enemy_lives_label = tk.Label(enemy_frame, text=self.lives_system.get_enemy_life_display(), 
                                         font=self.label_font, fg="red", bg="#FED000")
        self.enemy_lives_label.pack()
        
        # Battle arena - middle section
        arena_frame = tk.Frame(battle_overlay, bg="#FED000", relief="raised", bd=3)
        arena_frame.pack(fill="x", pady=20)
        
        # Battle message display
        self.battle_message = tk.Label(arena_frame, text="", font=self.label_font, 
                                     bg="#FED000", wraplength=400, fg="#8B0000")
        self.battle_message.pack(pady=10)
        
        # Question area
        self.question_label = tk.Label(arena_frame, text="", font=self.label_font, 
                                     bg="#FED000", wraplength=400)
        self.question_label.pack(pady=10)
        
        # Answer area - will be configured based on game mode
        self.answer_frame = tk.Frame(arena_frame, bg="#FED000")
        self.answer_frame.pack(pady=10)
        
        # Action buttons
        button_frame = tk.Frame(arena_frame, bg="#FED000")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Back", font=self.button_font, bg="#f44336",
                  fg="white", command=self.confirm_back_to_menu).pack(side="left", padx=5)
        
        # Configure answer area based on game mode
        self.configure_answer_area()

    def configure_answer_area(self):
        """Configure the answer area based on game mode"""
        # Clear previous answer widgets
        for widget in self.answer_frame.winfo_children():
            widget.destroy()
        
        if self.game_mode in ["algebra", "square_root", "pokemon_battle"]:
            # Text input for algebra, square root, and Pokémon battle
            tk.Label(self.answer_frame, text="Your Answer:", font=self.label_font, 
                    bg="#FED000").pack()
            
            self.answer_entry = tk.Entry(self.answer_frame, font=self.label_font, width=20)
            self.answer_entry.pack(pady=5)
            
            # Bind to appropriate check method
            if self.game_mode == "algebra":
                self.answer_entry.bind("<Return>", self.check_algebra_answer)
                attack_btn = tk.Button(self.answer_frame, text="⚡ Attack!", font=self.button_font, bg="#FF6B6B",
                                      fg="white", command=self.check_algebra_answer)
            elif self.game_mode == "square_root":
                self.answer_entry.bind("<Return>", self.check_square_root_answer)
                attack_btn = tk.Button(self.answer_frame, text="⚡ Attack!", font=self.button_font, bg="#FF6B6B",
                                      fg="white", command=self.check_square_root_answer)
            else:  # pokemon_battle
                self.answer_entry.bind("<Return>", self.check_pokemon_answer)
                attack_btn = tk.Button(self.answer_frame, text="⚡ Attack!", font=self.button_font, bg="#FF6B6B",
                                      fg="white", command=self.check_pokemon_answer)
            
            attack_btn.pack(pady=5)
            
        elif self.game_mode in ["integration", "differentiation"]:
            # Multiple choice for integration and differentiation
            self.options_frame = tk.Frame(self.answer_frame, bg="#FED000")
            self.options_frame.pack(pady=5)
            
            # Options will be populated by the question generation methods

    def select_random_enemy(self):
        """Select a random enemy Pokémon"""
        enemies = [
            {"name": "Squirtle", "photo": self.squirtle_photo, "text": "💧 Squirtle", "color": "#87CEEB"},
            {"name": "Charmander", "photo": self.charmander_photo, "text": "🔥 Charmander", "color": "#FF6B35"},
            {"name": "Gengar", "photo": self.gengar_photo, "text": "👻 Gengar", "color": "#8B5A96"},
            {"name": "Eevee", "photo": self.eevee_photo, "text": "🦊 Eevee", "color": "#D2B48C"},
            {"name": "Bulbasaur", "photo": self.bulbasaur_photo, "text": "🌱 Bulbasaur", "color": "#90EE90"}
        ]
        
        self.current_enemy = random.choice(enemies)
        self.current_enemy_photo = self.current_enemy["photo"]
        self.current_enemy_name = self.current_enemy["name"]
        print(f"🎯 Selected enemy: {self.current_enemy_name}")

    def get_enemy_name(self):
        """Get the name of the current enemy"""
        if hasattr(self, 'current_enemy'):
            return self.current_enemy["name"]
        return "Squirtle"  # Default fallback

    def get_enemy_text(self):
        """Get the text representation of the current enemy"""
        if hasattr(self, 'current_enemy'):
            return self.current_enemy["text"]
        return "💧 Squirtle"  # Default fallback

    def get_enemy_color(self):
        """Get the color for the current enemy"""
        if hasattr(self, 'current_enemy'):
            return self.current_enemy["color"]
        return "#87CEEB"  # Default fallback

    def flash_pokemon_red(self):
        """Make the player's Pokémon flash red when hit"""
        if hasattr(self, 'pikachu_label'):
            # Flash the Pikachu label red
            original_bg = self.pikachu_label.cget('bg')
            self.pikachu_label.config(bg='red')
            
            # Return to original color after 300ms
            self.root.after(300, lambda: self.pikachu_label.config(bg=original_bg))
        else:
            # Fallback: flash the entire player frame
            self.flash_player_frame_red()

    def flash_enemy_red(self):
        """Make the enemy's Pokémon flash red when hit"""
        if hasattr(self, 'enemy_label'):
            # Flash the enemy label red
            original_bg = self.enemy_label.cget('bg')
            self.enemy_label.config(bg='red')
            
            # Return to original color after 300ms
            self.root.after(300, lambda: self.enemy_label.config(bg=original_bg))
        else:
            # Fallback: flash the entire enemy frame
            self.flash_enemy_frame_red()

    def flash_player_frame_red(self):
        """Flash the entire player frame red as fallback"""
        # Find the player frame (first frame in the top section)
        for widget in self.root.winfo_children():
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if hasattr(child, 'winfo_children'):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Frame) and grandchild.cget('bg') == '#FED000':
                                # This is likely the player frame
                                original_bg = grandchild.cget('bg')
                                grandchild.config(bg='red')
                                self.root.after(300, lambda: grandchild.config(bg=original_bg))
                                return

    def flash_enemy_frame_red(self):
        """Flash the entire enemy frame red as fallback"""
        # Find the enemy frame (right side frame in the top section)
        for widget in self.root.winfo_children():
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if hasattr(child, 'winfo_children'):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Frame) and grandchild.cget('bg') == '#FED000':
                                # This is likely the enemy frame (right side)
                                original_bg = grandchild.cget('bg')
                                grandchild.config(bg='red')
                                self.root.after(300, lambda: grandchild.config(bg=original_bg))
                                return

    def handle_enemy_defeated(self):
        """Handle when enemy is defeated"""
        enemy_name = self.get_enemy_name()
        victory_message = self.game_logic.get_victory_messages(enemy_name)
        self.battle_message.config(text=victory_message, fg="#FFD700")  # Gold color for victory
        
        # Add bonus points for defeating enemy
        bonus_points = 50
        self.score += bonus_points
        
        # Show victory message
        result = self.show_message_with_timer_freeze("Victory!", 
            f"{victory_message}\n\nBonus Points: +{bonus_points}\nFinal Score: {self.score}\n\nWould you like to battle another trainer?", "yesno")
        
        if result:
            # Reset enemy lives for next battle
            self.lives_system.reset_enemy_lives()
            self.enemy_lives_label.config(text=self.lives_system.get_enemy_life_display())
            
            # Select a new random enemy for the next battle
            self.select_random_enemy()
            
            # Update the enemy display
            if hasattr(self, 'enemy_label'):
                if self.current_enemy_photo:
                    self.enemy_label.config(image=self.current_enemy_photo)
                else:
                    self.enemy_label.config(text=self.get_enemy_text(), fg=self.get_enemy_color())
            

        else:
            # End game and go back to menu
            self.end_game()

    def show_leaderboard(self):
        """Show leaderboard page"""
        self.clear_window()
        self.root.configure(bg="#FCE4EC")  # Light pink background
        
        self.data_manager.leaderboard = self.data_manager.load_leaderboard()
        leaderboard_frame = self.create_centered_frame()

        tk.Label(leaderboard_frame, text="Leaderboard", font=self.title_font).grid(row=0, column=0, pady=20)
        
        for idx, entry in enumerate(self.data_manager.leaderboard, 1):
            player_name = entry.get('player_name', 'Unknown Player')
            tk.Label(leaderboard_frame,
                     text=f"{idx}. {player_name} - Score: {entry['score']} ({entry['difficulty']}) - {entry['timestamp']}",
                     font=self.label_font).grid(row=idx, column=0, pady=2)

        buttons = [
            ("Delete All Records", "#ff4444", "white", self.confirm_delete_all),
            ("Back to Menu", self.button_color, "white", self.create_start_menu)
        ]
        
        for i, (text, bg, fg, command) in enumerate(buttons, len(self.data_manager.leaderboard) + 1):
            tk.Button(leaderboard_frame, text=text, font=self.button_font, bg=bg,
                     fg=fg, command=command).grid(row=i, column=0, pady=10 if i == len(self.data_manager.leaderboard) + 1 else 20)

    def show_store(self):
        """Show store page"""
        self.clear_window()
        self.root.configure(bg="#4CC7D8")   # Light blue background
        
        store_frame = self.create_centered_frame()
        
        tk.Label(store_frame, text="🏪 Math Master Store", font=self.title_font).grid(row=0, column=0, pady=10)
        player_coins = self.data_manager.get_player_gold_coins(self.player_name)
        tk.Label(store_frame, text=f"💰 Gold Coins: {player_coins}", 
                font=self.label_font, fg="#FFD700").grid(row=1, column=0, pady=5)
        
        for row, (item_name, item_data) in enumerate(self.data_manager.store_items.items(), 2):
            item_frame = tk.Frame(store_frame)
            item_frame.grid(row=row, column=0, pady=5, sticky="ew")
            
            tk.Label(item_frame, text=f"🛒 {item_name}", font=self.button_font).grid(row=0, column=0, sticky="w")
            tk.Label(item_frame, text=f"💡 {item_data['description']}", font=self.label_font).grid(row=1, column=0, sticky="w")
            tk.Label(item_frame, text=f"💰 {item_data['price']} coins", font=self.label_font, fg="#FFD700").grid(row=2, column=0, sticky="w")
            
            tk.Button(item_frame, text="Buy", font=self.button_font, bg="#4CAF50", fg="white",
                     command=lambda name=item_name: self.buy_item(name)).grid(row=0, column=1, rowspan=3, padx=10)
        
        tk.Button(store_frame, text="Back", font=self.button_font, bg=self.button_color,
                  fg="white", command=self.show_difficulty_selection).grid(row=len(self.data_manager.store_items)+2, column=0, pady=20)

    def buy_item(self, item_name):
        """Buy item from store"""
        success, message = self.data_manager.buy_item(self.player_name, item_name)
        if success:
            messagebox.showinfo("Purchase Successful", message)
        else:
            messagebox.showerror("Purchase Failed", message)
        self.show_store()

    def confirm_delete_all(self):
        """Handle delete all records confirmation"""
        if not self.data_manager.leaderboard:
            messagebox.showinfo("No Records", "There are no records to delete.")
            return
        
        result = messagebox.askyesno("Delete All Records", 
                                   f"Are you sure you want to delete ALL {len(self.data_manager.leaderboard)} records?\n\nThis action cannot be undone!")
        if result:
            success, message = self.data_manager.delete_all_records()
            if success:
                messagebox.showinfo("Records Deleted", message)
            else:
                messagebox.showerror("Error", message)
            self.show_leaderboard()

    def confirm_back_to_menu(self):
        """Handle back to menu confirmation"""
        if hasattr(self, 'score') and self.score > 0:
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
            
            coins_earned = self.data_manager.calculate_coins_earned_in_game(self.player_name, self.score, self.game_mode)
            result = messagebox.askyesno("Return to Menu", 
                                       f"Are you sure you want to return to the difficulty selection?\n\nCurrent Score: {self.score}\nDifficulty: {self.difficulty.capitalize()}\nGold Coins Earned: {coins_earned}\n\nYour score will be saved before returning.")
            if result:
                self.data_manager.update_leaderboard(self.player_name, self.score, self.difficulty)
                messagebox.showinfo("Score Saved", f"Your score of {self.score} has been saved to the leaderboard!\nGold Coins Earned: {coins_earned}")
                self.show_difficulty_selection()
            else:
                self.start_timer()
        else:
            self.show_difficulty_selection()

    def confirm_exit(self):
        """Handle exit confirmation"""
        if hasattr(self, 'score') and self.score > 0:
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
            
            coins_earned = self.data_manager.calculate_coins_earned_in_game(self.player_name, self.score, self.game_mode)
            result = messagebox.askyesno("Exit Game", 
                                       f"Are you sure you want to exit?\n\nCurrent Score: {self.score}\nDifficulty: {self.difficulty.capitalize()}\nGold Coins Earned: {coins_earned}\n\nYour score will be saved before exiting.")
            if result:
                self.data_manager.update_leaderboard(self.player_name, self.score, self.difficulty)
                messagebox.showinfo("Score Saved", f"Your score of {self.score} has been saved to the leaderboard!\nGold Coins Earned: {coins_earned}")
                self.root.quit()
            else:
                self.start_timer()
        else:
            result = messagebox.askyesno("Exit Game", "Are you sure you want to exit?")
            if result:
                self.root.quit() 