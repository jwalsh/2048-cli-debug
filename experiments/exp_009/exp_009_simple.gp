# Simple histogram of scores
set terminal pngcairo size 800,600 font "Arial,12"
set output 'exp_009_score_dist.png'
set title "Score Distribution (92 runs, 40 moves each)"
set xlabel "Score"
set ylabel "Frequency"
set grid
set datafile separator ","

# Create histogram
set style data histogram
set style histogram clustered gap 1
set style fill solid 0.7 border -1
binwidth = 50
bin(x,width) = width*floor(x/width) + width/2.0
set boxwidth binwidth*0.9

plot '../experiments/exp_009/exp_009_deep_results.csv' every ::1 using (bin($2,binwidth)):(1.0) smooth freq with boxes lc rgb "#4472C4" title "Scores"
