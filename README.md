# Math Master Game - Modular Structure

This is a refactored version of the Math Master game with a clean, modular structure.

## File Structure

```
math_game/
├── main.py                    # Entry point (minimal)
├── game_core.py              # Core game classes (LivesSystem, GameConfig)
├── game_ui.py                # All UI-related code (MathGame class)
├── game_logic.py             # Game modes and logic
├── data_manager.py           # File operations and data handling
├── utils.py                  # Utility functions and helpers
└── README.md                 # This file
```

## File Descriptions

### main.py
- Simple entry point that creates the main window and starts the game
- Only ~5 lines of code

### game_core.py
- `LivesSystem` class: Manages player and enemy lives
- `GameConfig` class: Centralized configuration for all game settings
- Game constants and time limits

### game_ui.py
- `MathGame` class: Main UI class with all interface logic
- Menu navigation, game screens, Pokémon battle UI
- Window management and user interaction

### game_logic.py
- `GameLogic` class: Handles all game logic
- Question generation for all game modes
- Answer checking and scoring logic
- Battle messages and victory handling

### data_manager.py
- `DataManager` class: Handles all data operations
- Leaderboard management
- Player gold coins and store system
- File I/O operations

### utils.py
- Sound effects and animations
- Input validation and formatting
- Common utility functions

## Benefits of This Structure

1. **Separation of Concerns**: Each file has a specific responsibility
2. **Maintainability**: Easy to find and modify specific functionality
3. **Testability**: Individual components can be tested separately
4. **Scalability**: Easy to add new features or game modes
5. **Readability**: Code is organized logically

## How to Run

1. Make sure all files are in the `math_game` directory
2. Run `python main.py` from the `math_game` directory
3. The game will start with the main menu

## Dependencies

- tkinter (built-in)
- PIL (Pillow) for image handling
- question.py (your existing question file)
- Assets folder with Pokémon sprites and backgrounds

## Migration Notes

- The original `main.py` has been split into these modular files
- All functionality is preserved
- The game should work exactly the same as before
- Each file is focused and manageable in size 