import tkinter as tk
from tkinter import messagebox
import random
import time
import math
from PIL import Image, ImageTk
from question import *

from game_core import LivesSystem, GameConfig, DIFFICULTY_LEVELS, DIFFICULTY_COLORS, GAME_MODES
from data_manager import DataManager
from game_logic import GameLogic
import utils

class MathGame:
    def __init__(self, root):
        self.root = root
        self.setupWindow()
        self.initVars()
        self.loadData()
        self.setupStyles()
        self.createStartMenu()

    def setupWindow(self):
        """Initialize the main window"""
        # sets up the main window - basic stuff
        self.root.title("Pokémath Adventures")
        self.root.geometry("1152x768")  # Scaled down 3:2 ratio (75% of original)
        
        # Load pre-resized background image for better performance
        try:
            self.bgImg = Image.open("assets/pokemon_pixle_bg_resized.png")
            self.bgPhoto = ImageTk.PhotoImage(self.bgImg)
        except:
            print("Background image not found, using default background")
            self.bgPhoto = None

    def initVars(self):
        """Initialize game variables"""
        # initializes game variables - sets up the basic stuff
        self.score = 0
        self.streak = 0
        self.livesSys = LivesSystem(playerMaxLives=3, enemyMaxLives=5)  # Initialize lives system
        self.gameConfig = GameConfig()  # Initialize game configuration
        self.timeLeft = 10
        self.difficulty = "easy"
        self.currentAnswer = 0
        self.timerId = None
        self.playerName = ""
        self.timerFrozen = False
        self.frozenTimeLeft = 0

    def loadData(self):
        """Load game data from files"""
        # loads game data from files
        self.dataMgr = DataManager()
        self.gameLogic = GameLogic(self.dataMgr, utils)

    def setupStyles(self):
        """Setup fonts and colors for consistent UI"""
        # sets up fonts and colors for consistent UI
        # Load Orbitron font
        self.loadOrbitronFont()
        
        self.bgColor = "#F4F4F4"
        self.btnColor = "#4CAF50"
        self.root.configure(bg=self.bgColor)

    def loadOrbitronFont(self):
        """Load Orbitron font with fallback options"""
        # loads orbitron font with fallback options - this part feels weird... double check
        try:
            import os
            import platform
            
            # Check if Orbitron font is available - try multiple paths
            fontPaths = []
            fontPaths.append("assets/fonts/Orbitron-VariableFont_wght.ttf")
            fontPaths.append("../assets/fonts/Orbitron-VariableFont_wght.ttf")
            fontPaths.append("Orbitron-VariableFont_wght.ttf")
            
            fontFound = False
            for fontPath in fontPaths:
                if os.path.exists(fontPath):
                    print("✅ Font file found at: " + fontPath)
                    fontFound = True
                    break
            
            if fontFound:
                # Try to use Orbitron font
                self.titleFont = ("Orbitron", 20, "bold")
                self.buttonFont = ("Orbitron", 12)
                self.labelFont = ("Orbitron", 14)
                print("✅ Orbitron font loaded successfully!")
                return
            else:
                print("⚠️ Font file not found in any expected location")
                
        except Exception as e:
            print("❌ Error loading Orbitron font: " + str(e))
        
        # Fallback to system fonts
        if platform.system() == "Windows":
            self.titleFont = ("Segoe UI", 20, "bold")
            self.buttonFont = ("Segoe UI", 12)
            self.labelFont = ("Segoe UI", 14)
        else:
            self.titleFont = ("Arial", 20, "bold")
            self.buttonFont = ("Arial", 12)
            self.labelFont = ("Arial", 14)
        
        print("⚠️ Using fallback fonts")

    def drawBackground(self):
        """Draw background image on window"""
        # draws background image on window
        if self.bgPhoto:
            self.bgLabel = tk.Label(self.root, image=self.bgPhoto)
            self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.root.configure(bg="#87CEEB")  # Sky blue fallback

    def createCenteredFrame(self):
        """Create a centered frame for content"""
        # creates a centered frame for content
        frame = tk.Frame(self.root, bg="#0C1A31")
        frame.place(relx=0.5, rely=0.4, anchor="center")
        return frame

    def clearWindow(self):
        """Clear all widgets from window"""
        # clears all widgets from window
        if self.timerId:
            self.root.after_cancel(self.timerId)
            self.timerId = None
        
        for widget in self.root.winfo_children():
            widget.destroy()

    def createStartMenu(self):
        """Create the main menu"""
        # creates the main menu - pretty straightforward
        self.clearWindow()
        self.drawBackground()
        
        
        startFrame = self.createCenteredFrame()
        
        titleLabel = tk.Label(startFrame, text="Pokémath Adventures", font=self.titleFont, bg="#0C1A31", fg="white")
        titleLabel.grid(row=0, column=0, pady=20)
        
        buttons = []
        buttons.append(("START GAME", "#4CAF50", "white", self.showUsernameAndDifficultyPage))
        buttons.append(("View Leaderboard", self.btnColor, "white", self.showLeaderboard))
        buttons.append(("Exit", "#f44336", "white", self.quitGame))
        
        for i in range(len(buttons)):
            button_info = buttons[i]
            text = button_info[0]
            bg = button_info[1]
            fg = button_info[2]
            command = button_info[3]
            
            button = tk.Button(startFrame, text=text, font=self.buttonFont, bg=bg,
                     fg=fg, command=command, width=15, height=2)
            button.grid(row=i+1, column=0, pady=10)

    def showUsernameAndDifficultyPage(self):
        """Show combined username input and difficulty selection page"""
        # shows combined username input and difficulty selection page - kinda messy but works
        self.clearWindow()
        self.root.configure(bg="#0C1A31")  # Shadow Color (Dark Teal) - background

        combinedFrame = tk.Frame(self.root)  # Secondary Color (Pale Yellow) - main frame
        combinedFrame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Header with Charizard-inspired styling
        headerFrame = tk.Frame(combinedFrame, bg="#FF6D28", relief="raised", bd=3)  # Primary Color (Fiery Orange)
        headerFrame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        titleLabel = tk.Label(headerFrame, text="Welcome to Pokémath Adventures!",
                font=self.titleFont, bg="#FF6D28", fg="#4E342E")
        titleLabel.grid(row=0, column=0, pady=10)
        
        # Username input section
        usernameFrame = tk.Frame(combinedFrame)
        usernameFrame.grid(row=1, column=0, pady=10, padx=10)
        
        usernamePromptLabel = tk.Label(usernameFrame, text="Enter Your Name:",
                font=self.labelFont, fg="#4E342E")
        usernamePromptLabel.grid(row=0, column=0, pady=10)
        
        self.usernameEntry = tk.Entry(usernameFrame, font=self.labelFont, width=20, 
                                     fg="#4E342E", relief="raised", bd=2)
        self.usernameEntry.grid(row=1, column=0, pady=10)
        self.usernameEntry.focus()
        self.usernameEntry.bind("<Return>", self.confirmUsername)
        
        # Confirm username button
        self.confirmButton = tk.Button(usernameFrame, text="Confirm Name", font=self.buttonFont,
                                 bg="#4CAF50", fg="white", relief="raised", bd=4,
                                 command=self.confirmUsername, width=15, height=2)
        self.confirmButton.grid(row=2, column=0, pady=10)
        
        # Edit name button (initially hidden)
        self.editButton = tk.Button(usernameFrame, text="Edit Name", font=self.buttonFont,
                               bg="#FF6D28", fg="white", relief="raised", bd=4,
                               command=self.editUsername, width=15, height=2)
        self.editButton.grid(row=2, column=0, pady=10)
        self.editButton.grid_remove()  # Initially hidden
        
        # Username confirmation status
        self.usernameStatusLabel = tk.Label(usernameFrame, text="", font=self.labelFont,
                                            fg="#4E342E")
        self.usernameStatusLabel.grid(row=3, column=0, pady=5)
        
        # Check if username was previously confirmed and restore state
        if hasattr(self, 'playerName') and len(self.playerName) > 0:
            # Restore the confirmed username state but allow editing
            self.usernameEntry.insert(0, self.playerName)
            status_text = "✓ Name confirmed: " + self.playerName
            self.usernameStatusLabel.config(text=status_text, fg="#4CAF50")
            self.confirmButton.config(text="✓ Confirmed", bg="#4CAF50", fg="white", state="disabled")
            self.confirmButton.grid_remove()  # Hide confirm button
            self.editButton.grid()  # Show edit button
        else:
            # Clear any previous state
            self.playerName = ""
        
        # Difficulty selection section (initially disabled)
        difficultyFrame = tk.Frame(combinedFrame)
        difficultyFrame.grid(row=2, column=0, pady=10, padx=10)

        difficultyPromptLabel = tk.Label(difficultyFrame, text="Select Difficulty:",
                font=self.labelFont, fg="#4E342E")
        difficultyPromptLabel.grid(row=0, column=0, pady=10)

        # Difficulty buttons with Charizard color scheme (initially disabled)
        self.difficultyVar = tk.StringVar(value="none")
        difficultyButtonsFrame = tk.Frame(difficultyFrame)
        difficultyButtonsFrame.grid(row=1, column=0, pady=10)
        
        self.difficultyButtons = []
        for i in range(len(DIFFICULTY_LEVELS)):
            difficulty = DIFFICULTY_LEVELS[i]
            # Set different text colors based on difficulty
            if difficulty == "easy":
                textColor = "#264653"  # Shadow Color for easy
                buttonBg = "#FFE156"   # Secondary Color for easy
            elif difficulty == "hard":
                textColor = "#4E342E"  # Outline Color for hard
                buttonBg = "#FF6D28"   # Primary Color for hard
            else:
                textColor = "#4E342E"  # Outline Color for medium
                buttonBg = "#0077B6"   # Accent Color for medium
            
            btn = tk.Button(difficultyButtonsFrame, text=difficulty.capitalize(), 
                           font=self.titleFont, bg=buttonBg, fg=textColor,
                           width=15, height=2, relief="raised", bd=4,
                           command=lambda d=difficulty: self.selectDifficultyCombined(d))
            btn.grid(row=0, column=i, padx=5)
            self.difficultyButtons.append(btn)
        
        # Action buttons with Charizard styling
        actionButtonsFrame = tk.Frame(combinedFrame)
        actionButtonsFrame.grid(row=3, column=0, pady=10, padx=10)
        
        actionButtons = []
        actionButtons.append(("Start Game", "#4CAF50", "#FFE156", self.validateUsernameAndDifficulty))  # Green for start
        actionButtons.append(("Back", "#264653", "#FFE156", self.createStartMenu))  # Shadow Color
        actionButtons.append(("Return to Start", "#f44336", "#FFE156", self.createStartMenu))  # Red color
        
        for i in range(len(actionButtons)):
            button_info = actionButtons[i]
            text = button_info[0]
            bg = button_info[1]
            fg = button_info[2]
            command = button_info[3]
            
            # All buttons have the same size and border width
            button = tk.Button(actionButtonsFrame, text=text, font=self.buttonFont,
                     width=15, height=2, bg=bg, fg=fg, relief="raised", bd=4,
                     command=command)
            button.grid(row=0, column=i, padx=5)


    def confirmUsername(self, event=None):
        """Confirm username and enable difficulty selection"""
        # confirms username and enables difficulty selection
        username = self.usernameEntry.get().strip()
        is_valid, error_message = utils.validateUsername(username)
        
        if not is_valid:
            self.usernameStatusLabel.config(text=error_message, fg="#f44336")  # Red for error
            return
        
        # Username is valid, store it
        self.playerName = username
        status_text = "✓ Name confirmed: " + username
        self.usernameStatusLabel.config(text=status_text, fg="#4CAF50")  # Green for success
        
        # Change confirm button to show it's been confirmed
        for widget in self.root.winfo_children():
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if hasattr(child, 'winfo_children'):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Frame) and grandchild.cget('bg') == '#FFE156':
                                for great_grandchild in grandchild.winfo_children():
                                    if isinstance(great_grandchild, tk.Frame):
                                        for button in great_grandchild.winfo_children():
                                            if isinstance(button, tk.Button) and button.cget('text') == "Confirm Name":
                                                button.config(text="✓ Confirmed", bg="#4CAF50", fg="white", state="disabled")
        
        # Also update the entry field to show the confirmed name
        self.usernameEntry.delete(0, tk.END)
        self.usernameEntry.insert(0, username)
        
        # Switch to edit mode
        self.confirmButton.grid_remove()  # Hide confirm button
        self.editButton.grid()  # Show edit button

    def editUsername(self):
        """Allow editing of username"""
        # allows editing of username
        # Clear the current username state
        self.playerName = ""
        
        # Enable the entry field for editing
        self.usernameEntry.config(state="normal")
        self.usernameEntry.focus()
        
        # Clear the status label
        self.usernameStatusLabel.config(text="", fg="#4E342E")
        
        # Switch back to confirm mode
        self.confirmButton.config(text="Confirm Name", bg="#4CAF50", fg="white", state="normal")
        self.confirmButton.grid()  # Show confirm button
        self.editButton.grid_remove()  # Hide edit button

    def selectDifficultyCombined(self, difficultyLevel):
        """Select difficulty in the combined page"""
        # selects difficulty in the combined page
        # Check if username has been confirmed first
        if not hasattr(self, 'playerName') or len(self.playerName) == 0:
            messagebox.showwarning("Name Not Confirmed", 
                "Please enter and confirm your name before selecting difficulty!\n\n"
                "Step 1: Enter your name\n"
                "Step 2: Click 'Confirm Name' button\n"
                "Step 3: Select difficulty level")
            return
        
        self.difficulty = difficultyLevel
        self.difficultyVar.set(difficultyLevel)
        
        # Visual feedback - highlight selected difficulty
        for btn in self.difficultyButtons:
            if btn.cget('text').lower() == difficultyLevel:
                btn.config(bg="#E0E0E0", fg="black")  # Highlight selected
            else:
                # Reset other buttons to their original colors
                if btn.cget('text').lower() == "easy":
                    btn.config(bg="#FF6D28", fg="white")
                elif btn.cget('text').lower() == "hard":
                    btn.config(bg="#FF6D28", fg="#4E342E")
                else:
                    btn.config(bg="#0077B6", fg="#4E342E")

    def validateUsernameAndDifficulty(self, event=None):
        """Validate both username and difficulty selection"""
        # validates both username and difficulty selection
        # Check if username has been confirmed
        if not hasattr(self, 'playerName') or len(self.playerName) == 0:
            messagebox.showwarning("Name Not Confirmed", "Please enter and confirm your name first!")
            return
        
        # Check if difficulty has been selected
        if len(self.difficulty) == 0 or self.difficulty not in DIFFICULTY_LEVELS:
            messagebox.showwarning("Difficulty Required", "Please select a difficulty level!")
            return
        
        # Both username and difficulty are valid, proceed to game
        self.showDifficultyTests()

    def showDifficultySelection(self):
        """Show difficulty selection page"""
        # shows difficulty selection page - maybe not needed anymore
        self.clearWindow()
        self.root.configure(bg="#264653")  # Shadow Color (Dark Teal) - background

        difficultyFrame = tk.Frame(self.root)  # Secondary Color (Pale Yellow) - main frame
        difficultyFrame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Header with Charizard-inspired styling
        headerFrame = tk.Frame(difficultyFrame, bg="#FF6D28", relief="raised", bd=3)  # Primary Color (Fiery Orange)
        headerFrame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        welcome_text = "Welcome, " + self.playerName + "!"
        welcomeLabel = tk.Label(headerFrame, text=welcome_text,
                font=self.titleFont, bg="#FF6D28", fg="#4E342E")
        welcomeLabel.grid(row=0, column=0, pady=10)
        

        
        # Difficulty selection section
        selectionFrame = tk.Frame(difficultyFrame, bg="#FFE156")
        selectionFrame.grid(row=1, column=0, pady=10, padx=10)
        
        difficultyPromptLabel = tk.Label(selectionFrame, text="Select Difficulty:",
                font=self.labelFont, bg="#FFE156", fg="#4E342E")
        difficultyPromptLabel.grid(row=0, column=0, pady=10)

        # Difficulty buttons with Charizard color scheme
        self.difficultyVar = tk.StringVar(value="none")
        difficultyButtonsFrame = tk.Frame(selectionFrame, bg="#FFE156")
        difficultyButtonsFrame.grid(row=1, column=0, pady=10)
        
        for i in range(len(DIFFICULTY_LEVELS)):
            difficulty = DIFFICULTY_LEVELS[i]
            # Set different text colors based on difficulty
            if difficulty == "easy":
                textColor = "#264653"  # Shadow Color for easy
                buttonBg = "#FFE156"   # Secondary Color for easy
            elif difficulty == "hard":
                textColor = "#4E342E"  # Outline Color for hard
                buttonBg = "#FF6D28"   # Primary Color for hard
            else:
                textColor = "#4E342E"  # Outline Color for medium
                buttonBg = "#0077B6"   # Accent Color for medium
            
            button = tk.Button(difficultyButtonsFrame, text=difficulty.capitalize(), 
                     font=self.titleFont, bg=buttonBg, fg=textColor,
                     width=15, height=2, relief="raised", bd=2,
                     command=lambda d=difficulty: self.selectDifficulty(d))
            button.grid(row=0, column=i, padx=5)
        
        # Action buttons with Charizard styling
        actionButtonsFrame = tk.Frame(difficultyFrame)
        actionButtonsFrame.grid(row=2, column=0, pady=10, padx=10)
        
        actionButtons = []
        actionButtons.append(("Back", "#264653", "#FFE156", self.showUsernameAndDifficultyPage))  # Shadow Color
        actionButtons.append(("Return to Start", "#f44336", "#FFE156", self.createStartMenu))  # Red color
        
        for i in range(len(actionButtons)):
            button_info = actionButtons[i]
            text = button_info[0]
            bg = button_info[1]
            fg = button_info[2]
            command = button_info[3]
            
            # Skip size standardization for "Back" and "Return to Start" buttons
            if text in ["Back", "Return to Start"]:
                button = tk.Button(actionButtonsFrame, text=text, font=self.buttonFont,
                         width=12, bg=bg, fg=fg, relief="raised", bd=2,
                         command=command)
                button.grid(row=0, column=i, padx=5)
            else:
                button = tk.Button(actionButtonsFrame, text=text, font=self.buttonFont,
                         width=15, height=2, bg=bg, fg=fg, relief="raised", bd=2,
                         command=command)
                button.grid(row=0, column=i, padx=5)

    def selectDifficulty(self, difficultyLevel):
        """Select difficulty and go to test selection"""
        # selects difficulty and goes to test selection
        self.difficulty = difficultyLevel
        self.difficultyVar.set(difficultyLevel)
        self.showDifficultyTests()

    def showDifficultyTests(self):
        """Validate difficulty and show test selection"""
        # validates difficulty and shows test selection
        if len(self.difficulty) == 0 or self.difficulty not in DIFFICULTY_LEVELS:
            messagebox.showwarning("Difficulty Required", "Please select a difficulty level first!")
            return
        
        self.showTestWindow()

    def showTestWindow(self):
        """Show test selection window"""
        # shows test selection window - this is where the fun begins
        self.clearWindow()
        self.root.configure(bg="#264653")  # Shadow Color (Dark Teal) - background
        
        testFrame = tk.Frame(self.root)  # Secondary Color (Pale Yellow) - main frame
        testFrame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Header with Charizard-inspired styling
        headerFrame = tk.Frame(testFrame, bg="#FF6D28", relief="raised", bd=3)  # Primary Color (Fiery Orange)
        headerFrame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        
        difficultyDisplay = self.difficulty.capitalize()
        difficulty_text = difficultyDisplay + " Difficulty Tests"
        difficultyLabel = tk.Label(headerFrame, text=difficulty_text, 
                font=self.titleFont, bg="#FF6D28", fg="#4E342E")
        difficultyLabel.grid(row=0, column=0, pady=10)
        
        player_text = "Player: " + self.playerName
        playerLabel = tk.Label(headerFrame, text=player_text, 
                font=self.labelFont, bg="#FF6D28", fg="#4E342E")
        playerLabel.grid(row=1, column=0, pady=5)
        
        # Test selection section
        selectionFrame = tk.Frame(testFrame)
        selectionFrame.grid(row=1, column=0, pady=10, padx=10)
        
        testPromptLabel = tk.Label(selectionFrame, text="Select Test Type:", 
                font=self.labelFont, fg="#4E342E")
        testPromptLabel.grid(row=0, column=0, pady=10)
        
        # Test buttons with Charizard color scheme
        testButtonsFrame = tk.Frame(selectionFrame)
        testButtonsFrame.grid(row=1, column=0, pady=10)
        
        # Add extra space to match combined_frame size
        extraSpaceFrame = tk.Frame(testFrame)
        extraSpaceFrame.grid(row=2, column=0, pady=20)
        
        # Action buttons section to match combined_frame structure
        actionButtonsFrame = tk.Frame(testFrame)
        actionButtonsFrame.grid(row=3, column=0, pady=10, padx=10)
        
        # Test buttons (only the game type buttons)
        testButtons = []
        testButtons.append(("Arithmetics", "#0077B6", "#FFE156", self.startGame))  # Accent Color
        testButtons.append(("Square Root Challenge", "#0077B6", "#FFE156", self.startSquareRootGame))  # Accent Color
        testButtons.append(("Integration", "#0077B6", "#FFE156", self.startIntegrationGame))  # Accent Color
        testButtons.append(("Differentiation", "#0077B6", "#FFE156", self.startDifferentiationGame))  # Accent Color
        
        # Arrange test buttons in a 2x2 grid with larger size and more separation
        for i in range(len(testButtons)):
            button_info = testButtons[i]
            text = button_info[0]
            bg = button_info[1]
            fg = button_info[2]
            command = button_info[3]
            
            row = i // 2  # 2 buttons per row
            col = i % 2   # Column within the row
            button = tk.Button(testButtonsFrame, text=text, font=self.buttonFont, bg=bg,
                     fg=fg, command=command, width=20, height=3, relief="raised", bd=3)
            button.grid(row=row, column=col, padx=15, pady=15)
        
        # Action buttons (Back and Return to Start) - matching combined_frame structure
        actionButtons = []
        actionButtons.append(("Back", "#264653", "#FFE156", self.showUsernameAndDifficultyPage))  # Shadow Color
        actionButtons.append(("Return to Start", "#f44336", "#FFE156", self.createStartMenu))  # Red color
        
        for i in range(len(actionButtons)):
            button_info = actionButtons[i]
            text = button_info[0]
            bg = button_info[1]
            fg = button_info[2]
            command = button_info[3]
            
            button = tk.Button(actionButtonsFrame, text=text, font=self.buttonFont,
                     width=15, height=2, bg=bg, fg=fg, relief="raised", bd=2,
                     command=command)
            button.grid(row=0, column=i, padx=5)

    def quitGame(self):
        """Quit the game directly"""
        # quits the game directly
        result = messagebox.askyesno("Exit Game", "Are you sure you want to exit?")
        if result:
            self.root.quit()

    def resetGameState(self):
        """Reset game state for new game"""
        # resets game state for new game
        self.score = 0
        self.streak = 0
        self.livesSys.resetAllLives()  # Reset both player and enemy lives

    def startGame(self):
        """Start algebra game with Pokémon battle GUI"""
        # starts algebra game with pokemon battle GUI
        self.resetGameState()
        self.gameMode = "algebra"
        self.setupPokemonBattleUi()
        self.generateQuestion()
        self.startTimer()

    def startSquareRootGame(self):
        """Start square root game with Pokémon battle GUI"""
        # starts square root game with pokemon battle GUI
        self.resetGameState()
        self.gameMode = "square_root"
        self.setupPokemonBattleUi()
        self.generateSquareRootQuestion()
        self.startTimer()

    def startIntegrationGame(self):
        """Start integration game with Pokémon battle GUI"""
        # starts integration game with pokemon battle GUI
        self.resetGameState()
        self.gameMode = "integration"
        self.setupPokemonBattleUi()
        self.generateIntegrationQuestion()
        self.startTimer()

    def startDifferentiationGame(self):
        """Start differentiation game with Pokémon battle GUI"""
        # starts differentiation game with pokemon battle GUI
        self.resetGameState()
        self.gameMode = "differentiation"
        self.setupPokemonBattleUi()
        self.generateDifferentiationQuestion()
        self.startTimer()



    def generateQuestion(self):
        """Generate algebra question based on difficulty"""
        # generates algebra question based on difficulty
        questionText, self.currentAnswer = self.gameLogic.generateAlgebraQuestion(self.difficulty)
        self.questionLabel.config(text=questionText)
        self.battleMessage.config(text="⚡ Pikachu is ready to battle! Answer correctly to attack!")
        self.answerEntry.delete(0, tk.END)

    def generateSquareRootQuestion(self):
        """Generate square root question"""
        # generates square root question
        questionText, self.currentAnswer = self.gameLogic.generateSquareRootQuestion(self.difficulty)
        self.questionLabel.config(text=questionText)
        self.battleMessage.config(text="⚡ Pikachu is ready to battle! Answer correctly to attack!")
        self.answerEntry.delete(0, tk.END)

    def generateIntegrationQuestion(self):
        """Generate integration question based on difficulty"""
        # generates integration question based on difficulty
        self.currentQuestion = self.gameLogic.generateIntegrationQuestion(self.difficulty)
        self.questionLabel.config(text=self.currentQuestion["question"])
        self.battleMessage.config(text="⚡ Pikachu is ready to battle! Choose the correct answer to attack!")
        
        # Clear previous options
        for widget in self.optionsFrame.winfo_children():
            widget.destroy()
        
        # Create option buttons
        for option, text in self.currentQuestion["options"].items():
            button_text = option + ". " + text
            btn = tk.Button(self.optionsFrame, text=button_text, 
                           font=("Comic Sans MS", 10), bg="#0077B6", fg="#FFE156",  # Accent Color background, Secondary Color text
                           command=lambda opt=option: self.checkIntegrationAnswer(opt),
                           width=50, height=2, relief="raised", bd=2)
            btn.pack(pady=3)

    def generateDifferentiationQuestion(self):
        """Generate differentiation question based on difficulty"""
        # generates differentiation question based on difficulty
        self.currentQuestion = self.gameLogic.generateDifferentiationQuestion(self.difficulty)
        self.questionLabel.config(text=self.currentQuestion["question"])
        self.battleMessage.config(text="⚡ Pikachu is ready to battle! Choose the correct answer to attack!")
        
        # Clear previous options
        for widget in self.optionsFrame.winfo_children():
            widget.destroy()
        
        # Create option buttons
        for option, text in self.currentQuestion["options"].items():
            button_text = option + ". " + text
            btn = tk.Button(self.optionsFrame, text=button_text, 
                           font=("Comic Sans MS", 10), bg="#0077B6", fg="#FFE156",  # Accent Color background, Secondary Color text
                           command=lambda opt=option: self.checkDifferentiationAnswer(opt),
                           width=50, height=2, relief="raised", bd=2)
            btn.pack(pady=3)



    def checkAlgebraAnswer(self, event=None):
        """Check algebra answer with Pokémon battle effects"""
        # checks algebra answer with pokemon battle effects
        try:
            userAnswer = float(self.answerEntry.get())
            is_correct, message = self.gameLogic.checkAlgebraAnswer(userAnswer, self.currentAnswer)
            
            if is_correct:
                # Correct answer - successful attack
                battleMessage = self.gameLogic.getBattleMessages(True)
                self.battleMessage.config(text=battleMessage, fg="#006400")  # Dark green for success
                
                # Flash the enemy pokemon red when hit
                self.flashEnemyRed()
                
                self.handleCorrectAnswer("Correct!")
            else:
                # Wrong answer - attack misses and player gets hit
                battleMessage = self.gameLogic.getBattleMessages(False)
                self.battleMessage.config(text=battleMessage, fg="#8B0000")  # Dark red for failure
                
                # Flash the player's pokemon red when hit
                self.flashPokemonRed()
                
                self.handleWrongAnswer("Wrong!", "Correct answer: " + str(self.currentAnswer))
        except ValueError:
            self.showMessageWithTimerFreeze("Error", "Please enter a valid number!", "error")
            self.answerEntry.delete(0, tk.END)

    def checkSquareRootAnswer(self, event=None):
        """Check square root answer"""
        # checks square root answer - this one's tricky with partial credit
        try:
            userAnswer = float(self.answerEntry.get())
            result = self.gameLogic.checkSquareRootAnswer(userAnswer, self.currentAnswer)
            
            if len(result) == 4:  # Correct format
                is_correct = result[0]
                message = result[1]
                points = result[2]
                deviation = result[3]
                
                if is_correct:
                    # Correct answer - successful attack
                    battleMessage = self.gameLogic.getBattleMessages(True)
                    self.battleMessage.config(text=battleMessage, fg="#006400")  # Dark green for success
                    
                    # Flash the enemy pokemon red when hit
                    self.flashEnemyRed()
                    
                    self.handleCorrectAnswer(message, deviation, points)
                else:
                    # Wrong answer - attack misses and player gets hit
                    battleMessage = self.gameLogic.getBattleMessages(False)
                    self.battleMessage.config(text=battleMessage, fg="#8B0000")  # Dark red for failure
                    
                    # Flash the player's pokemon red when hit
                    self.flashPokemonRed()
                    
                    self.handleWrongAnswer(message, "Deviation: " + str(round(deviation, 3)))
            else:
                self.handleWrongAnswer("Invalid input!", "")
                    
        except ValueError:
            self.showMessageWithTimerFreeze("Error", "Please enter a valid number!", "error")
            self.answerEntry.delete(0, tk.END)

    def checkIntegrationAnswer(self, selectedOption):
        """Check integration answer with difficulty-based scoring and Pokémon battle effects"""
        # checks integration answer with difficulty-based scoring and pokemon battle effects
        is_correct, message = self.gameLogic.checkIntegrationAnswer(selectedOption, self.currentQuestion)
        
        if is_correct:
            # Different scoring based on difficulty
            if self.difficulty == "easy":
                message = "Correct! Great job with basic integration!"
            elif self.difficulty == "medium":
                message = "Excellent! Medium difficulty integration mastered!"
            elif self.difficulty == "hard":
                message = "Outstanding! Advanced integration conquered!"
            else:
                message = "Correct! Great job with integration!"
            
            # Correct answer - successful attack
            battleMessage = self.gameLogic.getBattleMessages(True)
            self.battleMessage.config(text=battleMessage, fg="#006400")  # Dark green for success
            
            # Flash the enemy pokemon red when hit
            self.flashEnemyRed()
            
            self.handleCorrectAnswer(message)
        else:
            # Wrong answer - attack misses and player gets hit
            battleMessage = self.gameLogic.getBattleMessages(False)
            self.battleMessage.config(text=battleMessage, fg="#8B0000")  # Dark red for failure
            
            # Flash the player's pokemon red when hit
            self.flashPokemonRed()
            
            self.handleWrongAnswer("Incorrect!", "Correct answer: " + self.currentQuestion['answer'])

    def checkDifferentiationAnswer(self, selectedOption):
        """Check differentiation answer with difficulty-based scoring and Pokémon battle effects"""
        # checks differentiation answer with difficulty-based scoring and pokemon battle effects
        is_correct, message = self.gameLogic.checkDifferentiationAnswer(selectedOption, self.currentQuestion)
        
        if is_correct:
            # Different scoring based on difficulty
            if self.difficulty == "easy":
                message = "Correct! Great job with basic differentiation!"
            elif self.difficulty == "medium":
                message = "Excellent! Medium difficulty differentiation mastered!"
            elif self.difficulty == "hard":
                message = "Outstanding! Advanced differentiation conquered!"
            else:
                message = "Correct! Great job with differentiation!"
            
            # Correct answer - successful attack
            battleMessage = self.gameLogic.getBattleMessages(True)
            self.battleMessage.config(text=battleMessage, fg="#006400")  # Dark green for success
            
            # Flash the enemy pokemon red when hit
            self.flashEnemyRed()
            
            self.handleCorrectAnswer(message)
        else:
            # Wrong answer - attack misses and player gets hit
            battleMessage = self.gameLogic.getBattleMessages(False)
            self.battleMessage.config(text=battleMessage, fg="#8B0000")  # Dark red for failure
            
            # Flash the player's pokemon red when hit
            self.flashPokemonRed()
            
            self.handleWrongAnswer("Incorrect!", "Correct answer: " + self.currentQuestion['answer'])



    def handleCorrectAnswer(self, message, deviation=None, points=None):
        """Handle correct answer logic"""
        # handles correct answer logic - this is where the fun happens
        if points is not None:
            self.score = self.score + points
        else:
            self.score = self.score + 10
        self.streak = self.streak + 1
        utils.animateScoreLabel(self.scoreLabel, self.root)
        
        # Handle enemy lives reduction for ALL game modes
        # Reduce enemy lives and update display
        self.livesSys.reduceEnemyLives(1)
        
        # Force update the enemy lives display
        self.enemyLivesLabel.config(text=self.livesSys.getEnemyLifeDisplay())
        
        # Check if enemy is defeated
        if self.livesSys.isEnemyDefeated():
            self.handleEnemyDefeated()
            return  # Exit early to avoid further processing
        
        if self.streak % 3 == 0:
            if self.gameMode == "square_root":
                self.score = self.score + 10
            else:
                self.score = self.score + 20
            bonus_message = "🔥 Combo x" + str(self.streak) + "! +" + str(self.score) + " Bonus Points!"
            self.showMessageWithTimerFreeze("Combo!", bonus_message)
        
        utils.playSound("correct")
        
        if deviation is not None:
            deviation_text = "Deviation: " + str(round(deviation, 3))
            points_text = "Points earned: " + str(points)
            full_message = message + "\n" + deviation_text + "\n" + points_text
            self.showMessageWithTimerFreeze("Result", full_message)
        else:
            self.showMessageWithTimerFreeze("Result", message)
        
        self.updateGameDisplay()

    def handleWrongAnswer(self, message, details=""):
        """Handle wrong answer logic"""
        # handles wrong answer logic - not as fun but necessary
        if self.gameMode == "square_root":
            penalty = 2
        else:
            penalty = 5
        
        new_score = self.score - penalty
        if new_score < 0:
            new_score = 0
        self.score = new_score
        
        self.streak = 0
        self.livesSys.reducePlayerLives(1)
        self.livesLabel.config(text=self.livesSys.getPlayerLifeDisplay())
        utils.playSound("incorrect")
        
        # Update enemy lives display for ALL game modes
        self.enemyLivesLabel.config(text=self.livesSys.getEnemyLifeDisplay())
        
        if len(details) > 0:
            fullMessage = message + "\n" + details
        else:
            fullMessage = message
        self.showMessageWithTimerFreeze("Result", fullMessage, "error")
        
        if self.livesSys.isPlayerDefeated():
            self.endGame()
        else:
            self.updateGameDisplay()

    def updateGameDisplay(self):
        """Update game display after answer"""
        # updates game display after answer
        score_text = "Score: " + str(self.score)
        self.scoreLabel.config(text=score_text)
        
        # Update enemy lives display for ALL game modes
        self.enemyLivesLabel.config(text=self.livesSys.getEnemyLifeDisplay())
        
        if self.gameMode == "square_root":
            self.generateSquareRootQuestion()
        elif self.gameMode == "integration":
            self.generateIntegrationQuestion()
        elif self.gameMode == "differentiation":
            self.generateDifferentiationQuestion()
        else:
            self.generateQuestion()
        
        time_text = "Time: " + str(self.timeLeft) + "s"
        self.timeLabel.config(text=time_text)

    def startTimer(self):
        """Start the game timer"""
        # starts the game timer
        if self.timerId:
            self.root.after_cancel(self.timerId)
        
        # Set appropriate time limit based on game mode
        if hasattr(self, 'gameMode'):
            self.timeLeft = self.gameConfig.getTimeLimit(self.gameMode)
        
        self.updateTimer()

    def updateTimer(self):
        """Update game timer"""
        # updates game timer - this runs every second
        if self.timeLeft > 0:
            self.timeLeft = self.timeLeft - 1
            time_text = "Time: " + str(self.timeLeft) + "s"
            self.timeLabel.config(text=time_text)
            if self.timeLeft <= 3:
                utils.animateTimeWarning(self.timeLabel, self.root)
            self.timerId = self.root.after(1000, self.updateTimer)
        else:
            self.livesSys.reducePlayerLives(1)
            self.livesLabel.config(text=self.livesSys.getPlayerLifeDisplay())
            
            # Update enemy lives display for ALL game modes
            self.enemyLivesLabel.config(text=self.livesSys.getEnemyLifeDisplay())
            
            utils.playSound("incorrect")
            if self.livesSys.isPlayerDefeated():
                self.endGame()
            else:
                self.timeLeft = self.gameConfig.getTimeLimit(self.gameMode)
                if self.gameMode == "square_root":
                    self.generateSquareRootQuestion()
                elif self.gameMode == "integration":
                    self.generateIntegrationQuestion()
                elif self.gameMode == "differentiation":
                    self.generateDifferentiationQuestion()
                else:
                    self.generateQuestion()
                self.updateTimer()

    def freezeTimer(self):
        """Freeze the game timer"""
        # freezes the game timer - useful for message boxes
        if self.timerId and not self.timerFrozen:
            self.timerFrozen = True
            self.frozenTimeLeft = self.timeLeft
            self.root.after_cancel(self.timerId)
            self.timerId = None

    def resumeTimer(self):
        """Resume the game timer"""
        # resumes the game timer
        if self.timerFrozen:
            self.timerFrozen = False
            self.timeLeft = self.frozenTimeLeft
            self.startTimer()

    def showMessageWithTimerFreeze(self, title, message, messageType="info"):
        """Show message box with timer freeze/resume"""
        # shows message box with timer freeze/resume - keeps things in sync
        self.freezeTimer()
        
        messageFunctions = {}
        messageFunctions["info"] = messagebox.showinfo
        messageFunctions["error"] = messagebox.showerror
        messageFunctions["warning"] = messagebox.showwarning
        messageFunctions["yesno"] = messagebox.askyesno
        
        if messageType in messageFunctions:
            result = messageFunctions[messageType](title, message)
        else:
            result = messagebox.showinfo(title, message)
        
        self.resumeTimer()
        return result

    def endGame(self):
        """End the game and show results"""
        # ends the game and shows results
        game_over_message = "You're out of lives!\n\nFinal Score: " + str(self.score) + "\n\nReturning to difficulty selection..."
        self.showMessageWithTimerFreeze("Game Over", game_over_message, "info")
        self.dataMgr.updateLeaderboard(self.playerName, self.score, self.difficulty)
        # Always return to difficulty selection page
        self.showUsernameAndDifficultyPage()

    def endGameAfterVictory(self):
        """End the game after a victory with appropriate message"""
        # ends the game after a victory with appropriate message
        victory_message = "Congratulations on your victory!\n\n📊 Final Score: " + str(self.score) + "\n\nReturning to game setup..."
        self.showMessageWithTimerFreeze("🏆 Game Complete!", victory_message, "info")
        self.dataMgr.updateLeaderboard(self.playerName, self.score, self.difficulty)
        # Always return to combined username and difficulty page
        self.showUsernameAndDifficultyPage()

    def setupPokemonBattleUi(self):
        """Setup Pokémon battle game UI with battle background and sprites"""
        # sets up pokemon battle game UI with battle background and sprites - this is the fun part
        self.clearWindow()
        
        # Set up the battle background with Charizard-inspired color
        # Using the Shadow Color (Dark Teal) for the battle arena
        battleBgColor = "#264653"  # Shadow Color (Dark Teal)
        
        # Create background label with pure color
        self.battleBgLabel = tk.Label(self.root, bg=battleBgColor)
        self.battleBgLabel.place(x=0, y=0, relwidth=1, relheight=1)
        print("✅ Battle background set to Charizard-inspired dark teal color!")
        
        # Load pokemon sprites
        try:
            # Load Pikachu sprite (player)
            pikachuImg = Image.open("assets/pikachu.png")
            pikachuImg = pikachuImg.resize((120, 120), Image.Resampling.LANCZOS)
            self.pikachuPhoto = ImageTk.PhotoImage(pikachuImg)
            print("✅ Pikachu sprite loaded successfully!")
            
            # Load enemy pokemon sprites
            # Squirtle
            squirtleImg = Image.open("assets/turtle.png")
            squirtleImg = squirtleImg.resize((120, 120), Image.Resampling.LANCZOS)
            self.squirtlePhoto = ImageTk.PhotoImage(squirtleImg)
            print("✅ Squirtle sprite loaded successfully!")
            
            # Charmander (pokemon_1.png)
            charmanderImg = Image.open("assets/pokemon_1.png")
            charmanderImg = charmanderImg.resize((120, 120), Image.Resampling.LANCZOS)
            self.charmanderPhoto = ImageTk.PhotoImage(charmanderImg)
            print("✅ Charmander sprite loaded successfully!")
            
            # Gengar (pokemon_2.png)
            gengarImg = Image.open("assets/pokemon_2.png")
            gengarImg = gengarImg.resize((120, 120), Image.Resampling.LANCZOS)
            self.gengarPhoto = ImageTk.PhotoImage(gengarImg)
            print("✅ Gengar sprite loaded successfully!")
            
            # Eevee (pokemon_3.png)
            eeveeImg = Image.open("assets/pokemon_3.png")
            eeveeImg = eeveeImg.resize((120, 120), Image.Resampling.LANCZOS)
            self.eeveePhoto = ImageTk.PhotoImage(eeveeImg)
            print("✅ Eevee sprite loaded successfully!")
            
            # Bulbasaur (pokemon_4.png)
            bulbasaurImg = Image.open("assets/pokemon_4.png")
            bulbasaurImg = bulbasaurImg.resize((120, 120), Image.Resampling.LANCZOS)
            self.bulbasaurPhoto = ImageTk.PhotoImage(bulbasaurImg)
            print("✅ Bulbasaur sprite loaded successfully!")
            
        except Exception as e:
            print("❌ pokemon sprite error: " + str(e))
            # Try alternative paths for sprites
            try:
                # Try loading from root directory
                pikachuImg = Image.open("pikachu.png")
                pikachuImg = pikachuImg.resize((120, 120), Image.Resampling.LANCZOS)
                self.pikachuPhoto = ImageTk.PhotoImage(pikachuImg)
                print("✅ Pikachu sprite loaded from root directory!")
                
                squirtleImg = Image.open("turtle.png")
                squirtleImg = squirtleImg.resize((120, 120), Image.Resampling.LANCZOS)
                self.squirtlePhoto = ImageTk.PhotoImage(squirtleImg)
                print("✅ Squirtle sprite loaded from root directory!")
                
                charmanderImg = Image.open("pokemon_1.png")
                charmanderImg = charmanderImg.resize((120, 120), Image.Resampling.LANCZOS)
                self.charmanderPhoto = ImageTk.PhotoImage(charmanderImg)
                print("✅ Charmander sprite loaded from root directory!")
                
                gengarImg = Image.open("pokemon_2.png")
                gengarImg = gengarImg.resize((120, 120), Image.Resampling.LANCZOS)
                self.gengarPhoto = ImageTk.PhotoImage(gengarImg)
                print("✅ Gengar sprite loaded from root directory!")
                
                eeveeImg = Image.open("pokemon_3.png")
                eeveeImg = eeveeImg.resize((120, 120), Image.Resampling.LANCZOS)
                self.eeveePhoto = ImageTk.PhotoImage(eeveeImg)
                print("✅ Eevee sprite loaded from root directory!")
                
                bulbasaurImg = Image.open("pokemon_4.png")
                bulbasaurImg = bulbasaurImg.resize((120, 120), Image.Resampling.LANCZOS)
                self.bulbasaurPhoto = ImageTk.PhotoImage(bulbasaurImg)
                print("✅ Bulbasaur sprite loaded from root directory!")
                
            except Exception as e2:
                print("❌ pokemon sprites not found in root either: " + str(e2))
                # Fallback sprites if images not found
                self.pikachuPhoto = None
                self.squirtlePhoto = None
                self.charmanderPhoto = None
                self.gengarPhoto = None
                self.eeveePhoto = None
                self.bulbasaurPhoto = None
        
        # Select random enemy pokemon
        self.selectRandomEnemy()
        
        # Create battle interface overlay
        battleOverlay = tk.Frame(self.root)
        battleOverlay.place(relx=0.5, rely=0.5, anchor="center")
        
        # Top section - Battle info and stats
        topFrame = tk.Frame(battleOverlay, relief="raised", bd=3)  # Secondary Color (Pale Yellow)
        topFrame.pack(fill="x", pady=10)
        
        # Player side (left) - Pikachu
        playerFrame = tk.Frame(topFrame)
        playerFrame.pack(side="left", padx=20, pady=10)
        
        if self.pikachuPhoto:
            self.pikachuLabel = tk.Label(playerFrame, image=self.pikachuPhoto)
            self.pikachuLabel.pack()
        else:
            self.pikachuLabel = tk.Label(playerFrame, text="⚡ Pikachu", font=("Orbitron", 16, "bold"), 
                    fg="#FF6D28")  # Primary Color for text
            self.pikachuLabel.pack()
        
        player_name_text = "Player: " + self.playerName
        playerNameLabel = tk.Label(playerFrame, text=player_name_text, 
                font=self.labelFont, fg="#4E342E")  # Outline Color for text
        playerNameLabel.pack()
        
        # Battle stats (center)
        statsFrame = tk.Frame(topFrame)
        statsFrame.pack(side="left", padx=40, pady=10)
        
        score_text = "Score: " + str(self.score)
        self.scoreLabel = tk.Label(statsFrame, text=score_text, 
                                   font=self.labelFont, fg="#4E342E")
        self.scoreLabel.pack()
        
        time_text = "Time: " + str(self.timeLeft) + "s"
        self.timeLabel = tk.Label(statsFrame, text=time_text, 
                                  font=self.labelFont, fg="#4E342E")
        self.timeLabel.pack()
        
        self.livesLabel = tk.Label(statsFrame, text=self.livesSys.getPlayerLifeDisplay(), 
                                   font=self.labelFont, fg="#FF6D28")  # Primary Color for lives
        self.livesLabel.pack()
        
        # Enemy side (right) - Random enemy
        enemyFrame = tk.Frame(topFrame)
        enemyFrame.pack(side="right", padx=20, pady=10)
        
        # Display the selected enemy pokemon
        if hasattr(self, 'currentEnemyPhoto') and self.currentEnemyPhoto:
            self.enemyLabel = tk.Label(enemyFrame, image=self.currentEnemyPhoto)
            self.enemyLabel.pack()
        else:
            # Fallback text based on enemy type
            enemyText = self.getEnemyText()
            self.enemyLabel = tk.Label(enemyFrame, text=enemyText, font=("Orbitron", 16, "bold"), 
                    fg="#0077B6")  # Accent Color for enemy text
            self.enemyLabel.pack()
        
        enemyTrainerLabel = tk.Label(enemyFrame, text="Enemy Trainer", 
                font=self.labelFont, fg="#4E342E")  # Outline Color for text
        enemyTrainerLabel.pack()
        
        # Enemy lives display
        self.enemyLivesLabel = tk.Label(enemyFrame, text=self.livesSys.getEnemyLifeDisplay(), 
                                         font=self.labelFont, fg="#264653")  # Shadow Color for enemy lives
        self.enemyLivesLabel.pack()
        
        # Battle arena - middle section
        arenaFrame = tk.Frame(battleOverlay, relief="raised", bd=3)  # Secondary Color (Pale Yellow)
        arenaFrame.pack(fill="x", pady=20)
        
        # Battle message display
        self.battleMessage = tk.Label(arenaFrame, text="", font=self.labelFont, 
                                     wraplength=400, fg="#4E342E")  # Outline Color for text
        self.battleMessage.pack(pady=10)
        
        # Question area
        self.questionLabel = tk.Label(arenaFrame, text="", font=("Comic Sans MS", 14), 
                                     wraplength=400, fg="#4E342E")  # Outline Color for text
        self.questionLabel.pack(pady=10)
        
        # Answer area - will be configured based on game mode
        self.answerFrame = tk.Frame(arenaFrame)
        self.answerFrame.pack(pady=10)
        
        # Action buttons
        buttonFrame = tk.Frame(arenaFrame)
        buttonFrame.pack(pady=10)
        
        backButton = tk.Button(buttonFrame, text="Back", font=self.buttonFont, bg="#264653",  # Shadow Color
                  fg="#FFE156", command=self.confirmBackToMenu, relief="raised", bd=2)
        backButton.pack(side="left", padx=5)
        
        returnButton = tk.Button(buttonFrame, text="Return to Start", font=self.buttonFont, bg="#f44336",  # Red color
                  fg="#FFE156", command=self.confirmReturnToStart, relief="raised", bd=2)
        returnButton.pack(side="left", padx=5)
        
        # Configure answer area based on game mode
        self.configureAnswerArea()

    def configureAnswerArea(self):
        """Configure the answer area based on game mode"""
        # configures the answer area based on game mode
        # Clear previous answer widgets
        for widget in self.answerFrame.winfo_children():
            widget.destroy()
        
        if self.gameMode in ["algebra", "square_root"]:
            # Text input for algebra, square root, and pokemon battle
            answerPromptLabel = tk.Label(self.answerFrame, text="Your Answer:", font=("Comic Sans MS", 14), 
                    fg="#4E342E")  # Secondary Color background, Outline Color text
            answerPromptLabel.pack()
            
            self.answerEntry = tk.Entry(self.answerFrame, font=("Comic Sans MS", 14), width=20, 
                                       fg="#4E342E", relief="raised", bd=2)  # Secondary Color background, Outline Color text
            self.answerEntry.pack(pady=5)
            
            # Bind to appropriate check method
            if self.gameMode == "algebra":
                self.answerEntry.bind("<Return>", self.checkAlgebraAnswer)
                attackBtn = tk.Button(self.answerFrame, text="⚡ Attack!", font=self.buttonFont, bg="#FF6D28",  # Primary Color
                                      fg="#FFE156", command=self.checkAlgebraAnswer, width=15, height=2, relief="raised", bd=2)  # Secondary Color text
            elif self.gameMode == "square_root":
                self.answerEntry.bind("<Return>", self.checkSquareRootAnswer)
                attackBtn = tk.Button(self.answerFrame, text="⚡ Attack!", font=self.buttonFont, bg="#FF6D28",  # Primary Color
                                      fg="#FFE156", command=self.checkSquareRootAnswer, width=15, height=2, relief="raised", bd=2)  # Secondary Color text

            
            attackBtn.pack(pady=5)
            
        elif self.gameMode in ["integration", "differentiation"]:
            # Multiple choice for integration and differentiation
            self.optionsFrame = tk.Frame(self.answerFrame)  # Secondary Color
            self.optionsFrame.pack(pady=5)
            
            # Options will be populated by the question generation methods

    def selectRandomEnemy(self):
        """Select a random enemy Pokémon"""
        # selects a random enemy pokemon
        enemies = []
        enemies.append({"name": "Squirtle", "photo": self.squirtlePhoto, "text": "💧 Squirtle", "color": "#87CEEB"})
        enemies.append({"name": "Charmander", "photo": self.charmanderPhoto, "text": "🔥 Charmander", "color": "#FF6B35"})
        enemies.append({"name": "Gengar", "photo": self.gengarPhoto, "text": "👻 Gengar", "color": "#8B5A96"})
        enemies.append({"name": "Eevee", "photo": self.eeveePhoto, "text": "🦊 Eevee", "color": "#D2B48C"})
        enemies.append({"name": "Bulbasaur", "photo": self.bulbasaurPhoto, "text": "🌱 Bulbasaur", "color": "#90EE90"})
        
        self.currentEnemy = random.choice(enemies)
        self.currentEnemyPhoto = self.currentEnemy["photo"]
        self.currentEnemyName = self.currentEnemy["name"]
        print("🎯 Selected enemy: " + self.currentEnemyName)

    def getEnemyName(self):
        """Get the name of the current enemy"""
        # gets the name of the current enemy
        if hasattr(self, 'currentEnemy'):
            return self.currentEnemy["name"]
        return "Squirtle"  # Default fallback

    def getEnemyText(self):
        """Get the text representation of the current enemy"""
        # gets the text representation of the current enemy
        if hasattr(self, 'currentEnemy'):
            return self.currentEnemy["text"]
        return "💧 Squirtle"  # Default fallback

    def getEnemyColor(self):
        """Get the color for the current enemy"""
        # gets the color for the current enemy
        if hasattr(self, 'currentEnemy'):
            return self.currentEnemy["color"]
        return "#87CEEB"  # Default fallback

    def flashPokemonRed(self):
        """Make the player's Pokémon flash red when hit"""
        # makes the player's pokemon flash red when hit
        if hasattr(self, 'pikachuLabel'):
            # Flash the Pikachu label red
            originalBg = self.pikachuLabel.cget('bg')
            self.pikachuLabel.config(bg='red')
            
            # Return to original color after 300ms
            def restoreColor():
                self.pikachuLabel.config(bg=originalBg)
            self.root.after(300, restoreColor)
        else:
            # Fallback: flash the entire player frame
            self.flashPlayerFrameRed()

    def flashEnemyRed(self):
        """Make the enemy's Pokémon flash red when hit"""
        # makes the enemy's pokemon flash red when hit
        if hasattr(self, 'enemyLabel'):
            # Flash the enemy label red
            originalBg = self.enemyLabel.cget('bg')
            self.enemyLabel.config(bg='red')
            
            # Return to original color after 300ms
            def restoreColor():
                self.enemyLabel.config(bg=originalBg)
            self.root.after(300, restoreColor)
        else:
            # Fallback: flash the entire enemy frame
            self.flashEnemyFrameRed()

    def flashPlayerFrameRed(self):
        """Flash the entire player frame red as fallback"""
        # flashes the entire player frame red as fallback
        # Find the player frame (first frame in the top section)
        for widget in self.root.winfo_children():
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if hasattr(child, 'winfo_children'):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Frame) and grandchild.cget('bg') == '#FED000':
                                # This is likely the player frame
                                originalBg = grandchild.cget('bg')
                                grandchild.config(bg='red')
                                def restoreColor():
                                    grandchild.config(bg=originalBg)
                                self.root.after(300, restoreColor)
                                return

    def flashEnemyFrameRed(self):
        """Flash the entire enemy frame red as fallback"""
        # flashes the entire enemy frame red as fallback
        # Find the enemy frame (right side frame in the top section)
        for widget in self.root.winfo_children():
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if hasattr(child, 'winfo_children'):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Frame) and grandchild.cget('bg') == '#FED000':
                                # This is likely the enemy frame (right side)
                                originalBg = grandchild.cget('bg')
                                grandchild.config(bg='red')
                                def restoreColor():
                                    grandchild.config(bg=originalBg)
                                self.root.after(300, restoreColor)
                                return

    def handleEnemyDefeated(self):
        """Handle when enemy is defeated"""
        # handles when enemy is defeated - victory!
        enemyName = self.getEnemyName()
        victoryMessage = self.gameLogic.getVictoryMessages(enemyName)
        self.battleMessage.config(text=victoryMessage, fg="#FF9F1C")  # Orange color for victory  
        
        # Add bonus points for defeating enemy
        bonusPoints = 50
        self.score = self.score + bonusPoints
        
        # Show victory message with appropriate title and content
        victory_title = "🎉 VICTORY! 🎉"
        victory_content = victoryMessage + "\n\n🏆 Bonus Points: +" + str(bonusPoints) + "\n📊 Current Score: " + str(self.score) + "\n\nWould you like to battle another trainer?"
        result = self.showMessageWithTimerFreeze(victory_title, victory_content, "yesno")
        
        if result:
            # Reset enemy lives for next battle
            self.livesSys.resetEnemyLives()
            self.enemyLivesLabel.config(text=self.livesSys.getEnemyLifeDisplay())
            
            # Select a new random enemy for the next battle
            self.selectRandomEnemy()
            
            # Update the enemy display
            if hasattr(self, 'enemyLabel'):
                if self.currentEnemyPhoto:
                    self.enemyLabel.config(image=self.currentEnemyPhoto)
                else:
                    self.enemyLabel.config(text=self.getEnemyText(), fg=self.getEnemyColor())
            
            # Generate new question and clear answer entry
            if self.gameMode == "square_root":
                self.generateSquareRootQuestion()
            elif self.gameMode == "integration":
                self.generateIntegrationQuestion()
            elif self.gameMode == "differentiation":
                self.generateDifferentiationQuestion()
            else:
                self.generateQuestion()
            
            # Reset battle message to default state
            self.battleMessage.config(fg="black")  # Reset color to default

        else:
            # End game after victory with appropriate message
            self.endGameAfterVictory()

    def showLeaderboard(self):
        """Show leaderboard page"""
        # shows leaderboard page
        self.clearWindow()
        self.drawBackground()  # Use Pokemon pixel background
        
        self.dataMgr.leaderboard = self.dataMgr.loadLeaderboard()
        leaderboardFrame = self.createCenteredFrame()

        leaderboardTitleLabel = tk.Label(leaderboardFrame, text="Leaderboard", font=self.titleFont, bg="#0C1A31", fg="white")
        leaderboardTitleLabel.grid(row=0, column=0, pady=20)
        
        for idx in range(len(self.dataMgr.leaderboard)):
            entry = self.dataMgr.leaderboard[idx]
            playerName = entry.get('player_name', 'Unknown Player')
            leaderboard_text = str(idx + 1) + ". " + playerName + " - Score: " + str(entry['score']) + " (" + entry['difficulty'] + ") - " + entry['timestamp']
            leaderboardEntryLabel = tk.Label(leaderboardFrame, text=leaderboard_text, font=self.labelFont)
            leaderboardEntryLabel.grid(row=idx + 1, column=0, pady=2)

        buttons = []
        buttons.append(("Delete All Records", "#ff4444", "white", self.confirmDeleteAll))
        buttons.append(("Back", self.btnColor, "white", self.createStartMenu))
        buttons.append(("Return to Start", "#264653", "white", self.createStartMenu))
        
        # Create a frame for buttons to arrange them horizontally
        buttonFrame = tk.Frame(leaderboardFrame, bg="#0C1A31")
        buttonFrame.grid(row=len(self.dataMgr.leaderboard) + 1, column=0, pady=20)
        
        for i in range(len(buttons)):
            button_info = buttons[i]
            text = button_info[0]
            bg = button_info[1]
            fg = button_info[2]
            command = button_info[3]
            
            button = tk.Button(buttonFrame, text=text, font=self.buttonFont, bg=bg,
                     fg=fg, command=command, width=15, height=2)
            button.grid(row=0, column=i, padx=10)

    def confirmDeleteAll(self):
        """Handle delete all records confirmation"""
        # handles delete all records confirmation
        if len(self.dataMgr.leaderboard) == 0:
            messagebox.showinfo("No Records", "There are no records to delete.")
            return
        
        delete_message = "Are you sure you want to delete ALL " + str(len(self.dataMgr.leaderboard)) + " records?\n\nThis action cannot be undone!"
        result = messagebox.askyesno("Delete All Records", delete_message)
        if result:
            success, message = self.dataMgr.deleteAllRecords()
            if success:
                messagebox.showinfo("Records Deleted", message)
            else:
                messagebox.showerror("Error", message)
            self.showLeaderboard()

    def confirmBackToMenu(self):
        """Handle back to menu confirmation"""
        # handles back to menu confirmation
        if hasattr(self, 'score') and self.score > 0:
            if self.timerId:
                self.root.after_cancel(self.timerId)
                self.timerId = None
            
            back_message = "Are you sure you want to return to the difficulty selection?\n\nCurrent Score: " + str(self.score) + "\nDifficulty: " + self.difficulty.capitalize() + "\n\nYour score will be saved before returning."
            result = messagebox.askyesno("Return to Menu", back_message)
            if result:
                self.dataMgr.updateLeaderboard(self.playerName, self.score, self.difficulty)
                save_message = "Your score of " + str(self.score) + " has been saved to the leaderboard!"
                messagebox.showinfo("Score Saved", save_message)
                self.showUsernameAndDifficultyPage()
            else:
                self.startTimer()
        else:
            self.showDifficultySelection()

    def confirmReturnToStart(self):
        """Handle return to start menu confirmation"""
        # handles return to start menu confirmation
        if hasattr(self, 'score') and self.score > 0:
            if self.timerId:
                self.root.after_cancel(self.timerId)
                self.timerId = None
            
            return_message = "Are you sure you want to return to the start menu?\n\nCurrent Score: " + str(self.score) + "\nDifficulty: " + self.difficulty.capitalize() + "\n\nYour score will be saved before returning."
            result = messagebox.askyesno("Return to Start Menu", return_message)
            if result:
                self.dataMgr.updateLeaderboard(self.playerName, self.score, self.difficulty)
                save_message = "Your score of " + str(self.score) + " has been saved to the leaderboard!"
                messagebox.showinfo("Score Saved", save_message)
                self.createStartMenu()
            else:
                self.startTimer()
        else:
            self.createStartMenu()

    def confirmExit(self):
        """Handle exit confirmation"""
        # handles exit confirmation
        if hasattr(self, 'score') and self.score > 0:
            if self.timerId:
                self.root.after_cancel(self.timerId)
                self.timerId = None
            
            exit_message = "Are you sure you want to exit?\n\nCurrent Score: " + str(self.score) + "\nDifficulty: " + self.difficulty.capitalize() + "\n\nYour score will be saved before exiting."
            result = messagebox.askyesno("Exit Game", exit_message)
            if result:
                self.dataMgr.updateLeaderboard(self.playerName, self.score, self.difficulty)
                save_message = "Your score of " + str(self.score) + " has been saved to the leaderboard!"
                messagebox.showinfo("Score Saved", save_message)
                self.root.quit()
            else:
                self.startTimer()
        else:
            result = messagebox.askyesno("Exit Game", "Are you sure you want to exit?")
            if result:
                self.root.quit() 
