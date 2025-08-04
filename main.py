import tkinter as tk
from tkinter import messagebox
import random
import time
import json
import os
import math
from PIL import Image, ImageTk

# Try importing winsound for Windows beep sound effects
try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

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

integration_questions_simple = [
    # Original 10
    {
        "question": "What is the integral of ∫ x dx?",
        "options": {
            "A": "(1/2)x^2 + C",
            "B": "2x + C",
            "C": "x^2 + C",
            "D": "ln|x| + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ 3x² dx?",
        "options": {
            "A": "x^3 + C",
            "B": "x^2 + C",
            "C": "x^3",
            "D": "3x + C"
        },
        "answer": "A"
    },
    {
        "question": "What is the result of ∫ cos(x) dx?",
        "options": {
            "A": "cos(x) + C",
            "B": "sin(x) + C",
            "C": "-cos(x) + C",
            "D": "-sin(x) + C"
        },
        "answer": "B"
    },
    {
        "question": "Which of the following is ∫ (1/x) dx?",
        "options": {
            "A": "ln(x) + C",
            "B": "1/x^2 + C",
            "C": "ln|x| + C",
            "D": "x^(-1) + C"
        },
        "answer": "C"
    },
    {
        "question": "Find ∫₀² x dx",
        "options": {
            "A": "2",
            "B": "4",
            "C": "1",
            "D": "2"
        },
        "answer": "A"
    },
    {
        "question": "Which function is an antiderivative of 6x²?",
        "options": {
            "A": "3x^2",
            "B": "2x^3 + C",
            "C": "x^3 + C",
            "D": "6x + C"
        },
        "answer": "B"
    },
    {
        "question": "If F(x) = ∫ x^3 dx, then F(x) =",
        "options": {
            "A": "3x^2 + C",
            "B": "x^4 + C",
            "C": "(1/4)x^4 + C",
            "D": "4x + C"
        },
        "answer": "C"
    },
    {
        "question": "What is ∫ (4x³ + 2x) dx?",
        "options": {
            "A": "x^4 + x^2 + C",
            "B": "2x^4 + x^2 + C",
            "C": "x^3 + x + C",
            "D": "x^4 + 2x^2 + C"
        },
        "answer": "A"
    },
    {
        "question": "What is the integral of a constant: ∫ 5 dx?",
        "options": {
            "A": "5x + C",
            "B": "x^5 + C",
            "C": "(5/2)x^2 + C",
            "D": "ln(x) + C"
        },
        "answer": "A"
    },
    {
        "question": "Which of the following is correct: ∫ x^(-2) dx =",
        "options": {
            "A": "-x^(-1) + C",
            "B": "ln|x| + C",
            "C": "-(1/2)x^(-2) + C",
            "D": "(1/2)x^2 + C"
        },
        "answer": "A"
    },

    # Extra 20
    {
        "question": "What is ∫ sin(x) dx?",
        "options": {
            "A": "cos(x) + C",
            "B": "-cos(x) + C",
            "C": "tan(x) + C",
            "D": "-sin(x) + C"
        },
        "answer": "B"
    },
    {
        "question": "What is ∫ e^x dx?",
        "options": {
            "A": "e^x + C",
            "B": "x·e^x + C",
            "C": "ln|x| + C",
            "D": "1/x + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ x^0 dx?",
        "options": {
            "A": "x + C",
            "B": "0 + C",
            "C": "1 + C",
            "D": "ln(x) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ (2x + 1) dx?",
        "options": {
            "A": "x^2 + x + C",
            "B": "x^2 + C",
            "C": "2x^2 + C",
            "D": "(1/2)x^2 + x + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ sec²(x) dx?",
        "options": {
            "A": "tan(x) + C",
            "B": "-tan(x) + C",
            "C": "sec(x) + C",
            "D": "ln|sec(x)| + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ tan(x) dx?",
        "options": {
            "A": "sec(x) + C",
            "B": "-ln|cos(x)| + C",
            "C": "ln|cos(x)| + C",
            "D": "ln|sin(x)| + C"
        },
        "answer": "B"
    },
    {
        "question": "What is ∫ 1/(x+1) dx?",
        "options": {
            "A": "ln|x| + C",
            "B": "ln|x+1| + C",
            "C": "1/(x+1)^2 + C",
            "D": "(x+1) + C"
        },
        "answer": "B"
    },
    {
        "question": "What is ∫ x⁵ dx?",
        "options": {
            "A": "(1/6)x^6 + C",
            "B": "(1/5)x^5 + C",
            "C": "5x^4 + C",
            "D": "(1/4)x^4 + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ x⁻³ dx?",
        "options": {
            "A": "ln|x| + C",
            "B": "-x^(-2)/2 + C",
            "C": "-x^(-1) + C",
            "D": "x^-2 + C"
        },
        "answer": "B"
    },
    {
        "question": "∫ dx equals?",
        "options": {
            "A": "1 + C",
            "B": "x + C",
            "C": "ln(x) + C",
            "D": "C"
        },
        "answer": "B"
    },
    {
        "question": "What is the integral of ∫ 7x^6 dx?",
        "options": {
            "A": "x^7 + C",
            "B": "(7/7)x^7 + C",
            "C": "x^6 + C",
            "D": "(7/6)x^7 + C"
        },
        "answer": "B"
    },
    {
        "question": "∫ 0 dx =",
        "options": {
            "A": "0",
            "B": "C",
            "C": "x + C",
            "D": "1"
        },
        "answer": "B"
    },
    {
        "question": "What is ∫ √x dx?",
        "options": {
            "A": "(1/3)x^(3/2) + C",
            "B": "(2/3)x^(3/2) + C",
            "C": "x^(1/2) + C",
            "D": "(3/2)x^(2/3) + C"
        },
        "answer": "B"
    },
    {
        "question": "What is the integral of ∫ e^(2x) dx?",
        "options": {
            "A": "2e^(2x) + C",
            "B": "e^(2x)/2 + C",
            "C": "ln(e^(2x)) + C",
            "D": "e^x + C"
        },
        "answer": "B"
    },
    {
        "question": "What is ∫ ln(x) dx?",
        "options": {
            "A": "x ln(x) - x + C",
            "B": "1/x + C",
            "C": "ln(x)^2/2 + C",
            "D": "ln(x) + C"
        },
        "answer": "A"
    },
    {
        "question": "∫ (x+1)^2 dx equals:",
        "options": {
            "A": "(1/3)(x+1)^3 + C",
            "B": "(x+1)^3 + C",
            "C": "x^2 + 2x + C",
            "D": "(x^3)/3 + C"
        },
        "answer": "A"
    },
    {
        "question": "∫ |x| dx equals:",
        "options": {
            "A": "x|x| + C",
            "B": "1/2 x^2 + C",
            "C": "undefined",
            "D": "|x| + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ sec(x)tan(x) dx?",
        "options": {
            "A": "sec(x) + C",
            "B": "tan(x) + C",
            "C": "ln|sec(x)| + C",
            "D": "sec^2(x) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ 1/(1 + x^2) dx?",
        "options": {
            "A": "arctan(x) + C",
            "B": "ln|x| + C",
            "C": "arcsin(x) + C",
            "D": "tan(x) + C"
        },
        "answer": "A"
    },
    {
        "question": "∫ cos²(x) dx equals:",
        "options": {
            "A": "(1/2)x + (1/4)sin(2x) + C",
            "B": "sin(x)^2 + C",
            "C": "1 + cos(2x) + C",
            "D": "tan(x) + C"
        },
        "answer": "A"
    }
]

integration_questions_medium = [
    {
        "question": "What is ∫ x·e^x dx?",
        "options": {
            "A": "x·e^x + C",
            "B": "e^x + C",
            "C": "x·e^x - ∫ e^x dx + C",
            "D": "x·e^x - e^x + C"
        },
        "answer": "D"
    },
    {
        "question": "What is ∫ x·ln(x) dx?",
        "options": {
            "A": "(1/2)x^2·ln(x) - (1/4)x^2 + C",
            "B": "(1/2)x^2·ln(x) - (1/2)x^2 + C",
            "C": "x^2·ln(x) - x^2 + C",
            "D": "(1/2)x^2·ln(x) + C"
        },
        "answer": "B"
    },
    {
        "question": "What is ∫ e^(2x)·sin(3x) dx?",
        "options": {
            "A": "e^(2x)·(sin(3x) - cos(3x))/13 + C",
            "B": "e^(2x)·(2sin(3x) - 3cos(3x))/13 + C",
            "C": "e^(2x)·(2cos(3x) + 3sin(3x))/13 + C",
            "D": "e^(2x)·(3sin(3x) - 2cos(3x))/13 + C"
        },
        "answer": "B"
    },
    {
        "question": "What is ∫ x²·ln(x) dx?",
        "options": {
            "A": "(1/3)x^3·ln(x) - (1/9)x^3 + C",
            "B": "(1/3)x^3·ln(x) - x + C",
            "C": "(1/3)x^3·ln(x) - x^2 + C",
            "D": "x^2·ln(x) - (2/3)x^3 + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ ln(x)^2 dx?",
        "options": {
            "A": "x·ln(x)^2 - 2x·ln(x) + 2x + C",
            "B": "x·ln(x)^2 + C",
            "C": "ln(x)^3/3 + C",
            "D": "x·ln(x)^2 - x + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ arctan(x) dx?",
        "options": {
            "A": "x·arctan(x) - (1/2)·ln(1 + x^2) + C",
            "B": "x·arctan(x) - ln(1 + x^2) + C",
            "C": "(1/2)x^2·arctan(x) + C",
            "D": "x·arctan(x) + ln|x| + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ x²·e^x dx?",
        "options": {
            "A": "e^x·(x² - 2x + 2) + C",
            "B": "x²·e^x - 2x·e^x + 2e^x + C",
            "C": "x²·e^x + C",
            "D": "e^x·(x² + 2x + 2) + C"
        },
        "answer": "B"
    },
    {
        "question": "What is ∫ x/(x^2 + 1) dx?",
        "options": {
            "A": "arctan(x) + C",
            "B": "ln|x^2 + 1| / 2 + C",
            "C": "(1/2)ln(x^2 + 1) + C",
            "D": "ln|x| + C"
        },
        "answer": "C"
    },
    {
        "question": "What is ∫ 1/(x² - 1) dx?",
        "options": {
            "A": "(1/2)ln|(x - 1)/(x + 1)| + C",
            "B": "ln|x^2 - 1| + C",
            "C": "arctan(x) + C",
            "D": "(1/2)ln|x^2 - 1| + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ x·cos(x) dx?",
        "options": {
            "A": "x·sin(x) + cos(x) + C",
            "B": "x·cos(x) - sin(x) + C",
            "C": "x·sin(x) + cos(x) + C",
            "D": "x·sin(x) + sin(x) + C"
        },
        "answer": "A"
    },

    # Remaining 20 questions...
    {
        "question": "What is ∫ x/(x + 1) dx?",
        "options": {
            "A": "x - ln|x + 1| + C",
            "B": "ln|x + 1| + C",
            "C": "x·ln|x + 1| + C",
            "D": "ln|x| + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ x^4·ln(x) dx?",
        "options": {
            "A": "(1/5)x^5·ln(x) - (1/25)x^5 + C",
            "B": "(1/5)x^5·ln(x) - (1/5)x^5 + C",
            "C": "x^5·ln(x) + C",
            "D": "x^4·ln(x) + C"
        },
        "answer": "B"
    },
    {
        "question": "What is ∫ sec(x) dx?",
        "options": {
            "A": "ln|sec(x) + tan(x)| + C",
            "B": "arctan(x) + C",
            "C": "tan(x) + C",
            "D": "sec^2(x) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ x²·sin(x) dx?",
        "options": {
            "A": "-x²·cos(x) + 2x·sin(x) + 2cos(x) + C",
            "B": "x²·cos(x) - 2x·sin(x) + 2cos(x) + C",
            "C": "-x²·sin(x) + 2x·cos(x) - 2sin(x) + C",
            "D": "x²·sin(x) - 2x·cos(x) + 2sin(x) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ (1/(1 - x²)) dx?",
        "options": {
            "A": "(1/2)ln|(1 + x)/(1 - x)| + C",
            "B": "arcsin(x) + C",
            "C": "arctan(x) + C",
            "D": "ln|1 - x^2| + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ dx/(x² + a²)?",
        "options": {
            "A": "(1/a)·arctan(x/a) + C",
            "B": "arcsin(x/a) + C",
            "C": "ln|x² + a²| + C",
            "D": "(1/2a)·arctan(x/a) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ e^x·cos(x) dx?",
        "options": {
            "A": "(1/2)e^x·(cos(x) + sin(x)) + C",
            "B": "e^x·(sin(x) + cos(x))/2 + C",
            "C": "e^x·(cos(x) - sin(x))/2 + C",
            "D": "e^x·(cos(x) + sin(x)) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ tan(x)·sec²(x) dx?",
        "options": {
            "A": "(1/2)·tan²(x) + C",
            "B": "sec(x) + C",
            "C": "tan(x) + C",
            "D": "sec²(x) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ dx/(sqrt(1 - x²))?",
        "options": {
            "A": "arcsin(x) + C",
            "B": "arctan(x) + C",
            "C": "ln|x + sqrt(1 - x²)| + C",
            "D": "arccos(x) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ x·e^(x²) dx?",
        "options": {
            "A": "(1/2)e^(x²) + C",
            "B": "e^(x²)/2 + C",
            "C": "e^(x²) + C",
            "D": "x²·e^(x²) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ (1/sqrt(4 - x²)) dx?",
        "options": {
            "A": "arcsin(x/2) + C",
            "B": "arccos(x/2) + C",
            "C": "arctan(x/2) + C",
            "D": "(1/2)arcsin(x) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ sin²(x) dx?",
        "options": {
            "A": "(1/2)x - (1/4)sin(2x) + C",
            "B": "(1/2)x + (1/4)sin(2x) + C",
            "C": "sin(x) - cos(x) + C",
            "D": "x - sin(x)cos(x) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ dx/(x² + 2x + 2)?",
        "options": {
            "A": "arctan(x + 1) + C",
            "B": "(1/√3)·arctan((x + 1)/1) + C",
            "C": "arctan(x/2) + C",
            "D": "arctan((x + 1)/1) + C"
        },
        "answer": "D"
    },
    {
        "question": "What is ∫ x·sqrt(x + 1) dx?",
        "options": {
            "A": "(2/5)(x + 1)^(5/2) - (4/3)(x + 1)^(3/2) + C",
            "B": "(2/5)(x + 1)^(5/2) + C",
            "C": "(2/3)(x + 1)^(3/2) - C",
            "D": "sqrt(x + 1)·x + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ dx/(x² - 4)?",
        "options": {
            "A": "(1/4)ln|(x - 2)/(x + 2)| + C",
            "B": "(1/2)ln|(x - 2)/(x + 2)| + C",
            "C": "(1/4)ln|x² - 4| + C",
            "D": "(1/2)arctan(x/2) + C"
        },
        "answer": "B"
    },
    {
        "question": "What is ∫ cos(x)·ln(x) dx?",
        "options": {
            "A": "ln(x)·sin(x) - ∫ sin(x)/x dx + C",
            "B": "ln(x)·cos(x) + C",
            "C": "sin(x)·ln(x) + C",
            "D": "ln(x)·sin(x) + C"
        },
        "answer": "A"
    }
]

integration_questions_hard = [
    {
        "question": "What is ∫ (2x)/(x^2 + 1)^2 dx?",
        "options": {
            "A": "-1/(x^2 + 1) + C",
            "B": "ln(x^2 + 1) + C",
            "C": "x/(x^2 + 1) + C",
            "D": "arctan(x) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ x^3·e^(x^2) dx?",
        "options": {
            "A": "(1/2)x^2·e^(x^2) + C",
            "B": "(1/2)x^2·e^(x^2) - (1/2)e^(x^2) + C",
            "C": "(1/2)x^2·e^(x^2) + (1/4)e^(x^2) + C",
            "D": "(1/2)x^2·e^(x^2) - (1/4)e^(x^2) + C"
        },
        "answer": "B"
    },
    {
        "question": "What is ∫ (ln(x))^3 / x dx?",
        "options": {
            "A": "(1/4)(ln(x))^4 + C",
            "B": "(1/3)(ln(x))^3 + C",
            "C": "(ln(x))^4 + C",
            "D": "x·(ln(x))^3 + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ x^4 / sqrt(1 - x^2) dx?",
        "options": {
            "A": "(1/8)(3x^2 - 1)·arcsin(x) + (x^3·sqrt(1 - x^2))/4 + C",
            "B": "arcsin(x) + C",
            "C": "x^4·arcsin(x) + C",
            "D": "None of the above"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ (1 + ln(x))^2 / x dx?",
        "options": {
            "A": "(1/3)(1 + ln(x))^3 + C",
            "B": "ln(x) + ln(x)^2 + C",
            "C": "(1 + ln(x))^3/3 + C",
            "D": "x·(1 + ln(x))^2 + C"
        },
        "answer": "C"
    },
    {
        "question": "What is ∫ dx / (x·sqrt(x^2 - 1)) ?",
        "options": {
            "A": "arcsec(x) + C",
            "B": "arccos(x) + C",
            "C": "arcsin(x) + C",
            "D": "arctan(x) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ sin(x)/cos^3(x) dx?",
        "options": {
            "A": "sec^2(x)/2 + C",
            "B": "sec(x) + C",
            "C": "sec^2(x) + C",
            "D": "tan(x)·sec(x) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ (x^2 + 1)/(x^2 - 1) dx?",
        "options": {
            "A": "x + 2arctanh(x) + C",
            "B": "x + ln|x - 1| - ln|x + 1| + C",
            "C": "x + 2ln|(x - 1)/(x + 1)| + C",
            "D": "x + ln|x^2 - 1| + C"
        },
        "answer": "B"
    },
    {
        "question": "What is ∫ (1 + tan^2(x)) / sec(x) dx?",
        "options": {
            "A": "tan(x) + C",
            "B": "sec(x) + C",
            "C": "sec(x)·tan(x) + C",
            "D": "sec(x) + tan(x) + C"
        },
        "answer": "B"
    },
    {
        "question": "What is ∫ dx / (x^4 + 1)?",
        "options": {
            "A": "Complicated form with arctan and log",
            "B": "Use partial fractions, not elementary",
            "C": "arctan(x^2) + C",
            "D": "Not expressible in terms of elementary functions"
        },
        "answer": "B"
    },
    {
        "question": "What is ∫ x^2 / sqrt(4 - x^2) dx?",
        "options": {
            "A": "-(1/2)x·sqrt(4 - x^2) + 2arcsin(x/2) + C",
            "B": "2arcsin(x/2) + C",
            "C": "x^2·sqrt(4 - x^2) + C",
            "D": "x·sqrt(4 - x^2) + arcsin(x/2) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ tan^3(x) dx?",
        "options": {
            "A": "sec^2(x) - ln|cos(x)| + C",
            "B": "sec^2(x)·tan(x) - ln|cos(x)| + C",
            "C": "sec(x)·tan(x) - ln|cos(x)| + C",
            "D": "(1/2)tan^2(x) + ln|cos(x)| + C"
        },
        "answer": "D"
    },
    {
        "question": "What is ∫ sin^3(x) dx?",
        "options": {
            "A": "-(1/3)cos^3(x) + C",
            "B": "-cos(x) + (1/3)cos^3(x) + C",
            "C": "-cos(x) + (1/3)cos^3(x) + C",
            "D": "(1/3)cos^3(x) - cos(x) + C"
        },
        "answer": "D"
    },
    {
        "question": "What is ∫ (cos(x) - sin(x)) / (cos(x) + sin(x)) dx?",
        "options": {
            "A": "ln|cos(x) + sin(x)| + C",
            "B": "tan(x) + C",
            "C": "sec(x) + tan(x) + C",
            "D": "sqrt(2)x + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ (x + 1)/(x^2 + 2x + 2) dx?",
        "options": {
            "A": "(1/2)ln(x^2 + 2x + 2) + arctan(x + 1) + C",
            "B": "ln(x^2 + 2x + 2) + C",
            "C": "arctan(x + 1) + C",
            "D": "(1/2)ln(x^2 + 2x + 2) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ x / sqrt(x^2 + a^2) dx?",
        "options": {
            "A": "sqrt(x^2 + a^2) + C",
            "B": "arcsin(x/a) + C",
            "C": "arctan(x/a) + C",
            "D": "ln|x + sqrt(x^2 + a^2)| + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ dx / sqrt(9 + 4x^2)?",
        "options": {
            "A": "(1/2)arcsinh(2x/3) + C",
            "B": "(1/2)arctan(2x/3) + C",
            "C": "(1/3)arcsin(2x/3) + C",
            "D": "(1/3)arctan(2x/3) + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ x·arctan(x) dx?",
        "options": {
            "A": "(1/2)x^2·arctan(x) - (1/2)∫ x^2 / (1 + x^2) dx + C",
            "B": "(1/2)x^2·arctan(x) - (1/2)ln(1 + x^2) + C",
            "C": "(1/2)x^2·arctan(x) - (1/2)x + C",
            "D": "arctan(x)·x + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ (x^2 + 1)^2 dx?",
        "options": {
            "A": "(1/5)x^5 + (2/3)x^3 + x + C",
            "B": "x^5 + 2x^3 + x + C",
            "C": "x + 2x^3 + x^5 + C",
            "D": "(x^2 + 1)^3 / 3 + C"
        },
        "answer": "A"
    },
    {
        "question": "What is ∫ x / (x^2 + 1)^2 dx?",
        "options": {
            "A": "-1 / (2(x^2 + 1)) + C",
            "B": "-x / (x^2 + 1) + C",
            "C": "arctan(x) / (x^2 + 1) + C",
            "D": "(1/2)ln(x^2 + 1) + C"
        },
        "answer": "A"
    }
    # 10 more questions can be added here...
]

differentiation_questions_easy = [
    {
        "question": "What is d/dx (x^2)?",
        "options": {"A": "x", "B": "2x", "C": "x^2", "D": "2"},
        "answer": "B"
    },
    {
        "question": "What is d/dx (5x)?",
        "options": {"A": "0", "B": "x", "C": "5", "D": "5x^2"},
        "answer": "C"
    },
    {
        "question": "What is the derivative of a constant?",
        "options": {"A": "0", "B": "1", "C": "x", "D": "Undefined"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^3)?",
        "options": {"A": "3x^2", "B": "x^2", "C": "x^3", "D": "3x"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^4 + x^2)?",
        "options": {"A": "4x^3 + 2x", "B": "3x^3", "C": "2x^2 + 2x", "D": "4x"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (7)?",
        "options": {"A": "1", "B": "7", "C": "x", "D": "0"},
        "answer": "D"
    },
    {
        "question": "What is the derivative of x?",
        "options": {"A": "x", "B": "0", "C": "1", "D": "2"},
        "answer": "C"
    },
    {
        "question": "What is d/dx (2x^2 + 3x)?",
        "options": {"A": "4x + 3", "B": "2x + 3", "C": "4x", "D": "2x"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^5)?",
        "options": {"A": "5x^4", "B": "5x^5", "C": "x^4", "D": "x^5 + C"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (10x^3)?",
        "options": {"A": "10x^2", "B": "30x^2", "C": "x^2", "D": "30x^3"},
        "answer": "B"
    },
    {
        "question": "What is d/dx (x + 1)^2?",
        "options": {"A": "2(x + 1)", "B": "x^2 + 2x + 1", "C": "2x", "D": "x + 1"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^2 + 4)?",
        "options": {"A": "2x", "B": "2", "C": "x", "D": "0"},
        "answer": "A"
    },
    {
        "question": "What is the slope of y = 3x + 2?",
        "options": {"A": "3", "B": "2", "C": "1", "D": "0"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^0)?",
        "options": {"A": "0", "B": "1", "C": "x", "D": "Undefined"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (4x^2 - 3x)?",
        "options": {"A": "8x - 3", "B": "4x - 3", "C": "4x", "D": "3x"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^6)?",
        "options": {"A": "6x^5", "B": "6x^6", "C": "x^5", "D": "x^6 + C"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (3x^2)?",
        "options": {"A": "3x", "B": "6x", "C": "9x", "D": "x^2"},
        "answer": "B"
    },
    {
        "question": "What is d/dx (x^2 + x)?",
        "options": {"A": "2x + 1", "B": "x^2 + 1", "C": "2x", "D": "x + 1"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (9x)?",
        "options": {"A": "9", "B": "x", "C": "0", "D": "1"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^3 + 5x^2)?",
        "options": {"A": "3x^2 + 10x", "B": "3x + 10x^2", "C": "5x^2 + 3", "D": "x^2 + 2x"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (2)?",
        "options": {"A": "0", "B": "2", "C": "1", "D": "x"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^7)?",
        "options": {"A": "7x^6", "B": "7x^7", "C": "x^6", "D": "x^7 + C"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (4x + 9)?",
        "options": {"A": "4", "B": "9", "C": "13", "D": "x"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^2 + 2x + 1)?",
        "options": {"A": "2x + 2", "B": "x^2", "C": "2x", "D": "2x + 1"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^8)?",
        "options": {"A": "8x^7", "B": "8x^8", "C": "x^7", "D": "x^8 + C"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^0)?",
        "options": {"A": "0", "B": "1", "C": "x", "D": "x^0"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^1)?",
        "options": {"A": "1", "B": "x", "C": "0", "D": "2x"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^9)?",
        "options": {"A": "9x^8", "B": "9x^9", "C": "x^8", "D": "x^9 + C"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^3 + x)?",
        "options": {"A": "3x^2 + 1", "B": "3x + 1", "C": "x^2 + 1", "D": "3x^2"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^2 - 4)?",
        "options": {"A": "2x", "B": "-4", "C": "0", "D": "2"},
        "answer": "A"
    }
]

differentiation_questions_medium = [
    {
        "question": "What is d/dx (sin(x))?",
        "options": {"A": "cos(x)", "B": "-cos(x)", "C": "sin(x)", "D": "-sin(x)"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (cos(x))?",
        "options": {"A": "-cos(x)", "B": "-sin(x)", "C": "cos(x)", "D": "sin(x)"},
        "answer": "B"
    },
    {
        "question": "What is d/dx (e^x)?",
        "options": {"A": "x·e^(x-1)", "B": "e^x", "C": "ln(x)", "D": "xe^x"},
        "answer": "B"
    },
    {
        "question": "What is d/dx (ln(x))?",
        "options": {"A": "1/x", "B": "x", "C": "ln(x)", "D": "xln(x)"},
        "answer": "A"
    },
    {
        "question": "What is the derivative of tan(x)?",
        "options": {"A": "sec(x)", "B": "sec^2(x)", "C": "tan(x)", "D": "-csc^2(x)"},
        "answer": "B"
    },
    {
        "question": "What is d/dx (x·sin(x))?",
        "options": {"A": "x·cos(x)", "B": "x·cos(x) + sin(x)", "C": "x·sin(x)", "D": "cos(x)"},
        "answer": "B"
    },
    {
        "question": "What is d/dx (x·e^x)?",
        "options": {"A": "e^x", "B": "e^x + x·e^x", "C": "x^2·e^x", "D": "e^x - x·e^x"},
        "answer": "B"
    },
    {
        "question": "What is d/dx (x^2·ln(x))?",
        "options": {"A": "2x·ln(x) + x", "B": "x^2 / ln(x)", "C": "2ln(x)", "D": "2x + ln(x)"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (sin(x^2))?",
        "options": {"A": "cos(x^2)", "B": "2x·cos(x^2)", "C": "2x·sin(x^2)", "D": "-2x·cos(x^2)"},
        "answer": "B"
    },
    {
        "question": "What is d/dx (ln(x^2))?",
        "options": {"A": "1/x^2", "B": "2/x", "C": "ln(2x)", "D": "x·ln(x)"},
        "answer": "B"
    },
    {
        "question": "What is d/dx (1/x)?",
        "options": {"A": "x^-2", "B": "-1/x^2", "C": "-x^-2", "D": "1/x^2"},
        "answer": "B"
    },
    {
        "question": "What is d/dx (x / (x + 1))?",
        "options": {"A": "1/(x + 1)^2", "B": "1/(x + 1)", "C": "1/(x^2 + 1)", "D": "1"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (e^(3x))?",
        "options": {"A": "e^(3x)", "B": "3e^(3x)", "C": "ln(3x)", "D": "3x·e^x"},
        "answer": "B"
    },
    {
        "question": "What is d/dx (ln(5x))?",
        "options": {"A": "1/x", "B": "1/(5x)", "C": "5/x", "D": "1/x + ln(5)"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (cos(2x))?",
        "options": {"A": "-sin(2x)", "B": "-2sin(2x)", "C": "-cos(2x)", "D": "2cos(2x)"},
        "answer": "B"
    },
    {
        "question": "What is d/dx (x^3·cos(x))?",
        "options": {"A": "3x^2·cos(x) - x^3·sin(x)", "B": "3x^2·cos(x)", "C": "x^3·cos(x)", "D": "cos(x) - 3x^2"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (tan^2(x))?",
        "options": {"A": "2tan(x)", "B": "2tan(x)·sec^2(x)", "C": "sec^2(x)", "D": "2sec(x)tan(x)"},
        "answer": "B"
    },
    {
        "question": "What is d/dx (sqrt(x))?",
        "options": {"A": "1/2x", "B": "1/(2√x)", "C": "√x", "D": "2√x"},
        "answer": "B"
    },
    {
        "question": "What is d/dx (x^2 / sin(x))?",
        "options": {
            "A": "(2x·sin(x) - x^2·cos(x)) / sin^2(x)",
            "B": "x / sin(x)",
            "C": "2x / sin(x)",
            "D": "x^2·cos(x)"
        },
        "answer": "A"
    },
    {
        "question": "What is d/dx (ln(x^3 + 1))?",
        "options": {
            "A": "3x^2 / (x^3 + 1)",
            "B": "3x / (x + 1)",
            "C": "1 / ln(x^3 + 1)",
            "D": "x^3 / (x^3 + 1)"
        },
        "answer": "A"
    },
    {
        "question": "What is d/dx (x·ln(x))?",
        "options": {"A": "1 + ln(x)", "B": "ln(x)", "C": "x / ln(x)", "D": "1/x"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (x / ln(x))?",
        "options": {
            "A": "(ln(x) - 1) / (ln(x))^2",
            "B": "1 / x·ln(x)",
            "C": "ln(x)^2 / x",
            "D": "(1 - ln(x)) / (ln(x))^2"
        },
        "answer": "A"
    },
    {
        "question": "What is d/dx (sec(x))?",
        "options": {"A": "sec(x)·tan(x)", "B": "sec^2(x)", "C": "cos(x)", "D": "-sin(x)"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (sin(x)·cos(x))?",
        "options": {
            "A": "cos^2(x) - sin^2(x)",
            "B": "cos^2(x) + sin^2(x)",
            "C": "1",
            "D": "-1"
        },
        "answer": "A"
    },
    {
        "question": "What is d/dx (arctan(x))?",
        "options": {"A": "1 / (1 + x^2)", "B": "1 / x", "C": "arctan(x)", "D": "ln(x)"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (arcsin(x))?",
        "options": {"A": "1 / sqrt(1 - x^2)", "B": "1 / sqrt(1 + x^2)", "C": "sqrt(1 - x^2)", "D": "arcsin(x)"},
        "answer": "A"
    },
    {
        "question": "What is d/dx (log_10(x))?",
        "options": {
            "A": "1 / (x ln(10))",
            "B": "1 / (x ln(x))",
            "C": "ln(x) / x",
            "D": "1 / x"
        },
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^x)?",
        "options": {
            "A": "x^x(1 + ln(x))",
            "B": "x^x·ln(x)",
            "C": "x·ln(x)",
            "D": "x^(x-1)"
        },
        "answer": "A"
    },
    {
        "question": "What is d/dx (cos^2(x))?",
        "options": {
            "A": "-2cos(x)sin(x)",
            "B": "2cos(x)",
            "C": "sin(2x)",
            "D": "-sin(2x)"
        },
        "answer": "A"
    }
]

differentiation_questions_hard = [
    {
        "question": "If y = x^x, what is dy/dx?",
        "options": {
            "A": "x^x (1 + ln(x))",
            "B": "x^x ln(x)",
            "C": "x^(x-1)",
            "D": "x·x^x"
        },
        "answer": "A"
    },
    {
        "question": "If y = ln(sin(x)), what is dy/dx?",
        "options": {
            "A": "cot(x)",
            "B": "1/sin(x)",
            "C": "cos(x)/sin(x)",
            "D": "1/tan(x)"
        },
        "answer": "C"
    },
    {
        "question": "What is d/dx of arccos(x)?",
        "options": {
            "A": "-1/√(1 - x^2)",
            "B": "1/√(1 - x^2)",
            "C": "arccos(x)",
            "D": "ln|x|"
        },
        "answer": "A"
    },
    {
        "question": "Differentiate y = ln(x^2 + 1)",
        "options": {
            "A": "2x / (x^2 + 1)",
            "B": "2x ln(x^2 + 1)",
            "C": "1 / (x^2 + 1)",
            "D": "ln(2x)"
        },
        "answer": "A"
    },
    {
        "question": "If y = e^(sin(x)), what is dy/dx?",
        "options": {
            "A": "cos(x) e^(sin(x))",
            "B": "sin(x) e^(cos(x))",
            "C": "e^x cos(x)",
            "D": "cos(x) sin(x)"
        },
        "answer": "A"
    },
    {
        "question": "Implicit diff: x^2 + y^2 = 25, what is dy/dx?",
        "options": {
            "A": "-x/y",
            "B": "-y/x",
            "C": "x/y",
            "D": "2x/2y"
        },
        "answer": "A"
    },
    {
        "question": "d/dx of ln|cos(x)| is:",
        "options": {
            "A": "-tan(x)",
            "B": "tan(x)",
            "C": "-sin(x)/cos(x)",
            "D": "-sec(x)"
        },
        "answer": "A"
    },
    {
        "question": "Differentiate y = (x^2 + 1)^5",
        "options": {
            "A": "10x(x^2 + 1)^4",
            "B": "5(x^2 + 1)^4",
            "C": "5x(x^2 + 1)^4",
            "D": "5(x^2 + 1)^5"
        },
        "answer": "C"
    },
    {
        "question": "If y = arctan(3x), what is dy/dx?",
        "options": {
            "A": "3 / (1 + 9x^2)",
            "B": "1 / (1 + x^2)",
            "C": "1 / (1 + 3x^2)",
            "D": "3 / (1 + x^2)"
        },
        "answer": "A"
    },
    {
        "question": "d/dx of ln(x^3 + x^2) is:",
        "options": {
            "A": "(3x^2 + 2x) / (x^3 + x^2)",
            "B": "ln(x^2)",
            "C": "3x^2 + 2x",
            "D": "1 / x^2"
        },
        "answer": "A"
    },
    {
        "question": "Differentiate y = (sin(x))^x",
        "options": {
            "A": "(sin(x))^x (ln(sin(x)) + x·cot(x))",
            "B": "x (sin(x))^(x - 1)",
            "C": "x·cos(x)",
            "D": "(sin(x))^x + ln(x)"
        },
        "answer": "A"
    },
    {
        "question": "If x = tan(y), then dy/dx = ?",
        "options": {
            "A": "1 / (1 + x^2)",
            "B": "1 / cos^2(x)",
            "C": "cos^2(x)",
            "D": "tan(x)"
        },
        "answer": "A"
    },
    {
        "question": "Differentiate y = arccos(2x)",
        "options": {
            "A": "-2 / sqrt(1 - 4x^2)",
            "B": "-2x / sqrt(1 - 4x^2)",
            "C": "1 / sqrt(1 - x^2)",
            "D": "2 / sqrt(1 - x^2)"
        },
        "answer": "A"
    },
    {
        "question": "d/dx of y = (x^2 + 3)^4 (chain rule):",
        "options": {
            "A": "8x(x^2 + 3)^3",
            "B": "4(x^2 + 3)^3",
            "C": "8x(x^2 + 3)^4",
            "D": "4x(x^2 + 3)^3"
        },
        "answer": "D"
    },
    {
        "question": "What is d/dx (x^x^x)?",
        "options": {
            "A": "Too complex – needs logarithmic diff",
            "B": "x^x",
            "C": "x^(x-1)",
            "D": "x·x^x"
        },
        "answer": "A"
    },
    {
        "question": "d/dx of (ln(x))^2 is:",
        "options": {
            "A": "2ln(x)/x",
            "B": "2/x",
            "C": "2ln(x)^2",
            "D": "ln(x)"
        },
        "answer": "A"
    },
    {
        "question": "What is d/dx (1 / ln(x))?",
        "options": {
            "A": "-1 / (x·ln(x)^2)",
            "B": "1 / ln(x)^2",
            "C": "-1 / ln(x)^2",
            "D": "-ln(x)/x"
        },
        "answer": "A"
    },
    {
        "question": "Differentiate y = x^3 / (x^2 + 1)",
        "options": {
            "A": "(x^4 + 3x^2) / (x^2 + 1)^2",
            "B": "(x^4 + 1) / (x^2 + 1)^2",
            "C": "(x^4 + 1) / (x^2 + 1)",
            "D": "(x^4 + 3x^2 + 1) / (x^2 + 1)^2"
        },
        "answer": "A"
    },
    {
        "question": "What is dy/dx if y^2 + x^2 = 1?",
        "options": {
            "A": "-x/y",
            "B": "-y/x",
            "C": "x/y",
            "D": "2x"
        },
        "answer": "A"
    },
    {
        "question": "What is d/dx of x^2 ln(x)?",
        "options": {
            "A": "2x ln(x) + x",
            "B": "ln(x) + 2x",
            "C": "2x / ln(x)",
            "D": "x^2 / ln(x)"
        },
        "answer": "A"
    },
    {
        "question": "d/dx of arccot(x) is:",
        "options": {
            "A": "-1 / (1 + x^2)",
            "B": "1 / (1 + x^2)",
            "C": "-1 / (1 - x^2)",
            "D": "1 / sqrt(1 + x^2)"
        },
        "answer": "A"
    },
    {
        "question": "What is the derivative of y = ln(x^2 + sin(x))?",
        "options": {
            "A": "(2x + cos(x)) / (x^2 + sin(x))",
            "B": "2x + cos(x)",
            "C": "ln(x^2 + sin(x))",
            "D": "ln(sin(x)) + 2x"
        },
        "answer": "A"
    },
    {
        "question": "If y = (cos(x))^2, what is dy/dx?",
        "options": {
            "A": "-2cos(x)sin(x)",
            "B": "2cos(x)",
            "C": "cos^2(x)",
            "D": "sin(2x)"
        },
        "answer": "A"
    },
    {
        "question": "What is d/dx (e^(x^2))?",
        "options": {
            "A": "2x·e^(x^2)",
            "B": "e^(x^2) + 2x",
            "C": "2e^x",
            "D": "2x + e^x"
        },
        "answer": "A"
    },
    {
        "question": "What is d/dx (x^2 e^x)?",
        "options": {
            "A": "x^2 e^x + 2x e^x",
            "B": "x e^x",
            "C": "2x e^x",
            "D": "x^2 e^x"
        },
        "answer": "A"
    },
    {
        "question": "d/dx of (tan(x) / x):",
        "options": {
            "A": "(x sec^2(x) - tan(x)) / x^2",
            "B": "(sec^2(x)) / x",
            "C": "tan(x) / x^2",
            "D": "sec^2(x) / x^2"
        },
        "answer": "A"
    },
    {
        "question": "What is d/dx (sqrt(ln(x)))?",
        "options": {
            "A": "1 / (2x·sqrt(ln(x)))",
            "B": "1 / sqrt(x·ln(x))",
            "C": "ln(x) / (2√x)",
            "D": "1 / x"
        },
        "answer": "A"
    },
    {
        "question": "What is d/dx of tan^(-1)(1/x)?",
        "options": {
            "A": "-1 / (x^2 + 1)",
            "B": "-1 / (1 + x^2)",
            "C": "1 / (x^2 + 1)",
            "D": "-1 / (1 + (1/x)^2)"
        },
        "answer": "A"
    }
]


class MathGame:
    # Constants for better maintainability
    DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
    DIFFICULTY_COLORS = {"easy": "#4CAF50", "medium": "#FF9800", "hard": "#f44336"}
    GAME_MODES = ["algebra", "square_root"]
    
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
        self.root.geometry("1000x800")
        
        # Load and resize background image to fit window
        original_bg = Image.open("assets/pokemon_bg3.png")
        # Resize to window dimensions (1000x800)
        self.bg_image = original_bg.resize((1000, 800), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

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
        self.leaderboard = self.load_leaderboard()
        self.player_gold_coins = self.load_player_gold_coins()
        self.store_items = {
            "Extra Life": {"price": 50, "description": "Add 1 extra life to your game"},
            "Time Extension": {"price": 30, "description": "Add 5 seconds to timer"},
            "Score Multiplier": {"price": 100, "description": "Double points for 3 questions"},
            "Hint System": {"price": 75, "description": "Get hints for difficult questions"}
        }

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
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_centered_frame(self):
        """Create a centered frame for content"""
        frame = tk.Frame(self.root, bg="#4EC7D7")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        return frame

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
        self.root.configure(bg="#E8F5E8")  # Light green background
        
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
        if not username:
            messagebox.showwarning("Name Required", "Please enter your name!")
            return
        
        if len(username) > 20:
            messagebox.showwarning("Name Too Long", "Please enter a name with 20 characters or less!")
            return
        
        self.player_name = username
        self.show_difficulty_selection()

    def show_difficulty_selection(self):
        """Show difficulty selection page"""
        self.clear_window()
        self.root.configure(bg="#FFF3E0")  # Light orange background
        
        difficulty_frame = self.create_centered_frame()
        
        # Header
        tk.Label(difficulty_frame, text=f"Welcome, {self.player_name}!", 
                font=self.title_font).grid(row=0, column=0, pady=10)
        
        player_coins = self.get_player_gold_coins(self.player_name)
        tk.Label(difficulty_frame, text=f"💰 Gold Coins: {player_coins}", 
                font=self.label_font, fg="#FFD700").grid(row=1, column=0, pady=5)
        
        tk.Label(difficulty_frame, text="Select Difficulty:", 
                font=self.label_font).grid(row=2, column=0, pady=10)
        
        # Difficulty buttons
        self.difficulty_var = tk.StringVar(value="none")
        difficulty_buttons_frame = tk.Frame(difficulty_frame)
        difficulty_buttons_frame.grid(row=3, column=0, pady=10)
        
        for i, difficulty in enumerate(self.DIFFICULTY_LEVELS):
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
        if not self.difficulty or self.difficulty not in self.DIFFICULTY_LEVELS:
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
            # ("Trigonometry", self.button_color, "white", self.start_trigonometry_game),
            # ("Logarithms", self.button_color, "white", self.start_logarithms_game),
            ("Back", "#f44336", "white", self.show_difficulty_selection)
        ]
        
        for i, (text, bg, fg, command) in enumerate(test_buttons, 2):
            tk.Button(test_frame, text=text, font=self.button_font, bg=bg,
                     fg=fg, command=command).grid(row=i, column=0, pady=10)
    def setup_game_ui(self, game_mode="algebra"):
        """Setup common game UI elements"""
        self.clear_window()
        self.root.configure(bg="#F3E5F5")  # Light purple background
        
        self.game_frame = self.create_centered_frame()
        
        # Player info
        tk.Label(self.game_frame, text=f"Player: {self.player_name}", 
                font=self.label_font).grid(row=0, column=0, pady=5)
        
        # Game stats
        self.score_label = tk.Label(self.game_frame, text=f"Score: {self.score}", 
                                   font=self.label_font)
        self.score_label.grid(row=1, column=0, pady=5)
        
        self.time_label = tk.Label(self.game_frame, text=f"Time: {self.time_left}s", 
                                  font=self.label_font)
        self.time_label.grid(row=2, column=0, pady=5)
        
        self.lives_label = tk.Label(self.game_frame, text=self.lives_system.get_player_life_display(), 
                                   font=self.label_font, fg="red")
        self.lives_label.grid(row=3, column=0, pady=5)
        
        # Question area
        self.question_label = tk.Label(self.game_frame, text="", font=self.label_font)
        self.question_label.grid(row=4, column=0, pady=10)
        
        self.answer_entry = tk.Entry(self.game_frame, font=self.label_font)
        self.answer_entry.grid(row=5, column=0, pady=10)
        
        # Action buttons
        submit_command = self.check_square_root_answer if game_mode == "square_root" else self.check_algebra_answer
        self.answer_entry.bind("<Return>", submit_command)
        
        tk.Button(self.game_frame, text="Submit", font=self.button_font, bg=self.button_color,
                  fg="white", command=submit_command).grid(row=6, column=0, pady=10)
        tk.Button(self.game_frame, text="Back", font=self.button_font, bg="#f44336",
                  fg="white", command=self.confirm_back_to_menu).grid(row=7, column=0, pady=10)

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
        self.time_left = 15
        self.game_mode = "square_root"
        self.setup_pokemon_battle_ui()
        self.generate_square_root_question()
        self.start_timer()

    def reset_game_state(self):
        """Reset game state for new game"""
        self.score = 0
        self.streak = 0
        self.lives_system.reset_all_lives()  # Reset both player and enemy lives

    def start_integration_game(self):
        """Start integration game with Pokémon battle GUI"""
        self.reset_game_state()
        self.game_mode = "integration"
        self.setup_pokemon_battle_ui()
        self.generate_integration_question()
        self.start_timer()

    def setup_integration_ui(self):
        """Setup integration game UI with multiple choice"""
        self.clear_window()
        self.root.configure(bg="#E8F5E8")  # Light green background
        
        self.game_frame = self.create_centered_frame()
        
        # Player info
        tk.Label(self.game_frame, text=f"Player: {self.player_name}", 
                font=self.label_font).grid(row=0, column=0, pady=5)
        
        # Game stats
        self.score_label = tk.Label(self.game_frame, text=f"Score: {self.score}", 
                                   font=self.label_font)
        self.score_label.grid(row=1, column=0, pady=5)
        
        self.time_label = tk.Label(self.game_frame, text=f"Time: {self.time_left}s", 
                                  font=self.label_font)
        self.time_label.grid(row=2, column=0, pady=5)
        
        self.lives_label = tk.Label(self.game_frame, text=self.lives_system.get_player_life_display(), 
                                   font=self.label_font, fg="red")
        self.lives_label.grid(row=3, column=0, pady=5)
        
        # Question area
        self.question_label = tk.Label(self.game_frame, text="", font=self.label_font, wraplength=500)
        self.question_label.grid(row=4, column=0, pady=10)
        
        # Options frame
        self.options_frame = tk.Frame(self.game_frame)
        self.options_frame.grid(row=5, column=0, pady=10)
        
        # Action buttons
        tk.Button(self.game_frame, text="Back", font=self.button_font, bg="#f44336",
                  fg="white", command=self.confirm_back_to_menu).grid(row=6, column=0, pady=10)

    def generate_integration_question(self):
        """Generate integration question based on difficulty"""
        # Select question set based on difficulty
        if self.difficulty == "easy":
            question_set = integration_questions_simple
        elif self.difficulty == "medium":
            question_set = integration_questions_medium
        elif self.difficulty == "hard":
            question_set = integration_questions_hard
        else:
            # Default to simple if difficulty not set
            question_set = integration_questions_simple
            
        self.current_question = random.choice(question_set)
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

    def check_integration_answer(self, selected_option):
        """Check integration answer with difficulty-based scoring and Pokémon battle effects"""
        correct_answer = self.current_question["answer"]
        if selected_option == correct_answer:
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
            attack_messages = [
                "⚡ Thunderbolt hits! Critical damage!",
                "⚡ Electric attack successful! Enemy stunned!",
                "⚡ Pikachu's attack lands perfectly!",
                "⚡ Thunder Shock connects! Enemy weakened!"
            ]
            battle_message = random.choice(attack_messages)
            self.battle_message.config(text=battle_message, fg="#006400")  # Dark green for success
            
            # Flash the enemy Pokémon red when hit
            self.flash_enemy_red()
            
            self.handle_correct_answer(coins_earned, message)
        else:
            # Wrong answer - attack misses and player gets hit
            miss_messages = [
                "💧 Squirtle dodged the attack!",
                "💧 Enemy used Protect! Attack blocked!",
                "💧 Attack missed! Enemy counterattacks!",
                "💧 Squirtle's Water Gun deflects the attack!"
            ]
            battle_message = random.choice(miss_messages)
            self.battle_message.config(text=battle_message, fg="#8B0000")  # Dark red for failure
            
            # Flash the player's Pokémon red when hit
            self.flash_pokemon_red()
            
            self.handle_wrong_answer("Incorrect!", f"Correct answer: {correct_answer}")

    def start_differentiation_game(self):
        """Start differentiation game with Pokémon battle GUI"""
        self.reset_game_state()
        self.game_mode = "differentiation"
        self.setup_pokemon_battle_ui()
        self.generate_differentiation_question()
        self.start_timer()

    def setup_differentiation_ui(self):
        """Setup differentiation game UI with multiple choice"""
        self.clear_window()
        self.root.configure(bg="#FFF8E1")  # Light yellow background
        
        self.game_frame = self.create_centered_frame()
        
        # Player info
        tk.Label(self.game_frame, text=f"Player: {self.player_name}", 
                font=self.label_font).grid(row=0, column=0, pady=5)
        
        # Game stats
        self.score_label = tk.Label(self.game_frame, text=f"Score: {self.score}", 
                                   font=self.label_font)
        self.score_label.grid(row=1, column=0, pady=5)
        
        self.time_label = tk.Label(self.game_frame, text=f"Time: {self.time_left}s", 
                                  font=self.label_font)
        self.time_label.grid(row=2, column=0, pady=5)
        
        self.lives_label = tk.Label(self.game_frame, text=self.lives_system.get_player_life_display(), 
                                   font=self.label_font, fg="red")
        self.lives_label.grid(row=3, column=0, pady=5)
        
        # Question area
        self.question_label = tk.Label(self.game_frame, text="", font=self.label_font, wraplength=500)
        self.question_label.grid(row=4, column=0, pady=10)
        
        # Options frame
        self.options_frame = tk.Frame(self.game_frame)
        self.options_frame.grid(row=5, column=0, pady=10)
        
        # Action buttons
        tk.Button(self.game_frame, text="Back", font=self.button_font, bg="#f44336",
                  fg="white", command=self.confirm_back_to_menu).grid(row=6, column=0, pady=10)

    def generate_differentiation_question(self):
        """Generate differentiation question based on difficulty"""
        # Select question set based on difficulty
        if self.difficulty == "easy":
            question_set = differentiation_questions_easy
        elif self.difficulty == "medium":
            question_set = differentiation_questions_medium
        elif self.difficulty == "hard":
            question_set = differentiation_questions_hard
        else:
            # Default to easy if difficulty not set
            question_set = differentiation_questions_easy
            
        self.current_question = random.choice(question_set)
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

    def check_differentiation_answer(self, selected_option):
        """Check differentiation answer with difficulty-based scoring and Pokémon battle effects"""
        correct_answer = self.current_question["answer"]
        if selected_option == correct_answer:
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
            attack_messages = [
                "⚡ Thunderbolt hits! Critical damage!",
                "⚡ Electric attack successful! Enemy stunned!",
                "⚡ Pikachu's attack lands perfectly!",
                "⚡ Thunder Shock connects! Enemy weakened!"
            ]
            battle_message = random.choice(attack_messages)
            self.battle_message.config(text=battle_message, fg="#006400")  # Dark green for success
            
            # Flash the enemy Pokémon red when hit
            self.flash_enemy_red()
            
            self.handle_correct_answer(coins_earned, message)
        else:
            # Wrong answer - attack misses and player gets hit
            miss_messages = [
                "💧 Squirtle dodged the attack!",
                "💧 Enemy used Protect! Attack blocked!",
                "💧 Attack missed! Enemy counterattacks!",
                "💧 Squirtle's Water Gun deflects the attack!"
            ]
            battle_message = random.choice(miss_messages)
            self.battle_message.config(text=battle_message, fg="#8B0000")  # Dark red for failure
            
            # Flash the player's Pokémon red when hit
            self.flash_pokemon_red()
            
            self.handle_wrong_answer("Incorrect!", f"Correct answer: {correct_answer}")



    def generate_question(self):
        """Generate algebra question based on difficulty"""
        ranges = {
            "easy": (1, 10),
            "medium": (10, 50),
            "hard": (50, 100)
        }
        
        min_val, max_val = ranges[self.difficulty]
        num1, num2 = random.randint(min_val, max_val), random.randint(min_val, max_val)
        
        operations = ["+", "-", "*", "/"]
        op = random.choice(operations)
        
        if op == "/":
            num1 = num2 * random.randint(1, 10)
            self.current_answer = num1 // num2
        elif op == "+":
            self.current_answer = num1 + num2
        elif op == "-":
            num1, num2 = max(num1, num2), min(num1, num2)
            self.current_answer = num1 - num2
        else:
            self.current_answer = num1 * num2
        
        self.question_label.config(text=f"{num1} {op} {num2} = ?")
        self.battle_message.config(text="⚡ Pikachu is ready to battle! Answer correctly to attack!")
        self.answer_entry.delete(0, tk.END)

    def generate_square_root_question(self):
        """Generate square root question"""
        non_perfect_squares = {
            "easy": [2, 3, 5, 6, 7, 8],
            "medium": [10, 11, 12, 13, 14, 15, 17, 18, 19, 20],
            "hard": [21, 22, 23, 24, 26, 27, 28, 29, 30]
        }
        
        number = random.choice(non_perfect_squares[self.difficulty])
        self.current_answer = math.sqrt(number)
        self.question_label.config(text=f"√{number} = ? (Round to 2 decimal places)")
        self.battle_message.config(text="⚡ Pikachu is ready to battle! Answer correctly to attack!")
        self.answer_entry.delete(0, tk.END)

    def check_algebra_answer(self, event=None):
        """Check algebra answer with Pokémon battle effects"""
        try:
            user_answer = float(self.answer_entry.get())
            if abs(user_answer - self.current_answer) < 0.01:
                # Correct answer - successful attack
                attack_messages = [
                    "⚡ Thunderbolt hits! Critical damage!",
                    "⚡ Electric attack successful! Enemy stunned!",
                    "⚡ Pikachu's attack lands perfectly!",
                    "⚡ Thunder Shock connects! Enemy weakened!"
                ]
                message = random.choice(attack_messages)
                self.battle_message.config(text=message, fg="#006400")  # Dark green for success
                
                # Flash the enemy Pokémon red when hit
                self.flash_enemy_red()
                
                self.handle_correct_answer(2, "Correct!")
            else:
                # Wrong answer - attack misses and player gets hit
                miss_messages = [
                    "💧 Squirtle dodged the attack!",
                    "💧 Enemy used Protect! Attack blocked!",
                    "💧 Attack missed! Enemy counterattacks!",
                    "💧 Squirtle's Water Gun deflects the attack!"
                ]
                message = random.choice(miss_messages)
                self.battle_message.config(text=message, fg="#8B0000")  # Dark red for failure
                
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
            deviation = abs(user_answer - self.current_answer)
            
            points_map = {
                (0, 0.01): (50, "Excellent! Very close to the exact value!"),
                (0.01, 0.05): (30, "Great! Very accurate!"),
                (0.05, 0.1): (15, "Good! Close to the correct value!"),
                (0.1, 0.2): (10, "Not bad! You're getting closer!"),
                (0.2, float('inf')): (0, f"Too far off! The correct value is {self.current_answer:.2f}")
            }
            
            for (min_dev, max_dev), (points, message) in points_map.items():
                if min_dev <= deviation < max_dev:
                    if points > 0:
                        # Correct answer - successful attack
                        attack_messages = [
                            "⚡ Thunderbolt hits! Critical damage!",
                            "⚡ Electric attack successful! Enemy stunned!",
                            "⚡ Pikachu's attack lands perfectly!",
                            "⚡ Thunder Shock connects! Enemy weakened!"
                        ]
                        battle_message = random.choice(attack_messages)
                        self.battle_message.config(text=battle_message, fg="#006400")  # Dark green for success
                        
                        # Flash the enemy Pokémon red when hit
                        self.flash_enemy_red()
                        
                        self.handle_correct_answer(max(1, points // 5), message, deviation, points)
                    else:
                        # Wrong answer - attack misses and player gets hit
                        miss_messages = [
                            "💧 Squirtle dodged the attack!",
                            "💧 Enemy used Protect! Attack blocked!",
                            "💧 Attack missed! Enemy counterattacks!",
                            "💧 Squirtle's Water Gun deflects the attack!"
                        ]
                        battle_message = random.choice(miss_messages)
                        self.battle_message.config(text=battle_message, fg="#8B0000")  # Dark red for failure
                        
                        # Flash the player's Pokémon red when hit
                        self.flash_pokemon_red()
                        
                        self.handle_wrong_answer(message, f"Deviation: {deviation:.3f}")
                    break
                    
        except ValueError:
            self.show_message_with_timer_freeze("Error", "Please enter a valid number!", "error")
            self.answer_entry.delete(0, tk.END)

    def handle_correct_answer(self, coins_earned, message, deviation=None, points=None):
        """Handle correct answer logic"""
        self.score += points if points else 10
        self.streak += 1
        self.animate_score_label()
        self.add_gold_coins(coins_earned)
        
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
            self.add_gold_coins(bonus_coins)
            self.show_message_with_timer_freeze("Combo!", 
                f"🔥 Combo x{self.streak}! +{self.score} Bonus Points! +{bonus_coins} Gold Coins!")
        
        self.play_sound("correct")
        
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
        self.play_sound("incorrect")
        
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
            self.time_left = 15
            self.generate_square_root_question()
        elif self.game_mode == "integration":
            self.time_left = 20
            self.generate_integration_question()
        elif self.game_mode == "differentiation":
            self.time_left = 20
            self.generate_differentiation_question()
        elif self.game_mode == "pokemon_battle":
            self.time_left = 15
            self.generate_pokemon_question()
        else:
            self.time_left = 10
            self.generate_question()
        
        self.time_label.config(text=f"Time: {self.time_left}s")

    def end_game(self):
        """End the game and show results"""
        coins_earned = self.calculate_coins_earned_in_game()
        result = self.show_message_with_timer_freeze("Game Over", 
            f"You're out of lives!\n\nFinal Score: {self.score}\nGold Coins Earned: {coins_earned}\n\nWould you like to play again?", "yesno")
        self.update_leaderboard()
        if result:
            self.show_difficulty_selection()
        else:
            self.root.quit()



    def animate_score_label(self):
        """Animate score label when score increases"""
        original_color = self.score_label.cget("fg")
        self.score_label.config(fg="green")
        self.root.after(300, lambda: self.score_label.config(fg=original_color))

    def start_timer(self):
        """Start the game timer"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
        # Set appropriate time limit based on game mode
        if hasattr(self, 'game_mode'):
            if self.game_mode == "square_root":
                self.time_left = 15
            elif self.game_mode == "integration":
                self.time_left = 20
            elif self.game_mode == "differentiation":
                self.time_left = 20
            elif self.game_mode == "pokemon_battle":
                self.time_left = 15
            else:
                self.time_left = 10
        
        self.update_timer()

    def update_timer(self):
        """Update game timer"""
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"Time: {self.time_left}s")
            if self.time_left <= 3:
                self.animate_time_warning()
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.lives_system.reduce_player_lives(1)
            self.lives_label.config(text=self.lives_system.get_player_life_display())
            
            # Update enemy lives display for ALL game modes
            self.enemy_lives_label.config(text=self.lives_system.get_enemy_life_display())
            
            self.play_sound("incorrect")
            if self.lives_system.is_player_defeated():
                self.end_game()
            else:
                if self.game_mode == "square_root":
                    self.time_left = 15
                    self.generate_square_root_question()
                elif self.game_mode == "integration":
                    self.time_left = 20
                    self.generate_integration_question()
                elif self.game_mode == "differentiation":
                    self.time_left = 20
                    self.generate_differentiation_question()
                elif self.game_mode == "pokemon_battle":
                    self.time_left = 15
                    self.generate_pokemon_question()
                else:
                    self.time_left = 10
                    self.generate_question()
                self.update_timer()

    def animate_time_warning(self):
        """Animate time warning when timer is low"""
        self.time_label.config(fg="red")
        self.root.after(300, lambda: self.time_label.config(fg="black"))

    def play_sound(self, sound_type):
        """Play sound effects"""
        if SOUND_AVAILABLE:
            try:
                if sound_type == "correct":
                    winsound.Beep(1000, 200)
                elif sound_type == "incorrect":
                    winsound.Beep(500, 200)
            except:
                pass

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

    def add_gold_coins(self, amount):
        """Add gold coins to current player"""
        if hasattr(self, 'player_name') and self.player_name:
            if self.player_name not in self.player_gold_coins:
                self.player_gold_coins[self.player_name] = 0
            self.player_gold_coins[self.player_name] += amount
            self.save_player_gold_coins()

    def calculate_coins_earned_in_game(self):
        """Calculate gold coins earned during this game session"""
        if not hasattr(self, 'player_name') or not self.player_name:
            return 0
        
        if hasattr(self, 'game_mode'):
            if self.game_mode == "square_root":
                return max(1, self.score // 5)
            elif self.game_mode == "integration":
                return max(1, self.score // 15)
            elif self.game_mode == "pokemon_battle":
                return max(1, self.score // 8)
            else:
                correct_answers = self.score // 10
                combo_bonuses = (correct_answers // 3) * 5
                return (correct_answers * 2) + combo_bonuses
        else:
            correct_answers = self.score // 10
            combo_bonuses = (correct_answers // 3) * 5
            return (correct_answers * 2) + combo_bonuses

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

    def update_leaderboard(self):
        """Update leaderboard with current score"""
        self.leaderboard.append({
            "player_name": self.player_name,
            "score": self.score,
            "difficulty": self.difficulty,
            "timestamp": time.ctime()
        })
        self.leaderboard = sorted(self.leaderboard, key=lambda x: x["score"], reverse=True)[:5]
        try:
            with open("leaderboard.json", "w") as f:
                json.dump(self.leaderboard, f)
        except:
            messagebox.showerror("Error", "Failed to save leaderboard!")

    def show_leaderboard(self):
        """Show leaderboard page"""
        self.clear_window()
        self.root.configure(bg="#FCE4EC")  # Light pink background
        
        self.leaderboard = self.load_leaderboard()
        leaderboard_frame = self.create_centered_frame()

        tk.Label(leaderboard_frame, text="Leaderboard", font=self.title_font).grid(row=0, column=0, pady=20)
        
        for idx, entry in enumerate(self.leaderboard, 1):
            player_name = entry.get('player_name', 'Unknown Player')
            tk.Label(leaderboard_frame,
                     text=f"{idx}. {player_name} - Score: {entry['score']} ({entry['difficulty']}) - {entry['timestamp']}",
                     font=self.label_font).grid(row=idx, column=0, pady=2)

        buttons = [
            ("Delete All Records", "#ff4444", "white", self.confirm_delete_all),
            ("Back to Menu", self.button_color, "white", self.create_start_menu)
        ]
        
        for i, (text, bg, fg, command) in enumerate(buttons, len(self.leaderboard) + 1):
            tk.Button(leaderboard_frame, text=text, font=self.button_font, bg=bg,
                     fg=fg, command=command).grid(row=i, column=0, pady=10 if i == len(self.leaderboard) + 1 else 20)

    def show_store(self):
        """Show store page"""
        self.clear_window()
        self.root.configure(bg="#E0F2F1")  # Light cyan background
        
        store_frame = self.create_centered_frame()
        
        tk.Label(store_frame, text="🏪 Math Master Store", font=self.title_font).grid(row=0, column=0, pady=10)
        player_coins = self.get_player_gold_coins(self.player_name)
        tk.Label(store_frame, text=f"💰 Gold Coins: {player_coins}", 
                font=self.label_font, fg="#FFD700").grid(row=1, column=0, pady=5)
        
        for row, (item_name, item_data) in enumerate(self.store_items.items(), 2):
            item_frame = tk.Frame(store_frame)
            item_frame.grid(row=row, column=0, pady=5, sticky="ew")
            
            tk.Label(item_frame, text=f"�� {item_name}", font=self.button_font).grid(row=0, column=0, sticky="w")
            tk.Label(item_frame, text=f"💡 {item_data['description']}", font=self.label_font).grid(row=1, column=0, sticky="w")
            tk.Label(item_frame, text=f"💰 {item_data['price']} coins", font=self.label_font, fg="#FFD700").grid(row=2, column=0, sticky="w")
            
            tk.Button(item_frame, text="Buy", font=self.button_font, bg="#4CAF50", fg="white",
                     command=lambda name=item_name: self.buy_item(name)).grid(row=0, column=1, rowspan=3, padx=10)
        
        tk.Button(store_frame, text="Back", font=self.button_font, bg=self.button_color,
                  fg="white", command=self.show_difficulty_selection).grid(row=len(self.store_items)+2, column=0, pady=20)

    def buy_item(self, item_name):
        """Buy item from store"""
        if item_name in self.store_items:
            price = self.store_items[item_name]["price"]
            player_coins = self.get_player_gold_coins(self.player_name)
            if player_coins >= price:
                self.player_gold_coins[self.player_name] -= price
                self.save_player_gold_coins()
                messagebox.showinfo("Purchase Successful", f"You bought {item_name} for {price} coins!")
                self.show_store()
            else:
                messagebox.showerror("Insufficient Coins", f"You need {price} coins to buy {item_name}!")

    def confirm_exit(self):
        """Handle exit confirmation"""
        if hasattr(self, 'score') and self.score > 0:
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
            
            coins_earned = self.calculate_coins_earned_in_game()
            result = messagebox.askyesno("Exit Game", 
                                       f"Are you sure you want to exit?\n\nCurrent Score: {self.score}\nDifficulty: {self.difficulty.capitalize()}\nGold Coins Earned: {coins_earned}\n\nYour score will be saved before exiting.")
            if result:
                self.update_leaderboard()
                messagebox.showinfo("Score Saved", f"Your score of {self.score} has been saved to the leaderboard!\nGold Coins Earned: {coins_earned}")
                self.root.quit()
            else:
                self.start_timer()
        else:
            result = messagebox.askyesno("Exit Game", "Are you sure you want to exit?")
            if result:
                self.root.quit()

    def confirm_back_to_menu(self):
        """Handle back to menu confirmation"""
        if hasattr(self, 'score') and self.score > 0:
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
            
            coins_earned = self.calculate_coins_earned_in_game()
            result = messagebox.askyesno("Return to Menu", 
                                       f"Are you sure you want to return to the difficulty selection?\n\nCurrent Score: {self.score}\nDifficulty: {self.difficulty.capitalize()}\nGold Coins Earned: {coins_earned}\n\nYour score will be saved before returning.")
            if result:
                self.update_leaderboard()
                messagebox.showinfo("Score Saved", f"Your score of {self.score} has been saved to the leaderboard!\nGold Coins Earned: {coins_earned}")
                self.show_difficulty_selection()
            else:
                self.start_timer()
        else:
            self.show_difficulty_selection()

    def confirm_delete_all(self):
        """Handle delete all records confirmation"""
        if not self.leaderboard:
            messagebox.showinfo("No Records", "There are no records to delete.")
            return
        
        result = messagebox.askyesno("Delete All Records", 
                                   f"Are you sure you want to delete ALL {len(self.leaderboard)} records?\n\nThis action cannot be undone!")
        if result:
            self.leaderboard = []
            try:
                with open("leaderboard.json", "w") as f:
                    json.dump(self.leaderboard, f)
                messagebox.showinfo("Records Deleted", "All leaderboard records have been deleted successfully!")
                self.show_leaderboard()
            except:
                messagebox.showerror("Error", "Failed to delete records!")

    def quit_game(self):
        """Quit the game directly"""
        result = messagebox.askyesno("Exit Game", "Are you sure you want to exit?")
        if result:
            self.root.quit()

    def clear_window(self):
        """Clear all widgets from window"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_pokemon_battle_game(self):
        """Start Pokémon battle game with actual battle background"""
        self.reset_game_state()
        self.game_mode = "pokemon_battle"
        self.setup_pokemon_battle_ui()
        self.generate_pokemon_question()
        self.start_timer()

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

    def generate_pokemon_question(self):
        """Generate Pokémon-themed math question"""
        ranges = {
            "easy": (1, 10),
            "medium": (10, 50),
            "hard": (50, 100)
        }
        
        min_val, max_val = ranges[self.difficulty]
        num1, num2 = random.randint(min_val, max_val), random.randint(min_val, max_val)
        
        operations = ["+", "-", "*", "/"]
        op = random.choice(operations)
        
        # Pokémon-themed question templates
        question_templates = {
            "+": [
                f"Pikachu used {num1} Thunder Shocks and {num2} Quick Attacks. How many moves total?",
                f"Squirtle has {num1} HP and gains {num2} HP from a potion. What's the total HP?",
                f"Your team has {num1} Pokémon and you catch {num2} more. How many total?",
                f"Battle lasted {num1} minutes and {num2} more minutes. Total battle time?"
            ],
            "-": [
                f"Pikachu had {num1} HP but took {num2} damage. Remaining HP?",
                f"You had {num1} Poké Balls and used {num2}. How many left?",
                f"Route has {num1} trainers, you beat {num2}. How many remaining?",
                f"Pokémon has {num1} moves, {num2} are disabled. How many usable?"
            ],
            "*": [
                f"Pikachu's Thunderbolt does {num1} damage. {num2} Thunderbolts total damage?",
                f"Each Poké Ball costs {num1} coins. {num2} Poké Balls total cost?",
                f"Battle gives {num1} XP per win. {num2} wins total XP?",
                f"Pokémon learns {num1} moves per level. {num2} levels total moves?"
            ],
            "/": [
                f"Pikachu has {num1} HP and takes {num2} damage per hit. How many hits to defeat?",
                f"You have {num1} coins and each item costs {num2}. How many items can you buy?",
                f"Route has {num1} trainers and you have {num2} hours. How many trainers per hour?",
                f"Pokémon needs {num1} XP to evolve and gains {num2} XP per battle. How many battles?"
            ]
        }
        
        if op == "/":
            num1 = num2 * random.randint(1, 10)
            self.current_answer = num1 // num2
        elif op == "+":
            self.current_answer = num1 + num2
        elif op == "-":
            num1, num2 = max(num1, num2), min(num1, num2)
            self.current_answer = num1 - num2
        else:
            self.current_answer = num1 * num2
        
        # Select random question template
        template = random.choice(question_templates[op])
        self.question_label.config(text=template)
        self.battle_message.config(text="⚡ Pikachu is ready to battle! Answer correctly to attack!")
        self.answer_entry.delete(0, tk.END)

    def check_pokemon_answer(self, event=None):
        """Check Pokémon battle answer"""
        try:
            user_answer = float(self.answer_entry.get())
            if abs(user_answer - self.current_answer) < 0.01:
                # Correct answer - successful attack on enemy
                attack_messages = [
                    "⚡ Thunderbolt hits! Critical damage!",
                    "⚡ Electric attack successful! Enemy stunned!",
                    "⚡ Pikachu's attack lands perfectly!",
                    "⚡ Thunder Shock connects! Enemy weakened!"
                ]
                message = random.choice(attack_messages)
                self.battle_message.config(text=message, fg="#006400")  # Dark green for success
                
                # Flash the enemy Pokémon red when hit
                self.flash_enemy_red()
                
                # Use centralized handle_correct_answer function
                self.handle_correct_answer(3, "Correct!")
            else:
                # Wrong answer - attack misses and player gets hit
                miss_messages = [
                    "💧 Squirtle dodged the attack!",
                    "💧 Enemy used Protect! Attack blocked!",
                    "💧 Attack missed! Enemy counterattacks!",
                    "💧 Squirtle's Water Gun deflects the attack!"
                ]
                message = random.choice(miss_messages)
                self.battle_message.config(text=message, fg="#8B0000")  # Dark red for failure
                
                # Flash the player's Pokémon red when hit
                self.flash_pokemon_red()
                
                self.handle_wrong_answer("Attack missed!", f"Correct answer: {self.current_answer}")
        except ValueError:
            self.show_message_with_timer_freeze("Error", "Please enter a valid number!", "error")
            self.answer_entry.delete(0, tk.END)

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

    def flash_widget_red(self, widget):
        """Flash a specific widget red"""
        original_bg = widget.cget('bg')
        
        # Flash red
        widget.config(bg='red')
        
        # Return to original color after 300ms
        self.root.after(300, lambda: widget.config(bg=original_bg))

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

    def handle_enemy_defeated(self):
        """Handle when enemy is defeated"""
        enemy_name = self.get_enemy_name()
        victory_messages = [
            f"🎉 Victory! Enemy {enemy_name} fainted!",
            f"🏆 You defeated the {enemy_name} trainer!",
            "⚡ Pikachu wins the battle!",
            f"🎊 Battle won! {enemy_name} is defeated!"
        ]
        message = random.choice(victory_messages)
        self.battle_message.config(text=message, fg="#FFD700")  # Gold color for victory
        
        # Add bonus points for defeating enemy
        bonus_points = 50
        self.score += bonus_points
        
        # Show victory message
        result = self.show_message_with_timer_freeze("Victory!", 
            f"{message}\n\nBonus Points: +{bonus_points}\nFinal Score: {self.score}\n\nWould you like to battle another trainer?", "yesno")
        
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
            
            self.generate_pokemon_question()
        else:
            # End game and go back to menu
            self.end_game()

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


if __name__ == "__main__":
    root = tk.Tk()
    app = MathGame(root)
    root.mainloop()
