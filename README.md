# 🐍 Minesweeper (Python Edition) + Experimental Bot

Hi there!  
This is the very first version of my Minesweeper game that I built in Python — before turning it into a browser extension.

## 🎮 About the Python Game

At first, I wanted to recreate the classic Minesweeper using Python. I used the `tkinter` library for the interface because it's simple, fast, and good for small GUI projects.

The game includes:
- Adjustable difficulty levels (easy, medium, hard)
- Timer
- Flagging system
- First-click always safe
- Basic win/lose logic

It was a good starting point for understanding how the game works behind the scenes.

## 🤖 Minesweeper Bot (Work in Progress)

After finishing the basic game, I got curious about making a bot that could play Minesweeper on its own — just like a human would.

### Goals I had for the bot:
- Use `pyautogui` to detect the game board
- Read cell values from the screen using pixel color
- Implement basic logic for safe moves and flagging
- Avoid clicking on mines
- React when a cell is revealed (or if it explodes 💥)

Right now, the bot:
- Can locate the board on screen (with fixed pixel dimensions)
- Recognizes revealed cells and flags
- Can left/right click cells
- Starts playing, but doesn't stop after hitting a mine (still needs logic here)

### Status:
🧪 The bot is not complete yet, but the main idea is already working.  
Anyone can take this version and improve it — smarter decision-making, better visual detection, or even full auto-solving.

## 🛠️ Technologies Used

- `python` (core logic)
- `tkinter` (for GUI)
- `pyautogui` (for the bot)
- `pillow` (for image processing, optional)
- `time`, `random`, `os`, etc.

## 📌 To-Do & Ideas

- [ ] Add advanced logic (e.g. probability-based moves)
- [ ] Dynamic screen scaling (for different board sizes)
- [ ] Add a toggle to stop the bot when it hits a mine
- [ ] Add screenshot-based OCR to read numbers (optional)
- [ ] Rewrite into modular structure


## 💬 Final Notes

This was a fun side project that taught me more about game logic, automation, and how much thought goes into even a simple puzzle game like Minesweeper.  
The bot still needs love, but it's a great base to build from — feel free to fork it and experiment!

Enjoy — and don't step on a mine 😄
