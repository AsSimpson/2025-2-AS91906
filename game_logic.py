import random
import math
from tkinter import messagebox
from question import *

class GameLogic:
    """Handles all game logic including question generation and answer checking"""
    
    def __init__(self, data_manager, utils):
        self.data_manager = data_manager
        self.utils = utils
        
    def generate_algebra_question(self, difficulty):
        """Generate algebra question based on difficulty"""
        ranges = {
            "easy": (1, 10),
            "medium": (10, 50),
            "hard": (50, 100)
        }
        
        min_val, max_val = ranges[difficulty]
        num1, num2 = random.randint(min_val, max_val), random.randint(min_val, max_val)
        
        operations = ["+", "-", "*", "/"]
        op = random.choice(operations)
        
        if op == "/":
            num1 = num2 * random.randint(1, 10)
            current_answer = num1 // num2
        elif op == "+":
            current_answer = num1 + num2
        elif op == "-":
            num1, num2 = max(num1, num2), min(num1, num2)
            current_answer = num1 - num2
        else:
            current_answer = num1 * num2
        
        question_text = f"{num1} {op} {num2} = ?"
        return question_text, current_answer

    def generate_square_root_question(self, difficulty):
        """Generate square root question"""
        non_perfect_squares = {
            "easy": [2, 3, 5, 6, 7, 8],
            "medium": [10, 11, 12, 13, 14, 15, 17, 18, 19, 20],
            "hard": [21, 22, 23, 24, 26, 27, 28, 29, 30]
        }
        
        number = random.choice(non_perfect_squares[difficulty])
        current_answer = math.sqrt(number)
        question_text = f"√{number} = ? (Round to 2 decimal places)"
        return question_text, current_answer

    def generate_integration_question(self, difficulty):
        """Generate integration question based on difficulty"""
        # Select question set based on difficulty
        if difficulty == "easy":
            question_set = integration_questions_simple
        elif difficulty == "medium":
            question_set = integration_questions_medium
        elif difficulty == "hard":
            question_set = integration_questions_hard
        else:
            # Default to simple if difficulty not set
            question_set = integration_questions_simple
            
        return random.choice(question_set)

    def generate_differentiation_question(self, difficulty):
        """Generate differentiation question based on difficulty"""
        # Select question set based on difficulty
        if difficulty == "easy":
            question_set = differentiation_questions_easy
        elif difficulty == "medium":
            question_set = differentiation_questions_medium
        elif difficulty == "hard":
            question_set = differentiation_questions_hard
        else:
            # Default to easy if difficulty not set
            question_set = differentiation_questions_easy
            
        return random.choice(question_set)

    def generate_pokemon_question(self, difficulty):
        """Generate Pokémon-themed math question"""
        ranges = {
            "easy": (1, 10),
            "medium": (10, 50),
            "hard": (50, 100)
        }
        
        min_val, max_val = ranges[difficulty]
        num1, num2 = random.randint(min_val, max_val), random.randint(min_val, max_val)
        
        operations = ["+", "-", "*", "/"]
        op = random.choice(operations)
        
        # Pokémon-themed question templates (clearer version)
        question_templates = {
            "+": [
                f"Pikachu used {num1} Thunder Shocks and {num2} Quick Attacks. How many moves did it use in total?",
                f"Squirtle has {num1} HP and gains {num2} HP from a potion. What is its new total HP?",
                f"Your team started with {num1} Pokémon and you caught {num2} more. How many Pokémon are on your team now?",
                f"The battle lasted {num1} minutes, then continued for another {num2} minutes. What was the total battle time?"
            ],
            "-": [
                f"Pikachu had {num1} HP but took {num2} damage. How much HP does it have left?",
                f"You had {num1} Poké Balls and used {num2} of them. How many do you have remaining?",
                f"There were {num1} trainers on the route. You defeated {num2} of them. How many are left?",
                f"A Pokémon had {num1} moves, but {num2} of them are currently disabled. How many moves can it still use?"
            ],
            "*": [
                f"Pikachu's Thunderbolt deals {num1} damage. If it uses the move {num2} times, what is the total damage dealt?",
                f"Each Poké Ball costs {num1} coins. How much do {num2} Poké Balls cost in total?",
                f"Each battle win gives you {num1} XP. If you win {num2} times, how much XP will you earn in total?",
                f"A Pokémon learns {num1} new moves per level. After gaining {num2} levels, how many new moves will it have learned?"
            ],
            "/": [
                f"Pikachu has {num1} HP and takes {num2} damage with each hit. How many hits will it take to knock it out?",
                f"You have {num1} coins, and each item costs {num2} coins. How many items can you afford to buy?",
                f"There are {num1} trainers on the route, and you have {num2} hours to battle. How many trainers can you battle per hour?",
                f"A Pokémon needs {num1} XP to evolve and earns {num2} XP per battle. How many battles does it need to evolve?"
            ]
        }
                
        if op == "/":
            num1 = num2 * random.randint(1, 10)
            current_answer = num1 // num2
        elif op == "+":
            current_answer = num1 + num2
        elif op == "-":
            num1, num2 = max(num1, num2), min(num1, num2)
            current_answer = num1 - num2
        else:
            current_answer = num1 * num2
        
        # Select random question template
        template = random.choice(question_templates[op])
        return template, current_answer

    def check_algebra_answer(self, user_answer, correct_answer):
        """Check algebra answer"""
        try:
            user_float = float(user_answer)
            if abs(user_float - correct_answer) < 0.01:
                return True, "Correct!"
            else:
                return False, f"Wrong! Correct answer: {correct_answer}"
        except ValueError:
            return False, "Please enter a valid number!"

    def check_square_root_answer(self, user_answer, correct_answer):
        """Check square root answer"""
        try:
            user_float = float(user_answer)
            deviation = abs(user_float - correct_answer)
            
            points_map = {
                (0, 0.01): (50, "Excellent! Very close to the exact value!"),
                (0.01, 0.05): (30, "Great! Very accurate!"),
                (0.05, 0.1): (15, "Good! Close to the correct value!"),
                (0.1, 0.2): (10, "Not bad! You're getting closer!"),
                (0.2, float('inf')): (0, f"Too far off! The correct value is {correct_answer:.2f}")
            }
            
            for (min_dev, max_dev), (points, message) in points_map.items():
                if min_dev <= deviation < max_dev:
                    if points > 0:
                        return True, message, points, deviation
                    else:
                        return False, message, 0, deviation
            return False, "Invalid input!", 0, 0
                    
        except ValueError:
            return False, "Please enter a valid number!", 0, 0

    def check_integration_answer(self, selected_option, question):
        """Check integration answer"""
        correct_answer = question["answer"]
        if selected_option == correct_answer:
            return True, "Correct!"
        else:
            return False, f"Incorrect! Correct answer: {correct_answer}"

    def check_differentiation_answer(self, selected_option, question):
        """Check differentiation answer"""
        correct_answer = question["answer"]
        if selected_option == correct_answer:
            return True, "Correct!"
        else:
            return False, f"Incorrect! Correct answer: {correct_answer}"

    def check_pokemon_answer(self, user_answer, correct_answer):
        """Check Pokémon battle answer"""
        try:
            user_float = float(user_answer)
            if abs(user_float - correct_answer) < 0.01:
                return True, "Correct!"
            else:
                return False, f"Attack missed! Correct answer: {correct_answer}"
        except ValueError:
            return False, "Please enter a valid number!"

    def get_battle_messages(self, is_correct):
        """Get battle messages for Pokémon mode"""
        if is_correct:
            attack_messages = [
                "⚡ Thunderbolt hits! Critical damage!",
                "⚡ Electric attack successful! Enemy stunned!",
                "⚡ Pikachu's attack lands perfectly!",
                "⚡ Thunder Shock connects! Enemy weakened!"
            ]
        else:
            attack_messages = [
                "💧 Squirtle dodged the attack!",
                "💧 Enemy used Protect! Attack blocked!",
                "💧 Attack missed! Enemy counterattacks!",
                "💧 Squirtle's Water Gun deflects the attack!"
            ]
        return random.choice(attack_messages)

    def get_victory_messages(self, enemy_name):
        """Get victory messages for Pokémon mode"""
        victory_messages = [
            f"🎉 Victory! Enemy {enemy_name} fainted!",
            f"🏆 You defeated the {enemy_name} trainer!",
            "⚡ Pikachu wins the battle!",
            f"🎊 Battle won! {enemy_name} is defeated!"
        ]
        return random.choice(victory_messages) 