# 2048 Deep Run Analysis: 92 runs, 40 moves each
set terminal pngcairo size 1200,800 font "Arial,12"
set output 'exp_009_distributions.png'

# Configure multiplot
set multiplot layout 2,2 title "2048 Deep Run Analysis: 92 runs, 40 moves each" font ",16"

# --- Plot 1: Score Distribution ---
set origin 0,0.5
set size 0.5,0.5
set title "Score Distribution"
set xlabel "Score"
set ylabel "Frequency"
set grid
set style data histogram
set style histogram clustered gap 1
set style fill solid 0.7 border -1
set boxwidth 0.9

# Calculate statistics from CSV (skip header)
set datafile separator ","
stats 'exp_009_deep_results.csv' using 2 name "SCORE" nooutput every ::1
binwidth = 20
bin(x,width) = width*floor(x/width) + width/2.0

plot 'exp_009_deep_results.csv' every ::1 using (bin($2,binwidth)):(1.0) smooth freq with boxes lc rgb "#4472C4" title "Scores", \
     SCORE_mean title sprintf("Mean = %.1f", SCORE_mean) lc rgb "red" lw 2, \
     SCORE_median title sprintf("Median = %.1f", SCORE_median) lc rgb "dark-green" lw 2 dt 2

# --- Plot 2: Timing Distribution ---
set origin 0.5,0.5
set size 0.5,0.5
set title "Timing Distribution"
set xlabel "Time (seconds)"
set ylabel "Frequency"

stats 'exp_009_deep_results.csv' using 3 name "TIME" nooutput every ::1
binwidth_time = 0.5
set xrange [TIME_min-0.5:TIME_max+0.5]

plot 'exp_009_deep_results.csv' every ::1 using (bin($3,binwidth_time)):(1.0) smooth freq with boxes lc rgb "#70AD47" title "Times", \
     TIME_mean title sprintf("Mean = %.2fs", TIME_mean) lc rgb "red" lw 2

# --- Plot 3: Score Progression ---
set origin 0,0
set size 0.5,0.5
set title "Score Progression Over Runs"
set xlabel "Run Number"
set ylabel "Score"
set xrange [0:93]
set yrange [0:*]

plot 'exp_009_deep_results.csv' every ::1 using 1:2 with points pt 7 ps 0.5 lc rgb "#4472C4" title "Individual runs", \
     'exp_009_deep_results.csv' every ::1 using 1:2 smooth bezier lw 2 lc rgb "red" title "Smoothed trend"

# --- Plot 4: Max Tile Distribution ---
set origin 0.5,0
set size 0.5,0.5
set title "Max Tile Distribution"
set xlabel "Max Tile Value"
set ylabel "Count"
set xtics ("8" 8, "16" 16, "32" 32, "64" 64, "128" 128)
set logscale x 2
set xrange [4:256]
set style data histogram
set style histogram clustered
set style fill solid 0.8 border -1

# Count occurrences manually (gnuplot limitation)
plot 'exp_009_deep_results.csv' every ::1 using 4 bins=5 with boxes lc rgb "#FF7F0E" title "Max Tiles"

unset multiplot

# Generate summary statistics file
set print "exp_009_stats.txt"
print sprintf("=== SCORE STATISTICS ===")
print sprintf("Mean: %.2f", SCORE_mean)
print sprintf("Median: %.1f", SCORE_median)
print sprintf("Std Dev: %.2f", SCORE_stddev)
print sprintf("Min: %.0f", SCORE_min)
print sprintf("Max: %.0f", SCORE_max)
print sprintf("")
print sprintf("=== TIMING STATISTICS ===")
print sprintf("Mean: %.3fs", TIME_mean)
print sprintf("Std Dev: %.3fs", TIME_stddev)
print sprintf("Min: %.1fs", TIME_min)
print sprintf("Max: %.1fs", TIME_max)