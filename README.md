# Pass-the-Phone Chess Game

A classic chess game designed as a "pass-the-phone" experience, developed in Python with Pygame for the user interface. This application allows two players to play on a single device, sharing turns to make moves. The project emphasizes simplicity in its design and mechanics, while offering a traditional chess experience.

## Features

- **Player vs. Player**: Both players take turns on the same device.
- **Basic Chess Mechanics**: All standard chess rules are implemented, including:
  - Piece movement (pawns, rooks, knights, bishops, queen, king).
  - Special moves, such as castling, en passant, and pawn promotion.
- **Turn-Based System**: Ensures each player alternates turns.
- **Check Detection**: Alerts players if the king is in check.
- **Game Over Conditions**: Includes checkmate and stalemate detection.

## Getting Started

### Prerequisites

- Python 3.9
- Pygame library

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/username/pass-the-phone-chess.git
   cd pass-the-phone-chess
   ```
2. **Install Pygame**:
   ```bash
   pip install pygame
   ```
2. **Run the game**:
   ```bash
   python main.py
   ```

### Controls

- Tap on Pieces: Select a piece by clicking or tapping on it.
- Move Selection: Once a piece is selected, possible moves are highlighted. Click on a highlighted square to move.
- Turn System: At the end of each turn, pass the device to the other player.

## Future Enhancements

- **AI Opponent**: Add an optional AI for solo play.
- **Move History**: Implement an in-game move log.
- **Timed Games**: Add a timer option to simulate biltz chess.
- **Online Games**: Create a backend, which the pygame window can communicate with.

## Lincense

This project is open-source and available for personal and educational use.
