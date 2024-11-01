# Rooky Road 2D Side-Scroller Shooter

Rooky Road is a 2D side-scrolling shooter game built using Python's `pygame` library. Players control a soldier, defending against waves of enemies. The gameplay is inspired by "Plants vs Zombies," where enemies approach from the left, and the player must strategically defeat them to prevent health depletion.

## Table of Contents

- [Features](#features)
- [Game Mechanics](#game-mechanics)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Future Enhancements](#future-enhancements)
- [Credits](#credits)

## Features

- **Side-Scroller Shooter**: Players shoot enemies approaching from the left side of the screen.
- **Player and Enemy Animations**: Smooth animation sequences for player movement, shooting, and enemy approach.
- **Score and Health Tracking**: Players accumulate points by defeating enemies and keeping their base health intact.
- **Background Music and Sound Effects**: Engaging sound effects and background music to enhance the experience.
- **Main and End Menus**: Includes a start menu with options to play, view options, and exit, and an end menu displaying the score with restart and exit options.

## Game Mechanics

- **Player Movement**: The player can move up, down, left, and right using the arrow keys or `WASD`. Speed increases when holding `Shift`.
- **Shooting**: Press `X` to shoot bullets toward the enemies. Shooting has a cooldown timer.
- **Enemy Spawning**: Enemies spawn randomly from various lanes and approach the player’s base. If they reach the base, the player loses health.
- **Scoring System**: The player's score is calculated based on time survived and enemies defeated. Defeating enemies increases the score, while letting enemies reach the base depletes health.
- **Health System**: Player and base health are displayed on the screen, with the game ending when base health reaches zero.

## Installation

1. **Install Python**: Ensure Python 3.x is installed.
2. **Install pygame**:
   ```bash
   pip install pygame
