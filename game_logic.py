import random
import math
from tkinter import messagebox
from question import *

class GameLogic:
    """Handles all game logic including question generation and answer checking"""
    
    def __init__(self, dataMgr, utils):
        self.dataMgr = dataMgr
        self.utils = utils
        
    def generateAlgebraQuestion(self, difficulty):
        # generates algebra question based on difficulty level
        ranges = {}
        ranges["easy"] = (1, 10)
        ranges["medium"] = (10, 50)
        ranges["hard"] = (50, 100)
        
        difficulty_range = ranges[difficulty]
        minVal = difficulty_range[0]
        maxVal = difficulty_range[1]
        
        num1 = random.randint(minVal, maxVal)
        num2 = random.randint(minVal, maxVal)
        
        operations = []
        operations.append("+")
        operations.append("-")
        operations.append("*")
        operations.append("/")
        
        op = random.choice(operations)
        
        if op == "/":
            num1 = num2 * random.randint(1, 10)
            currentAnswer = num1 // num2
        elif op == "+":
            currentAnswer = num1 + num2
        elif op == "-":
            if num1 > num2:
                temp_num1 = num1
                temp_num2 = num2
            else:
                temp_num1 = num2
                temp_num2 = num1
            currentAnswer = temp_num1 - temp_num2
        else:
            currentAnswer = num1 * num2
        
        questionText = str(num1) + " " + op + " " + str(num2) + " = ?"
        return questionText, currentAnswer

    def generateSquareRootQuestion(self, difficulty):
        # generates square root question - these are tricky
        nonPerfectSquares = {}
        nonPerfectSquares["easy"] = [2, 3, 5, 6, 7, 8]
        nonPerfectSquares["medium"] = [10, 11, 12, 13, 14, 15, 17, 18, 19, 20]
        nonPerfectSquares["hard"] = [21, 22, 23, 24, 26, 27, 28, 29, 30]
        
        difficulty_numbers = nonPerfectSquares[difficulty]
        number = random.choice(difficulty_numbers)
        currentAnswer = math.sqrt(number)
        questionText = "√" + str(number) + " = ? (Round to 2 decimal places)"
        return questionText, currentAnswer

    def generateIntegrationQuestion(self, difficulty):
        # generates integration question based on difficulty
        # Select question set based on difficulty
        if difficulty == "easy":
            questionSet = integration_questions_simple
        elif difficulty == "medium":
            questionSet = integration_questions_medium
        elif difficulty == "hard":
            questionSet = integration_questions_hard
        else:
            # Default to simple if difficulty not set
            questionSet = integration_questions_simple
            
        return random.choice(questionSet)

    def generateDifferentiationQuestion(self, difficulty):
        # generates differentiation question based on difficulty
        # Select question set based on difficulty
        if difficulty == "easy":
            questionSet = differentiation_questions_easy
        elif difficulty == "medium":
            questionSet = differentiation_questions_medium
        elif difficulty == "hard":
            questionSet = differentiation_questions_hard
        else:
            # Default to easy if difficulty not set
            questionSet = differentiation_questions_easy
            
        return random.choice(questionSet)

    def checkAlgebraAnswer(self, userAnswer, correctAnswer):
        # checks algebra answer - pretty straightforward
        try:
            userFloat = float(userAnswer)
            difference = abs(userFloat - correctAnswer)
            if difference < 0.01:
                return True, "Correct!"
            else:
                return False, "Wrong! Correct answer: " + str(correctAnswer)
        except ValueError:
            return False, "Please enter a valid number!"

    def checkSquareRootAnswer(self, userAnswer, correctAnswer):
        # checks square root answer - this one's more complex with partial credit
        try:
            userFloat = float(userAnswer)
            deviation = abs(userFloat - correctAnswer)
            
            pointsMap = {}
            pointsMap[(0, 0.01)] = (50, "Excellent! Very close to the exact value!")
            pointsMap[(0.01, 0.05)] = (30, "Great! Very accurate!")
            pointsMap[(0.05, 0.1)] = (15, "Good! Close to the correct value!")
            pointsMap[(0.1, 0.2)] = (10, "Not bad! You're getting closer!")
            pointsMap[(0.2, float('inf'))] = (0, "Too far off! The correct value is " + str(round(correctAnswer, 2)))
            
            for range_tuple, result_tuple in pointsMap.items():
                minDev = range_tuple[0]
                maxDev = range_tuple[1]
                points = result_tuple[0]
                message = result_tuple[1]
                
                if minDev <= deviation and deviation < maxDev:
                    if points > 0:
                        return True, message, points, deviation
                    else:
                        return False, message, 0, deviation
            return False, "Invalid input!", 0, 0
                    
        except ValueError:
            return False, "Please enter a valid number!", 0, 0

    def checkIntegrationAnswer(self, selectedOption, question):
        # checks integration answer
        correctAnswer = question["answer"]
        if selectedOption == correctAnswer:
            return True, "Correct!"
        else:
            return False, "Incorrect! Correct answer: " + correctAnswer

    def checkDifferentiationAnswer(self, selectedOption, question):
        # checks differentiation answer
        correctAnswer = question["answer"]
        if selectedOption == correctAnswer:
            return True, "Correct!"
        else:
            return False, "Incorrect! Correct answer: " + correctAnswer

    def getBattleMessages(self, isCorrect):
        # gets battle messages for pokemon mode - adds some flavor
        if isCorrect:
            attackMessages = []
            attackMessages.append("⚡ Thunderbolt hits! Critical damage!")
            attackMessages.append("⚡ Electric attack successful! Enemy stunned!")
            attackMessages.append("⚡ Pikachu's attack lands perfectly!")
            attackMessages.append("⚡ Thunder Shock connects! Enemy weakened!")
        else:
            attackMessages = []
            attackMessages.append("💧 Squirtle dodged the attack!")
            attackMessages.append("💧 Enemy used Protect! Attack blocked!")
            attackMessages.append("💧 Attack missed! Enemy counterattacks!")
            attackMessages.append("💧 Squirtle's Water Gun deflects the attack!")
        
        return random.choice(attackMessages)

    def getVictoryMessages(self, enemyName):
        # gets victory messages for pokemon mode
        victoryMessages = []
        victoryMessages.append("🎉 Victory! Enemy " + enemyName + " fainted!")
        victoryMessages.append("🏆 You defeated the " + enemyName + " trainer!")
        victoryMessages.append("⚡ Pikachu wins the battle!")
        victoryMessages.append("🎊 Battle won! " + enemyName + " is defeated!")
        
        return random.choice(victoryMessages) 
