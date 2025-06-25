# 2048 Down-Right Spam Distribution Analysis
set terminal pngcairo size 1200,800 font "Arial,12"
set output 'exp_008_gnuplot.png'

# Set up the plot
set title "Score Distribution: 150-Move Down-Right Spam (100 Runs)" font ",16"
set xlabel "Score"
set ylabel "Frequency"
set grid

# Style
set style data histogram
set style histogram clustered gap 1
set style fill solid 0.7 border -1
set boxwidth 0.9

# Stats from CSV
stats 'exp_008_results.csv' using 2 name "SCORE" nooutput

# Create histogram bins
set xrange [0:*]
set yrange [0:*]
binwidth = 50
bin(x,width) = width*floor(x/width) + width/2.0

# Plot histogram with statistics
plot 'exp_008_results.csv' using (bin($2,binwidth)):(1.0) smooth freq with boxes lc rgb "#4472C4" title "Score Distribution", \
     SCORE_mean title sprintf("Mean = %.1f", SCORE_mean) lc rgb "red" lw 2, \
     SCORE_median title sprintf("Median = %.1f", SCORE_median) lc rgb "dark-green" lw 2 dt 2

# Add text box with statistics
set label 1 sprintf("Statistics:\nMean: %.1f\nMedian: %.1f\nStd Dev: %.1f\nMin: %.0f\nMax: %.0f", \
    SCORE_mean, SCORE_median, SCORE_stddev, SCORE_min, SCORE_max) \
    at graph 0.7, 0.8 boxed font ",10"

# Second plot: Max tile distribution
set terminal pngcairo size 800,600 font "Arial,12"
set output 'exp_008_tiles.png'
set title "Max Tile Distribution" font ",16"
set xlabel "Max Tile Value"
set ylabel "Count"
set xtics ("32" 32, "64" 64, "128" 128, "256" 256, "512" 512)
set logscale x 2

# Reset style for bar chart
unset label
set style data histogram
set style histogram clustered
set style fill solid 0.8 border -1

# Plot max tile distribution
plot 'exp_008_results.csv' using 3 bins=5 with boxes lc rgb "#70AD47" title "Max Tiles"
