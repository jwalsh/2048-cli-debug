#!/usr/bin/env python3
"""
Claude Plays 2048 - Shows board state for Claude to make decisions
After 50 auto-moves, Claude takes manual control
"""

import time
import random
import click
from tty_manual.tty_reader import TTYReader
from tty_manual.board_analyzer import BoardAnalyzer


def display_board(board, score, move_num):
    """Display board in a clear format for Claude to see"""
    click.echo(f"\n{'='*40}")
    click.echo(f"Move {move_num} | Score: {score}")
    click.echo("="*40)
    
    # Display board with nice formatting
    for row in board:
        click.echo("|", nl=False)
        for cell in row:
            if cell == 0:
                click.echo("     |", nl=False)
            else:
                click.echo(f"{cell:5}|", nl=False)
        click.echo()
    click.echo("="*40)


@click.command()
def main():
    """Let Claude play 2048!"""
    reader = TTYReader()
    move_count = 0
    auto_moves = 50
    
    click.echo("🎮 Claude Plays 2048!")
    click.echo("First 50 moves: Auto down-right spam")
    click.echo("Then: Claude takes control\n")
    
    # Start game
    reader.start_game()
    time.sleep(0.5)
    
    # Get initial board
    output = reader.read_output()
    if not reader.parse_board_state(output):
        click.echo("Failed to start!", err=True)
        return
        
    click.echo(f"Starting - Current high score: {reader.high_score}")
    
    try:
        # Auto-spam phase
        click.echo("Auto-spamming", nl=False)
        while move_count < auto_moves:
            move_count += 1
            
            # Simple down-right spam
            if random.random() < 0.5:
                move = 's'  # down
            else:
                move = 'd'  # right
                
            reader.send_move(move)
            time.sleep(0.05)
            
            output = reader.read_output()
            reader.parse_board_state()
            
            if move_count % 10 == 0:
                click.echo(".", nl=False)
                
        click.echo("\n\n🎯 CLAUDE TAKES CONTROL!")
        
        # Manual phase - show board for Claude
        while True:
            # Display current state
            display_board(reader.current_board, reader.current_score, move_count)
            
            # Analyze board
            analyzer = BoardAnalyzer(reader.current_board)
            scores = analyzer.get_complexity_score()
            
            click.echo(f"Empty cells: {scores['empty_cells']}")
            click.echo(f"Max tile: {scores['max_tile']} ({'corner' if scores['max_in_corner'] else 'NOT in corner'})")
            click.echo(f"Merge opportunities: {scores['merge_opportunities']}")
            click.echo(f"Complexity: {scores['complexity']:.1f}/100")
            
            # Get Claude's move
            click.echo("\nClaude's move (w/a/s/d or q to quit): ", nl=False)
            move = click.getchar()
            
            if move == 'q':
                break
            elif move not in ['w', 'a', 's', 'd']:
                click.echo("Invalid move!")
                continue
                
            # Execute move
            move_count += 1
            reader.send_move(move)
            time.sleep(0.2)
            
            output = reader.read_output()
            if not reader.parse_board_state():
                click.echo("Failed to read board!")
                
            if "Game over" in output:
                click.echo("\n🏁 GAME OVER!")
                display_board(reader.current_board, reader.current_score, move_count)
                break
                
            # Check for high score
            if reader.current_score > 1708:
                click.echo(f"\n🎉 NEW HIGH SCORE: {reader.current_score}!")
                reader.save_board_snapshot(f"claude_victory_{reader.current_score}.txt")
                
    except KeyboardInterrupt:
        click.echo("\nInterrupted!")
    finally:
        click.echo(f"\nFinal score: {reader.current_score}")
        click.echo(f"Total moves: {move_count}")
        
        if reader.current_score > 1708:
            click.echo(f"\n🏆 BEAT THE HIGH SCORE BY {reader.current_score - 1708} POINTS!")
            
        reader.cleanup()


if __name__ == "__main__":
    main()