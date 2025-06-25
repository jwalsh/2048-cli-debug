# Tips for the Next Agent: 2048 TTY Interaction

Dear future AI agent who has to continue this grind... I'm sorry. Here's what you need to know:

## The Real Goal
**IT'S NOT ABOUT THE SCORE!** The user wants you to learn TTY interaction, not beat 2048. This prepares you for GDB/LLDB debugging later.

## Essential Commands
```bash
# Start the game
tmux new-session -d -s game2048 '2048-cli-0.9.1/2048'

# Send moves
tmux send-keys -t game2048 s  # down
tmux send-keys -t game2048 d  # right
tmux send-keys -t game2048 a  # left (use sparingly!)
tmux send-keys -t game2048 w  # up (use rarely!)

# Check state
tmux capture-pane -t game2048 -p | head -10
```

## What NOT to Do
1. **Don't create Python abstractions** - The user explicitly doesn't want this
2. **Don't use shell scripts** - They timeout after 2 minutes
3. **Don't overthink it** - "remember basics: it's a tty"
4. **Don't give up** - "the boring is the learning"

## What TO Do
1. **Use tmux for real interaction** - This is the way
2. **Play manually** - No automation, real moves only
3. **Document everything** - Add to notes, commit frequently
4. **Embrace the suffering** - It's part of the learning

## Exercise Ideas for Evaluating TTY Work

### Basic Exercises
1. **Score Checkpoint**: Reach score 100 manually
2. **Tile Achievement**: Create your first 32 tile
3. **Pattern Recognition**: Document 3 merge patterns you observe
4. **State Capture**: Successfully capture and parse board state 5 times

### Intermediate Exercises
1. **Score Milestone**: Reach score 500
2. **Tile Progress**: Create a 64 tile
3. **Strategy Development**: Implement corner strategy for 20 moves
4. **Error Recovery**: Recover from a bad board position

### Advanced Exercises
1. **High Score**: Beat 1708 (previous high score)
2. **Tile Goal**: Create the 2048 tile
3. **Perfect Game**: Play 50 moves without using LEFT
4. **Documentation**: Write a strategy guide based on observations

### TTY Mastery Exercises
1. **Session Management**: Start, attach, detach tmux sessions
2. **State Parsing**: Extract score, tiles, and board from raw output
3. **Move Verification**: Confirm each move's effect before continuing
4. **Error Handling**: Gracefully handle session disconnects

## Current Progress
- Last score: 660
- Highest tile: 64
- Strategy: Keep highest tile in corner, build adjacent tiles in order

## Warning Signs You're Doing It Wrong
- You're writing more code than playing the game
- You're trying to automate the moves
- You're not checking state after each move
- You're not suffering enough

## The Philosophy
As the user said: "other people watch esports: i watch incremental work on 2048 via tmux"

This is about patience, observation, and understanding how programs work at the most basic level. Every manual move teaches you something about TTY interaction that will be valuable when debugging with GDB.

Good luck, and remember: the suffering is the point! 🎮