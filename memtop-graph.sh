#!/bin/bash
# Graphs creator for memtop.py. 
# This is kind of a wrapper around two gnuplot scripts (incorporated).
# The script takes one optional argument - filename with memtop log,
# if no file given, it expects memtop.log in current dir.
# More info: http://code.google.com/p/memtop/
# v.1 (25 May 2012)

if [[ ${#1} -ge 1 && -f $1 ]]; then
	logfile=$1
elif [[ -f memtop.log ]];then
	logfile=memtop.log
elif [[ ${#1} -eq 0 ]]; then
	echo "No input log file given"
	exit 1
else
	echo "File $1 not found"
	exit 1
fi

echo "Input file: " $logfile

echo "Creating:   " PgInOut.png
gnuplot > PgInOut.png << EOS1


reset
set terminal png
#set the background color here
set object 1 rectangle from screen 0,0 to screen 1,1 fillcolor rgb"#f9f9f9" behind

set xdata time
set timefmt "%d/%m/%Y %H:%M:%S"
set format x "%d/%m %H:%M"
#set xlabel "time"
set xtics rotate

set ylabel "Pages / second"
#set yrange [0:150]

set title "Paging In / Out"
#set key reverse Left outside
set grid

# possible styles f.e.: lines, points, linespoints, impulses, dots, steps,
set style data lines

plot "$logfile" using 1:6 title "PgIn", \
"" using 1:7 title "PgOut"


EOS1


#####################################################

echo "Creating:   " MemStat.png
gnuplot > MemStat.png << EOS2


reset
set terminal png
#set the background color here
set object 1 rectangle from screen 0,0 to screen 1,1 fillcolor rgb"#f9f9f9" behind

set xdata time
set timefmt "%d/%m/%Y %H:%M:%S"
set format x "%d/%m %H:%M"
#set xlabel "time"
set xtics rotate

set key outside
set key below
set key horizontal 

set ylabel "% of utlization"
#set yrange [0:150]

set title "RAM & SWAP Utilization" 
#set key reverse Left outside
set grid

# possible styles f.e.: lines, points, linespoints, impulses, dots, steps,
set style data lines

plot "$logfile" using 1:3 title "Writeable", \
"" using 1:4 title "RAM", \
"" using 1:5 title "SWAP"


EOS2
