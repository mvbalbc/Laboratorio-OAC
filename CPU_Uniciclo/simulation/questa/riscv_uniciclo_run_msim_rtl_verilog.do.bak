transcript on
if {[file exists rtl_work]} {
	vdel -lib rtl_work -all
}
vlib rtl_work
vmap work rtl_work

vlog  -work work +incdir+/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo {/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo/riscv_top.v}
vlog  -work work +incdir+/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo {/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo/control.v}
vlog  -work work +incdir+/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo {/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo/alu_control.v}
vlog  -work work +incdir+/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo {/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo/alu.v}
vlog  -work work +incdir+/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo {/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo/reg_file.v}
vlog  -work work +incdir+/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo {/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo/imm_gen.v}
vlog  -work work +incdir+/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo {/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo/inst_mem.v}
vlog  -work work +incdir+/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo {/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo/data_mem.v}

vlog  -work work +incdir+/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo {/home/samuel-cds/Documentos/Faculdade/OAC/Laboratorio-OAC/CPU_Uniciclo/tb_riscv_top.v}

vsim -t 1ps -L altera_ver -L lpm_ver -L sgate_ver -L altera_mf_ver -L altera_lnsim_ver -L cyclonev_ver -L cyclonev_hssi_ver -L cyclonev_pcie_hip_ver -L rtl_work -L work -voptargs="+acc"  tb_riscv_top

add wave *
view structure
view signals
run -all
