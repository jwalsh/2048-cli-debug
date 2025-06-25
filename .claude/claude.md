# Claude's 2048 TTY Control Journey

## 🎯 The Real Goal
**It's not about beating 2048!** It's about learning to interact with running programs through their actual interfaces (TTY, screen, expect, eventually GDB/LLDB).

User quote: "the goal is maybe 2000? i don't really care since you running an interactive program is the goal"

## 📚 What We Learned (The Hard Way)

### ❌ Failed Approaches
1. **Shell scripts** - Timeout after 2 minutes, can't maintain interactive session
2. **Python pty module** - Process crashes with `OSError: [Errno 5] Input/output error`
3. **GNU screen** - Created session but couldn't capture output properly
4. **Python abstractions** - Too many layers, lost direct control

### ✅ What Works: EXPECT!
```bash
# Basic pattern that works
spawn 2048-cli-0.9.1/2048
expect "Score:"
send "s"  # Send moves
expect "Score:"
send "q"  # Quit
```

## 🚀 Current Working Approach

### Key Scripts
1. **claude_with_expect.exp** - Simple proof of concept
2. **claude_plays_with_expect.exp** - Full player with strategies
3. **claude_takes_over_when_difficult.exp** - The best approach:
   - Spam until board becomes "difficult"
   - Claude takes strategic control
   - Shows move-by-move decisions

### Running the Game
```bash
# Make sure expect is installed
brew install expect

# Run the main script
./claude_takes_over_when_difficult.exp
```

## 🐛 Known Oddities

1. **Score stays at 0 during spam phase** - Even though tiles are merging, score doesn't update until strategic phase
2. **Board never gets truly "difficult"** - Need better detection than just looking for 64+ tiles
3. **Game sometimes crashes after ~500 moves** - Might be buffer overflow or TTY issues

## 🎮 Strategy Notes

### Spam Phase (Down-Right Strategy™)
- 40% down, 30% right, 15% left, 15% up
- Academically proven to reach ~1708 points
- Creates complex board states for Claude to solve

### Strategic Phase
- Keep largest tile in corner (preferably bottom-left)
- Build ordered sequences (2048 → 1024 → 512 → 256...)
- Merge opportunistically but maintain structure
- Use UP sparingly (only for recovery)

## 📈 Progress Tracking
- Best spam-only score: 1708
- Best Claude-assisted score: ~600
- Target score: 2000+ (but remember, score doesn't matter!)
- **ACTUAL GOAL: Create a 2048 tile in the game called 2048!** 🤦‍♂️

## 🔮 Next Steps
1. Improve "difficulty" detection in expect scripts
2. Parse actual board tiles not just score
3. Eventually move to GDB/LLDB for direct memory inspection

## 💡 Key Insight
User: "imagine i said 'create an eshell in emacs' and we would not have a great time"

Some tasks require real interaction with the running process, not abstractions!

## 🎬 To Continue This Work
1. Clone the repo
2. Read this file and `docs/learning_notes.md`
3. Check GitHub issues #5 (TTY approach) and #9 (Expect approach)
4. Run `./claude_takes_over_when_difficult.exp` to see current state
5. Try to beat 2000 using expect-based TTY control!

Remember: The journey matters more than the destination. We're learning to control running programs, not just playing 2048!