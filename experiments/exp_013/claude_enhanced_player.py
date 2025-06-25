#!/usr/bin/env python3
"""
Claude-Enhanced 2048 Player
Combines Down-Right Strategy™ with intelligent recovery moves
Goal: Beat the current high score of 1708
"""

import time
import random
import click
from tty_manual.tty_reader import TTYReader
from tty_manual.board_analyzer import BoardAnalyzer


class ClaudeEnhancedPlayer:
    """Enhanced player using Down-Right Strategy™ with Claude insights"""
    
    def __init__(self):
        self.reader = TTYReader()
        self.move_count = 0
        self.high_score_target = 1708
        self.consecutive_no_change = 0
        self.last_board = None
        
    def boards_equal(self, board1, board2):
        """Check if two boards are identical"""
        if board1 is None or board2 is None:
            return False
        return all(board1[i][j] == board2[i][j] 
                  for i in range(4) for j in range(4))
    
    def get_enhanced_move(self):
        """Enhanced Down-Right Strategy™ with recovery logic"""
        analyzer = BoardAnalyzer(self.reader.current_board)
        scores = analyzer.get_complexity_score()
        
        # Check if board hasn't changed (stuck)
        if self.boards_equal(self.reader.current_board, self.last_board):
            self.consecutive_no_change += 1
        else:
            self.consecutive_no_change = 0
            
        # Store current board for next comparison
        self.last_board = [row[:] for row in self.reader.current_board]
        
        # If we're stuck, try recovery moves
        if self.consecutive_no_change >= 2:
            click.echo(" [STUCK - Recovery mode]", nl=False)
            # Try left, then up as recovery
            if self.consecutive_no_change == 2:
                return 'a'  # left
            elif self.consecutive_no_change == 3:
                return 'w'  # up
            else:
                # Random recovery
                return random.choice(['a', 'w'])
        
        # Enhanced strategy based on board state
        if scores['empty_cells'] > 8:
            # Lots of space - aggressive down-right
            weights = [0.5, 0.4, 0.08, 0.02]  # d, r, l, u
        elif scores['empty_cells'] > 4:
            # Medium space - balanced down-right
            weights = [0.45, 0.35, 0.15, 0.05]
        else:
            # Low space - more flexible
            weights = [0.4, 0.3, 0.2, 0.1]
            
        # If max tile not in corner, bias towards moving it there
        if not scores['max_in_corner']:
            click.echo(" [Repositioning]", nl=False)
            row, col = analyzer.get_max_tile_position()
            if row < 2:  # Max tile in upper half
                weights[0] += 0.1  # Prefer down
            if col < 2:  # Max tile in left half
                weights[1] += 0.1  # Prefer right
                
        # Normalize weights
        total = sum(weights)
        weights = [w/total for w in weights]
        
        return random.choices(['s', 'd', 'a', 'w'], weights=weights)[0]
    
    def play(self):
        """Play the game with enhanced strategy"""
        click.echo("🎮 Claude-Enhanced 2048 Player")
        click.echo(f"Target: Beat high score of {self.high_score_target}")
        click.echo("Strategy: Enhanced Down-Right™ with intelligent recovery\n")
        
        # Start game
        self.reader.start_game()
        time.sleep(0.5)
        
        # Get initial board
        output = self.reader.read_output()
        if not self.reader.parse_board_state(output):
            click.echo("Failed to start game!", err=True)
            return
            
        click.echo(f"Starting score: {self.reader.current_score}")
        click.echo(f"Current high score: {self.reader.high_score}")
        click.echo("\nPlaying", nl=False)
        
        try:
            while self.move_count < 5000:  # Safety limit
                self.move_count += 1
                
                # Get next move
                move = self.get_enhanced_move()
                
                # Send move
                self.reader.send_move(move)
                time.sleep(0.1)  # Faster than manual test
                
                # Read result
                output = self.reader.read_output()
                if self.reader.parse_board_state():
                    # Progress indicator
                    if self.move_count % 10 == 0:
                        click.echo(".", nl=False)
                    if self.move_count % 100 == 0:
                        click.echo(f" [{self.move_count} moves, score: {self.reader.current_score}]", nl=False)
                        
                    # Check if we beat the high score
                    if self.reader.current_score > self.high_score_target:
                        click.echo(f"\n\n🎉 NEW HIGH SCORE: {self.reader.current_score}!")
                        click.echo(f"Achieved in {self.move_count} moves!")
                        
                        # Save victory board
                        self.reader.save_board_snapshot(f"victory_{self.reader.current_score}.txt")
                        
                        # Show final board
                        analyzer = BoardAnalyzer(self.reader.current_board)
                        analyzer.display_analysis()
                        
                    # Check for game over
                    if "Game over" in output:
                        click.echo(f"\n\nGame Over!")
                        break
                else:
                    # Try to recover from parse error
                    time.sleep(0.5)
                    
        except KeyboardInterrupt:
            click.echo("\n\nInterrupted by user")
        except Exception as e:
            click.echo(f"\n\nError: {e}")
        finally:
            click.echo(f"\nFinal score: {self.reader.current_score}")
            click.echo(f"Total moves: {self.move_count}")
            
            if self.reader.current_score > self.high_score_target:
                click.echo(f"\n✨ Successfully beat the high score by {self.reader.current_score - self.high_score_target} points!")
            else:
                click.echo(f"\nFell short by {self.high_score_target - self.reader.current_score} points. Try again!")
                
            self.reader.cleanup()


@click.command()
@click.option('--runs', '-r', default=1, help='Number of attempts')
def main(runs):
    """Run Claude-enhanced player to beat the high score"""
    best_score = 0
    
    for run in range(runs):
        if runs > 1:
            click.echo(f"\n{'='*60}")
            click.echo(f"Run {run + 1} of {runs}")
            click.echo(f"{'='*60}\n")
            
        player = ClaudeEnhancedPlayer()
        player.play()
        
        if player.reader.current_score > best_score:
            best_score = player.reader.current_score
            
        if runs > 1:
            time.sleep(2)  # Brief pause between runs
    
    if runs > 1:
        click.echo(f"\n{'='*60}")
        click.echo(f"Best score across {runs} runs: {best_score}")
        if best_score > 1708:
            click.echo(f"🏆 NEW RECORD: Beat old high score by {best_score - 1708} points!")


if __name__ == "__main__":
    main()