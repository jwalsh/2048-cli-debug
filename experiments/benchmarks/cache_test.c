#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define SIZE 4
#define ITERATIONS 1000000

// Simulate the column-major grid
int grid[SIZE][SIZE];

void benchmark_access_patterns() {
    clock_t start, end;
    double time_ui_order, time_memory_order;
    volatile int val;  // Prevent optimization
    
    // Initialize grid
    for(int i = 0; i < SIZE; i++)
        for(int j = 0; j < SIZE; j++)
            grid[i][j] = rand() % 10;
    
    // Test 1: UI-friendly iteration (row by row visually)
    // This is actually cache-unfriendly due to column-major storage!
    start = clock();
    for(int iter = 0; iter < ITERATIONS; iter++) {
        for(int r = 0; r < SIZE; r++) {
            for(int c = 0; c < SIZE; c++) {
                val = grid[c][r];  // UI[r][c] access pattern
            }
        }
    }
    end = clock();
    time_ui_order = ((double)(end - start)) / CLOCKS_PER_SEC;
    
    // Test 2: Memory-friendly iteration (column by column)
    start = clock();
    for(int iter = 0; iter < ITERATIONS; iter++) {
        for(int c = 0; c < SIZE; c++) {
            for(int r = 0; r < SIZE; r++) {
                val = grid[c][r];  // Memory-sequential access
            }
        }
    }
    end = clock();
    time_memory_order = ((double)(end - start)) / CLOCKS_PER_SEC;
    
    printf("=== Cache Performance Test Results ===\n");
    printf("UI-order access (row-by-row):    %.3f seconds\n", time_ui_order);
    printf("Memory-order access (col-by-col): %.3f seconds\n", time_memory_order);
    printf("Performance ratio: %.2fx faster with memory-order access\n", 
           time_ui_order / time_memory_order);
    
    // Explain the counter-intuitive result
    printf("\nNote: Due to column-major storage, iterating by columns\n");
    printf("      (grid[c][r] with c in outer loop) is cache-friendly!\n");
}

int main() {
    benchmark_access_patterns();
    return 0;
}
