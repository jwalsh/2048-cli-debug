#!/usr/bin/env python3
"""
Manual Test Runner - Integrates TTY reader and board analyzer
Part of Issue #5: TTY-based 2048 controller implementation
"""

import os
import time
import json
import uuid
from pathlib import Path
from datetime import datetime, timezone
import click

from .tty_reader import TTYReader
from .board_analyzer import BoardAnalyzer


class ManualTestRunner:
    """Runs 2048 with automated spam and manual inspection points"""
    
    def __init__(self, spam_moves=50, check_interval=10, complexity_threshold=70):
        self.spam_moves = spam_moves
        self.check_interval = check_interval
        self.complexity_threshold = complexity_threshold
        self.test_guid = str(uuid.uuid4())
        self.move_count = 0
        self.log_dir = Path(f"logs/manual_test_{self.test_guid}")
        self.reader = TTYReader()
        
        # Setup logging directories
        self.log_dir.mkdir(parents=True, exist_ok=True)
        (self.log_dir / "boards").mkdir(exist_ok=True)
        (self.log_dir / "checkpoints").mkdir(exist_ok=True)
        
        # Initialize logs
        self._init_config()
        self._init_move_log()
        
    def _init_config(self):
        """Initialize test configuration file"""
        config = {
            "test_guid": self.test_guid,
            "start_time": datetime.now(timezone.utc).isoformat() + "Z",
            "spam_moves": self.spam_moves,
            "check_interval": self.check_interval,
            "complexity_threshold": self.complexity_threshold,
            "strategy": "down_right_spam"
        }
        with open(self.log_dir / "config.json", "w") as f:
            json.dump(config, f, indent=2)
            
    def _init_move_log(self):
        """Initialize move log file"""
        with open(self.log_dir / "moves.log", "w") as f:
            f.write(f"# Move log for test {self.test_guid}\n")
            f.write("# Format: move_number,direction,timestamp,score,complexity\n")
            
    def _log_move(self, direction, score=0, complexity=0):
        """Log a move to the moves file"""
        with open(self.log_dir / "moves.log", "a") as f:
            timestamp = datetime.now(timezone.utc).isoformat() + "Z"
            f.write(f"{self.move_count},{direction},{timestamp},{score},{complexity:.1f}\n")
            
    def _save_board_snapshot(self):
        """Save current board state"""
        if self.reader.current_board:
            board_file = self.log_dir / "boards" / f"move_{self.move_count:04d}.txt"
            self.reader.save_board_snapshot(str(board_file))
            
            # Also save as JSON for analysis
            json_file = self.log_dir / "boards" / f"move_{self.move_count:04d}.json"
            with open(json_file, "w") as f:
                json.dump(self.reader.get_board_dict(), f, indent=2)
                
    def _get_spam_move(self):
        """Get next move for spam phase (down-right strategy)"""
        import random
        # 40% down, 30% right, 20% left, 10% up
        rand = random.random()
        if rand < 0.4:
            return 's'  # down
        elif rand < 0.7:
            return 'd'  # right
        elif rand < 0.9:
            return 'a'  # left
        else:
            return 'w'  # up
            
    def _check_complexity(self):
        """Check if board needs manual inspection"""
        if not self.reader.current_board:
            return False
            
        analyzer = BoardAnalyzer(self.reader.current_board)
        scores = analyzer.get_complexity_score()
        
        return scores['complexity'] >= self.complexity_threshold, scores
        
    def _manual_inspection(self, complexity_scores):
        """Handle manual inspection checkpoint"""
        checkpoint_file = self.log_dir / "checkpoints" / f"check_{self.move_count:04d}.txt"
        
        click.echo("\n" + "="*50)
        click.echo("=== MANUAL INSPECTION REQUIRED ===")
        click.echo("="*50)
        click.echo(f"Test: {self.test_guid}")
        click.echo(f"Move: {self.move_count}")
        click.echo(f"Score: {self.reader.current_score}")
        click.echo(f"Complexity: {complexity_scores['complexity']:.1f}/100")
        click.echo("")
        
        # Display board
        analyzer = BoardAnalyzer(self.reader.current_board)
        analyzer.display_analysis()
        
        # Save checkpoint
        with open(checkpoint_file, "w") as f:
            f.write(f"Manual Inspection at Move {self.move_count}\n")
            f.write(f"Complexity: {complexity_scores['complexity']:.1f}\n")
            f.write(f"Score: {self.reader.current_score}\n")
            f.write(json.dumps(complexity_scores, indent=2))
        
        # Get user decision
        click.echo("\nOptions:")
        click.echo("  [c] Continue auto-spam")
        click.echo("  [m] Manual move")
        click.echo("  [s] Switch strategy (not implemented)")
        click.echo("  [q] Quit and analyze")
        
        choice = click.prompt("Choice", type=click.Choice(['c', 'm', 's', 'q']))
        
        with open(checkpoint_file, "a") as f:
            f.write(f"\nUser choice: {choice}\n")
            
        if choice == 'm':
            move = click.prompt("Enter move", type=click.Choice(['w', 'a', 's', 'd']))
            with open(checkpoint_file, "a") as f:
                f.write(f"Manual move: {move}\n")
            return move
        elif choice == 'q':
            return 'quit'
        else:
            return None  # Continue auto-spam
            
    def run(self):
        """Run the manual test"""
        click.echo(f"🎮 Starting Manual TTY Test")
        click.echo(f"Test ID: {self.test_guid}")
        click.echo(f"Spam moves: {self.spam_moves}")
        click.echo(f"Check interval: {self.check_interval}")
        click.echo(f"Complexity threshold: {self.complexity_threshold}")
        click.echo("")
        
        # Start game
        self.reader.start_game()
        time.sleep(0.5)
        
        # Get initial board
        output = self.reader.read_output()
        if not self.reader.parse_board_state(output):
            click.echo("Failed to parse initial board!", err=True)
            return
            
        click.echo(f"Initial score: {self.reader.current_score}")
        click.echo(f"High score: {self.reader.high_score}")
        
        # Main game loop
        try:
            while self.move_count < 1000:  # Safety limit
                self.move_count += 1
                
                # Save board snapshot every 10 moves
                if self.move_count % 10 == 0:
                    self._save_board_snapshot()
                
                # Determine next move
                if self.move_count <= self.spam_moves:
                    # Auto-spam phase
                    move = self._get_spam_move()
                    click.echo(".", nl=False)  # Progress indicator
                else:
                    # Check complexity every interval
                    if self.move_count % self.check_interval == 0:
                        click.echo("")  # New line
                        needs_inspection, scores = self._check_complexity()
                        
                        if needs_inspection:
                            result = self._manual_inspection(scores)
                            if result == 'quit':
                                break
                            elif result:  # Manual move
                                move = result
                            else:  # Continue spam
                                move = self._get_spam_move()
                        else:
                            click.echo(f"Move {self.move_count}: Complexity {scores['complexity']:.1f} - continuing auto-spam")
                            move = self._get_spam_move()
                    else:
                        move = self._get_spam_move()
                        click.echo(".", nl=False)
                
                # Send move
                try:
                    self.reader.send_move(move)
                    time.sleep(0.2)
                    
                    # Read result
                    output = self.reader.read_output()
                    if self.reader.parse_board_state():
                        # Log move with score and complexity
                        analyzer = BoardAnalyzer(self.reader.current_board)
                        complexity = analyzer.get_complexity_score()['complexity']
                        self._log_move(move, self.reader.current_score, complexity)
                        
                        # Check for game over
                        if "Game over" in output:
                            click.echo("\nGame Over!")
                            break
                except OSError as e:
                    click.echo(f"\nI/O Error: {e}")
                    click.echo("Game process may have ended")
                    break
                        
        except KeyboardInterrupt:
            click.echo("\nInterrupted by user")
            
        finally:
            self._finish_test()
            self.reader.cleanup()
            
    def _finish_test(self):
        """Save final test summary"""
        summary = {
            "test_guid": self.test_guid,
            "end_time": datetime.now(timezone.utc).isoformat() + "Z",
            "total_moves": self.move_count,
            "final_score": self.reader.current_score,
            "status": "completed"
        }
        
        with open(self.log_dir / "summary.json", "w") as f:
            json.dump(summary, f, indent=2)
            
        click.echo(f"\n\nTest completed!")
        click.echo(f"Total moves: {self.move_count}")
        click.echo(f"Final score: {self.reader.current_score}")
        click.echo(f"Results saved to: {self.log_dir}")


@click.command()
@click.option('--spam-moves', '-s', default=50, help='Number of initial spam moves')
@click.option('--check-interval', '-i', default=10, help='Moves between complexity checks')
@click.option('--threshold', '-t', default=70, help='Complexity threshold for manual inspection')
def main(spam_moves, check_interval, threshold):
    """Run manual test with TTY reader and board analyzer"""
    runner = ManualTestRunner(spam_moves, check_interval, threshold)
    runner.run()


if __name__ == "__main__":
    main()