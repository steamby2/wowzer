# wowzer - World of Warcraft Automation Bot
## Python & OpenCV Tutorial Project for Fishing and Grinding

This project is an educational tutorial on AI and computer vision using Python and OpenCV. It demonstrates basic Python and OpenCV techniques for game automation. The bot now includes:

1. **Fishing Bot**: Automatically casts fishing and catches fish in different zones.
2. **Grinding Bot**: Automatically finds enemies, fights them, and loots them.

## Features

### Core Features
- Screen capture and analysis using OpenCV
- Template matching for object detection
- Keyboard and mouse automation via PyAutoGUI
- Multithreaded operation for responsive performance

### Fishing Bot
- Detects fishing bobber using template matching
- Watches for bite detection using color changes
- Automatically reels in and recasts

### Grinding Bot (New!)
- Enemy detection and targeting
- Class-specific combat rotations
- Pathfinding and navigation
- Loot collection
- Resource management (health/mana)
- Stuck detection and recovery

## Installation

1. Clone this repository
2. Install dependencies:
```
pip install opencv-python pyautogui numpy pillow
```

## Usage

Run the bot with:
```
python src/wowzer.py
```

### Commands
- `S` - Start screen capture
- `Z` - Set zone
- `F` - Start fishing
- `G` - Start grinding (NEW!)
- `C` - Set character class (NEW!)
- `Q` - Quit wowzer

## Customization

### Adding New Combat Classes
Edit the `combat.py` file to add new class rotations.

### Setting Up Grinding Areas
Configure grinding areas by adding waypoints in `navigation.py`.

## Educational Use Only

This project is intended for educational purposes to demonstrate computer vision and automation techniques. Using bots in online games may violate the terms of service and could result in your account being banned.

## License

This project is licensed under GNU GPL v3.