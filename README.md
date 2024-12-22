# Flip and Find: A Memory Card Game

## Description

Flip and Find is a fun and challenging memory card game built using Python and the Pygame library. The objective of the game is to test your memory skills by finding matching pairs of cards. But beware, hidden among the cards are bombs that will shuffle the remaining unmatched cards, adding an extra layer of difficulty!

## How to Play

1. **Start the Game:** Run the `main.py` file to start the game.
2. **Select Difficulty:**
    *   On the main menu, click the "New Game" button.
    *   Choose your difficulty level: "Easy", "Medium", or "Hard". The difficulty affects the number of cards, the time limit, and the number of bombs.
3. **Gameplay:**
    *   The game board will be displayed with cards face down.
    *   Click on two cards to flip them over.
    *   If the cards match, they will remain face up.
    *   If the cards don't match, they will flip back over after a short delay.
    *   If you reveal a bomb, the remaining unmatched cards will shuffle their positions!
4. **Timer:** Keep an eye on the timer in the top right corner. You need to find all the matching pairs before time runs out.
5. **Winning:** You win the game if you find all matching pairs before the timer reaches zero.
6. **Losing:** You lose the game if the timer runs out before you find all the pairs.
7. **End Screen:**
    *   After winning or losing, an end screen will appear.
    *   Click "Play Again" to start a new game with the same difficulty.
    *   Click "Back to Menu" to return to the main menu and choose a different difficulty or exit the game.

## Game Features

*   **Multiple Difficulty Levels:** Easy, Medium, and Hard, each offering a different level of challenge.
*   **Animated Card Shuffling:** When a bomb is revealed, the remaining unmatched cards will animate and shuffle to new positions, making it harder to remember their locations.
*   **Timer:** A countdown timer adds a sense of urgency to the game.
*   **Sound Effects:** The game includes sound effects for card clicks and win/lose conditions.
*   **Visual Feedback:** The timer turns red and vibrates when there are only 5 seconds left.
*   **Rounded Corners:** The card backs have rounded corners for a visually appealing look.
*   **Customizable Card Back:** You can change the image on the back of the cards by replacing the `card_back.png` file in the `Assets` folder.

## Requirements

To run this game, you need the following:

1. **Python 3:** Make sure you have Python 3 installed on your computer. You can download it from the official Python website ([https://www.python.org/downloads/](https://www.python.org/downloads/)).
2. **Pygame Library:** This game requires the Pygame library. You can install it using `pip`:
    ```bash
    pip install pygame
    ```
3. **Assets Folder:** Ensure that you have the `Assets` folder in the same directory as the game files. This folder contains:
    *   **Background Images:** Images for the main menu, difficulty selection screen, win screen, and lose screen (in the `Assets/bg` subfolder).
    *   **Card Images:** Images for the card faces (in the `Assets/object` subfolder).
    *   **Card Back Image:** The image for the back of the cards (`card_back.png`).
    *   **Font File:** The font used for the game text (`Pixelicious.ttf`).
    *   **Sound Files:** Sound effects for card clicks, timer warnings, and win/lose conditions (`tap.wav`, `warning.mp3`, `win.wav`, `lose.wav`).
4. **Game Files:** You'll need all the Python files for the game:
    *   `main.py`
    *   `game_logic.py`
    *   `start_screen.py`
    *   `end_screen.py`
    *   `timer.py`
    *   `effects.py`

## How to Run

1. **Make sure you have met all the requirements listed above.**
2. **Navigate to the game's directory** in your terminal or command prompt.
3. **Run the following command:**

    ```bash
    python main.py
    ```

## Notes

*   You can customize the game by changing the images in the `Assets` folder. Make sure to keep the same file names if you replace existing images.
*   The difficulty levels control the following:
    *   **Easy:** 3x3 grid, 1 bomb, 30-second time limit.
    *   **Medium:** 4x4 grid, 2 bombs, 50-second time limit.
    *   **Hard:** 5x5 grid, 3 bombs, 80-second time limit.

## Have Fun!

Enjoy playing Flip and Find! If you have any questions or feedback, please don't hesitate to contact the developer.