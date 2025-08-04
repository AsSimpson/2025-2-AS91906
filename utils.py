# Try importing winsound for Windows beep sound effects
try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

def play_sound(sound_type):
    """Play sound effects"""
    if SOUND_AVAILABLE:
        try:
            if sound_type == "correct":
                winsound.Beep(1000, 200)
            elif sound_type == "incorrect":
                winsound.Beep(500, 200)
        except:
            pass

def animate_score_label(score_label, root):
    """Animate score label when score increases"""
    original_color = score_label.cget("fg")
    score_label.config(fg="green")
    root.after(300, lambda: score_label.config(fg=original_color))

def animate_time_warning(time_label, root):
    """Animate time warning when timer is low"""
    time_label.config(fg="red")
    root.after(300, lambda: time_label.config(fg="black"))

def flash_widget_red(widget, root):
    """Flash a specific widget red"""
    original_bg = widget.cget('bg')
    
    # Flash red
    widget.config(bg='red')
    
    # Return to original color after 300ms
    root.after(300, lambda: widget.config(bg=original_bg))

def validate_username(username):
    """Validate username input"""
    if not username:
        return False, "Please enter your name!"
    
    if len(username) > 20:
        return False, "Please enter a name with 20 characters or less!"
    
    return True, ""

def format_time(seconds):
    """Format time display"""
    return f"{seconds}s"

def format_score(score):
    """Format score display"""
    return f"Score: {score}"

def format_lives(lives):
    """Format lives display"""
    return "Lives: " + "❤️ " * lives

def format_enemy_lives(lives):
    """Format enemy lives display"""
    return "Enemy Lives: " + "💙 " * lives 