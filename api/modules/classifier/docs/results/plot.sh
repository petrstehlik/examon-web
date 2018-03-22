metrics=("back_end_bound" "c3" "c6" "CPU_Utilization" "Mem_Utilization" "IO_Utilization" "Sys_Utilization" "front_end_bound" "ips" "jobber" "L1L2_Bound" "L3_Bound" "load_core" )

for metric in "${metrics[@]}"
do
    echo "
    set terminal svg font 'arial,13' size 800,470
    set key noenhanced
    set output 'res_$metric.svg'
    set style textbox transparent margins  1.0,  1.0 border
    set xlabel 'epoch'
    set ylabel 'error'
    set title '$metric' noenhanced
    set key top right
    plot 'err/$metric.err' t 'error of $metric' smooth cspline
    " | gnuplot
done

