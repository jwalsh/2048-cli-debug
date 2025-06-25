import struct
import sys
import os

save_dir = os.path.dirname(os.path.abspath(__file__))

# Read grid data
with open(os.path.join(save_dir, 'grid.bin'), 'rb') as f:
    grid_data = f.read()

# Decode grid
values = struct.unpack('<16I', grid_data)

# Calculate statistics
non_zero = [v for v in values if v > 0]
tiles = [2**v if v > 0 else 0 for v in values]
max_tile = max(tiles)
total_tiles = len(non_zero)
empty_cells = 16 - total_tiles

print("=== Board Analysis ===")
print(f"Timestamp: {os.path.basename(save_dir)}")
print(f"Non-empty cells: {total_tiles}")
print(f"Empty cells: {empty_cells}")
print(f"Highest tile: {max_tile}")
print(f"\nBoard layout:")

# Print board (accounting for column-major storage)
for row in range(4):
    row_str = "|"
    for col in range(4):
        idx = col * 4 + row  # Column-major
        tile = tiles[idx]
        row_str += f"{str(tile):>5} |"
    print(row_str)

# Save summary
with open(os.path.join(save_dir, 'summary.txt'), 'w') as f:
    f.write(f"Highest tile: {max_tile}\n")
    f.write(f"Empty cells: {empty_cells}\n")
    f.write(f"Board hash: {hash(tuple(values))}\n")
