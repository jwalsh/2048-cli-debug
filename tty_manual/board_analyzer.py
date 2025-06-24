#!/usr/bin/env python3
"""
Board Analyzer for 2048 - Analyzes board complexity and suggests strategies
Part of Issue #5: TTY-based 2048 controller implementation
"""

import numpy as np
from typing import List, Dict, Tuple
import click


class BoardAnalyzer:
    """Analyzes 2048 board state for complexity and strategy decisions"""
    
    def __init__(self, board: List[List[int]]):
        self.board = np.array(board)
        self.rows, self.cols = self.board.shape
        
    def get_empty_cells(self) -> int:
        """Count empty cells on the board"""
        return np.count_nonzero(self.board == 0)
    
    def get_max_tile(self) -> int:
        """Get the highest tile value"""
        return np.max(self.board)
    
    def get_max_tile_position(self) -> Tuple[int, int]:
        """Get position of the highest tile"""
        max_val = self.get_max_tile()
        positions = np.argwhere(self.board == max_val)
        return tuple(positions[0]) if len(positions) > 0 else (-1, -1)
    
    def is_max_tile_in_corner(self) -> bool:
        """Check if the highest tile is in a corner"""
        row, col = self.get_max_tile_position()
        corners = [(0, 0), (0, self.cols-1), (self.rows-1, 0), (self.rows-1, self.cols-1)]
        return (row, col) in corners
    
    def get_monotonicity_score(self) -> float:
        """Calculate how well-ordered the board is (higher is better)"""
        score = 0.0
        
        # Check rows
        for row in self.board:
            # Left to right
            left_right = all(row[i] <= row[i+1] for i in range(len(row)-1) if row[i] != 0 or row[i+1] != 0)
            # Right to left
            right_left = all(row[i] >= row[i+1] for i in range(len(row)-1) if row[i] != 0 or row[i+1] != 0)
            if left_right or right_left:
                score += 1.0
                
        # Check columns
        for col in range(self.cols):
            column = self.board[:, col]
            # Top to bottom
            top_bottom = all(column[i] <= column[i+1] for i in range(len(column)-1) if column[i] != 0 or column[i+1] != 0)
            # Bottom to top
            bottom_top = all(column[i] >= column[i+1] for i in range(len(column)-1) if column[i] != 0 or column[i+1] != 0)
            if top_bottom or bottom_top:
                score += 1.0
                
        return score / (self.rows + self.cols)  # Normalize to 0-1
    
    def get_merge_opportunities(self) -> int:
        """Count how many adjacent tiles can be merged"""
        merges = 0
        
        # Check horizontal merges
        for i in range(self.rows):
            for j in range(self.cols - 1):
                if self.board[i][j] != 0 and self.board[i][j] == self.board[i][j+1]:
                    merges += 1
                    
        # Check vertical merges
        for i in range(self.rows - 1):
            for j in range(self.cols):
                if self.board[i][j] != 0 and self.board[i][j] == self.board[i+1][j]:
                    merges += 1
                    
        return merges
    
    def get_scattered_score(self) -> float:
        """Calculate how scattered high-value tiles are (lower is better)"""
        # Find all tiles >= 64
        high_tiles = np.argwhere(self.board >= 64)
        if len(high_tiles) <= 1:
            return 0.0
            
        # Calculate average Manhattan distance between high tiles
        total_distance = 0
        count = 0
        
        for i in range(len(high_tiles)):
            for j in range(i + 1, len(high_tiles)):
                dist = abs(high_tiles[i][0] - high_tiles[j][0]) + abs(high_tiles[i][1] - high_tiles[j][1])
                total_distance += dist
                count += 1
                
        return total_distance / count if count > 0 else 0.0
    
    def get_complexity_score(self) -> Dict[str, float]:
        """Calculate overall board complexity (0-100, higher = more complex)"""
        empty_cells = self.get_empty_cells()
        max_tile = self.get_max_tile()
        max_in_corner = self.is_max_tile_in_corner()
        monotonicity = self.get_monotonicity_score()
        merges = self.get_merge_opportunities()
        scattered = self.get_scattered_score()
        
        # Calculate complexity factors
        empty_factor = max(0, 1 - (empty_cells / 4))  # Less empty = more complex
        corner_factor = 0 if max_in_corner else 0.5   # Max not in corner = more complex
        monotonicity_factor = 1 - monotonicity         # Less ordered = more complex
        merge_factor = max(0, 1 - (merges / 4))       # Fewer merges = more complex
        scattered_factor = min(1, scattered / 6)       # More scattered = more complex
        
        # Weighted complexity score
        complexity = (
            empty_factor * 30 +
            corner_factor * 20 +
            monotonicity_factor * 20 +
            merge_factor * 20 +
            scattered_factor * 10
        )
        
        return {
            'complexity': complexity,
            'empty_cells': empty_cells,
            'max_tile': max_tile,
            'max_in_corner': max_in_corner,
            'monotonicity': monotonicity,
            'merge_opportunities': merges,
            'scattered_score': scattered,
            'empty_factor': empty_factor,
            'corner_factor': corner_factor,
            'monotonicity_factor': monotonicity_factor,
            'merge_factor': merge_factor,
            'scattered_factor': scattered_factor
        }
    
    def needs_manual_inspection(self, threshold: float = 70) -> bool:
        """Determine if the board needs manual inspection"""
        return self.get_complexity_score()['complexity'] >= threshold
    
    def suggest_strategy(self) -> str:
        """Suggest a strategy based on board state"""
        scores = self.get_complexity_score()
        
        if scores['empty_cells'] <= 2:
            return "CRITICAL: Focus on creating merges"
        elif not scores['max_in_corner']:
            return "REPOSITION: Move max tile to corner"
        elif scores['monotonicity'] < 0.5:
            return "ORGANIZE: Improve tile ordering"
        elif scores['merge_opportunities'] == 0:
            return "STUCK: Try different directions"
        else:
            return "CONTINUE: Keep down-right strategy"
    
    def display_analysis(self) -> None:
        """Display a formatted analysis of the board"""
        scores = self.get_complexity_score()
        
        click.echo("\n=== Board Analysis ===")
        click.echo(f"Complexity Score: {scores['complexity']:.1f}/100")
        click.echo(f"Empty Cells: {scores['empty_cells']}")
        click.echo(f"Max Tile: {scores['max_tile']} ({'corner' if scores['max_in_corner'] else 'not corner'})")
        click.echo(f"Monotonicity: {scores['monotonicity']:.2f}")
        click.echo(f"Merge Opportunities: {scores['merge_opportunities']}")
        click.echo(f"Scattered Score: {scores['scattered_score']:.2f}")
        click.echo(f"\nStrategy: {self.suggest_strategy()}")


@click.command()
@click.argument('board_file', type=click.File('r'))
@click.option('--threshold', '-t', default=70, help='Complexity threshold for manual inspection')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def main(board_file, threshold, output_json):
    """Analyze a 2048 board from a file"""
    import json
    
    # Parse board from file
    lines = board_file.readlines()
    board = []
    
    for line in lines:
        # Look for lines with pipe characters (board rows)
        if '|' in line and '---' not in line:
            cells = line.split('|')[1:-1]  # Remove first and last empty
            row = []
            for cell in cells:
                cell = cell.strip()
                row.append(int(cell) if cell else 0)
            if len(row) == 4:  # Valid row
                board.append(row)
    
    if len(board) != 4:
        click.echo("Error: Could not parse a valid 4x4 board", err=True)
        return
    
    # Analyze
    analyzer = BoardAnalyzer(board)
    
    if output_json:
        scores = analyzer.get_complexity_score()
        scores['needs_inspection'] = analyzer.needs_manual_inspection(threshold)
        scores['strategy'] = analyzer.suggest_strategy()
        click.echo(json.dumps(scores, indent=2))
    else:
        analyzer.display_analysis()
        if analyzer.needs_manual_inspection(threshold):
            click.echo(f"\n⚠️  Board complexity exceeds threshold ({threshold})")
            click.echo("Manual inspection recommended!")


if __name__ == "__main__":
    main()