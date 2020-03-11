# Pokemon Top Trumps
To start playing, run: `python3 start.py`

## Games Modes
- [Single Match](#single-match)
- [Traditional](#traditional)
- [Deplete](#deplete)
- [~~PvP~~ (not implemented yet)](#pvp)

### General Gameplay
- A coin flip will determine who starts the game; if it's heads, you start!
- When a round starts, each player will draw one card from the deck, 
    starting with whomever won the last round, or the initial coin toss.
- On a player's turn, they call out a stat they want to compete with.
    - The turn player then announces the chosen stat and both players compare values.
    - The winner then takes the loser's card (depending on the game mode).
    - If there is a draw, the cards are set aside and both players draw again.
    - The final winner of this 'mini-round wins ALL cards!
    - This repeats until there are no cards left in the neutral deck.

### Single Match
You start the game with one round; you choose when to stop!

### Traditional
- The player to obtain ALL cards wins!
- Once the neutral deck is empty, players start using their accumulated decks.

### Deplete
When the neutral deck is depleted, the player with the highest number of cards wins!

### PvP
Enter your opponent's IP address and agree on a game mode!

## High Scores
There are individual score boards for each game mode and a matching score board for PvP.
Python's `shelve` library is used for persistent storage of score boards.

## Data Source
Uses `pokebase`, a wrapper for `PokeAPI` backend.

## TODO
- [ ] persistent high scores
- [ ] import / export score boards
- [ ] network games (PvP)
