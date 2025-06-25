import struct

with open('grid_only.bin', 'rb') as f:
    grid_data = f.read()

# Read 16 32-bit integers
values = struct.unpack('<16I', grid_data)

print("Decoded 2048 Grid:")
print("Raw values:", values)
print("\nBoard layout:")
for row in range(4):
    row_tiles = []
    for col in range(4):
        idx = row * 4 + col
        val = values[idx]
        tile = (2 ** val) if val > 0 else 0
        row_tiles.append(str(tile).center(5))
    print("|" + "|".join(row_tiles) + "|")

print(f"\nHighest tile: {max(2**v if v > 0 else 0 for v in values)}")
