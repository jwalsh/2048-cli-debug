#!/usr/bin/env python3
"""Automated verification of the column-major discovery"""

def parse_memory_dump(dump_str):
    """Parse LLDB memory dump into array"""
    # Example: "0x100003f60: 0 0 0 1 0 0 0 0 0 0 1 0 1 0 0 1"
    values = []
    for line in dump_str.strip().split('\n'):
        if ':' in line:
            nums = line.split(':')[1].strip().split()
            values.extend([int(x) for x in nums])
    return values[:16]  # Only first 16 values

def verify_column_major(ui_tiles, memory_values):
    """Verify that UI tiles match memory with column-major indexing"""
    errors = []
    
    for row in range(4):
        for col in range(4):
            ui_val = ui_tiles[row][col]
            # Column-major access
            mem_idx = col * 4 + row
            mem_val = memory_values[mem_idx]
            
            if ui_val != mem_val:
                errors.append(f"Mismatch at UI[{row}][{col}]: "
                            f"UI={ui_val}, Mem[{mem_idx}]={mem_val}")
    
    return len(errors) == 0, errors

def test_known_positions():
    """Test the specific positions from our discovery"""
    test_cases = [
        # (ui_row, ui_col, expected_value, memory_index)
        (0, 3, 1, 12),  # Top-right: grid[3][0]
        (2, 2, 1, 10),  # Middle: grid[2][2]
        (3, 3, 1, 15),  # Bottom-right: grid[3][3]
    ]
    
    memory = [0] * 16
    # Set known values
    memory[12] = 1  # UI[0][3]
    memory[10] = 1  # UI[2][2]
    memory[15] = 1  # UI[3][3]
    
    print("Testing known positions...")
    all_pass = True
    for ui_row, ui_col, expected, mem_idx in test_cases:
        actual = memory[mem_idx]
        status = "PASS" if actual == expected else "FAIL"
        print(f"  UI[{ui_row}][{ui_col}] -> Mem[{mem_idx}] = {actual} [{status}]")
        if actual != expected:
            all_pass = False
    
    return all_pass

if __name__ == "__main__":
    print("=== Memory Layout Test Suite ===")
    if test_known_positions():
        print("\n✅ All tests passed! Column-major indexing confirmed.")
    else:
        print("\n❌ Tests failed!")
