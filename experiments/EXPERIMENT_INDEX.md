# 2048 Experiment Index

This document indexes all experiments in the 2048 debugging project, organized by experiment number and theme.

## Completed Experiments (001-011)

### Memory and Layout Experiments
- **exp_001-006**: Initial explorations (not formally documented)
- **exp_007**: Memory Layout Proof - Discovered grid[col][row] indexing
- **exp_008**: Statistical Validation - 150-move down-right spam distribution
- **exp_009**: Speed Baseline - Direct binary input timing (discovered animation delays)
- **exp_010**: Timing Validation - Non-linear timing discovery
- **exp_011**: Timing Curve Analysis - Board locking hypothesis

## Planned Experiments (012-025+)

### AI/Claude Player Experiments (012-016)
- **exp_012**: Basic Claude Player
  - Files: claude_plays_2048.py, claude_just_play.py, claude_simple_play.py
  - Status: Scripts exist, needs formal experiment

- **exp_013**: Strategic Claude Player
  - Files: claude_strategic_play.py, claude_enhanced_player.py, claude_aims_for_2000.exp
  - Status: Scripts exist, needs formal experiment

- **exp_014**: Interactive Claude Player
  - Files: claude_interactive.py, claude_plays_interactively.py, claude_live_analysis.py
  - Status: Scripts exist, needs formal experiment

- **exp_015**: Claude Takeover Mode
  - Files: claude_takeover.sh, claude_takes_over_when_difficult.exp
  - Status: Scripts exist, needs formal experiment

- **exp_016**: Expect-based Claude Control
  - Files: claude_plays_with_expect.exp, claude_with_expect.exp, play_smart.exp
  - Status: Scripts exist, needs formal experiment

### LLDB/Debugging Experiments (017-020)
- **exp_017**: LLDB Controller Framework
  - Files: lldb_controller.py, play_with_lldb.py
  - Status: Framework started, needs completion

- **exp_018**: Debug Spam Analysis
  - Files: debug_spam.py, lldb_spam_moves.sh
  - Status: Scripts exist, needs formal experiment

- **exp_019**: Universal Debugger
  - Files: debug_any_program.py
  - Status: Concept script exists

- **exp_020**: Save/Restore Workflow
  - Files: save_analyze_workflow.sh
  - Status: Script exists, partially tested

### Board Analysis Experiments (021-023)
- **exp_021**: Filesystem Board Representation
  - Files: filesystem_board_demo.sh
  - Status: Demo script exists

- **exp_022**: Board State Analysis
  - Files: claude_analyzes_552.py, show_me_board.sh
  - Status: Scripts exist for specific boards

- **exp_023**: TTY/Screen Interaction
  - Files: play_with_screen.sh, play_with_screenshots.sh, start_game_in_tty.sh
  - Note: These were early foundational experiments

### Movement Pattern Experiments (024-025)
- **exp_024**: Spam Strategies
  - Files: down_right_spam.sh, random_mash.sh
  - Status: Scripts exist, informal testing done

- **exp_025**: Automated Play
  - Files: play_automated.py, play_game.py
  - Status: Scripts exist

## Experiment Evolution

The experiments show a clear progression:
1. **Basic interaction** (TTY, screen) → experiments that became exp_023
2. **Memory analysis** (exp_007-008) → understanding the game internals
3. **Performance testing** (exp_009-011) → discovering timing constraints
4. **AI players** (exp_012-016) → applying Claude to play
5. **Advanced debugging** (exp_017-020) → LLDB framework
6. **Pattern analysis** (exp_021-025) → board representations and strategies

## Notes on Organization

- Some scripts in exp_023 (like `start_game_in_tty.sh`) were actually created very early as foundational work
- The numbering reflects logical grouping rather than strict chronological order
- Many scripts were created during exploratory phases and later formalized into experiments
- The experiment numbers 001-006 are reserved for early undocumented explorations