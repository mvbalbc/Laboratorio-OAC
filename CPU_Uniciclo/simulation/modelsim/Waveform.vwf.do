vlog -work work Waveform.vwf.vtvsim -novopt -c -t 1ps -L cycloneive_ver -L altera_ver -L altera_mf_ver -L 220model_ver -L sgate work.riscv_top_vlg_vec_tst -voptargs="+acc"
add wave /*
run -all
