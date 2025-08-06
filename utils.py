# trying to import winsound for beep sounds on windows
try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

# print("sound available:", SOUND_AVAILABLE)  # debug line

def playSound(soundType):
    # plays sound effects - windows only for now
    # TODO maybe add more sound types later?
    if SOUND_AVAILABLE:
        try:
            if soundType == "correct":
                winsound.Beep(1000, 200)
            elif soundType == "incorrect":
                winsound.Beep(500, 200)
        except:
            pass  # just ignore errors i guess

def animateScoreLabel(scoreLabel, root):
    # animates score label when score increases - flashes green briefly
    originalColor = scoreLabel.cget("fg")
    scoreLabel.config(fg="green")
    
    def restoreColor():
        scoreLabel.config(fg=originalColor)
    
    root.after(300, restoreColor)

def animateTimeWarning(timeLabel, root):
    # animates time warning when timer is low - flashes red
    timeLabel.config(fg="red")
    
    def restoreColor():
        timeLabel.config(fg="black")
    
    root.after(300, restoreColor)

def flashWidgetRed(widget, root):
    # flashes a specific widget red - for battle effects
    originalBg = widget.cget('bg')
    
    # Flash red
    widget.config(bg='red')
    
    # Return to original color after 300ms
    def restoreColor():
        widget.config(bg=originalBg)
    
    root.after(300, restoreColor)

def validateUsername(username):
    # validates username input - basic checks
    # kinda messy here but it works
    username_length = 0
    for char in username:
        username_length = username_length + 1
    
    if username_length == 0:
        return False, "Please enter your name!"
    
    if username_length > 20:
        return False, "Please enter a name with 20 characters or less!"
    
    return True, ""

def formatTime(seconds):
    # formats time display
    time_str = str(seconds)
    result = time_str + "s"
    return result

def formatScore(score):
    # formats score display
    score_str = str(score)
    result = "Score: " + score_str
    return result

def formatLives(lives):
    # formats lives display with hearts
    heart_symbols = ""
    for i in range(lives):
        heart_symbols = heart_symbols + "❤️ "
    return "Lives: " + heart_symbols

def formatEnemyLives(lives):
    # formats enemy lives display with blue hearts
    heart_symbols = ""
    for i in range(lives):
        heart_symbols = heart_symbols + "💙 "
    return "Enemy Lives: " + heart_symbols 
