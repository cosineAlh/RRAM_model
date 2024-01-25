1T1R testbench

** Options **
.option ingold=1
.option post=2
.temp 25

** Load models **
.include '32nm_bulk.pm'
.hdl 'rram.va'

** Parameters **
.param tr=10ps          $ Voltage pulse rise time
.param tf=10ps          $ Voltage pulse fall time
.param WL_SET=3.0V		$ WL SET voltage amplitude
.param BL_SET=2.0V		$ BL SET voltage amplitude
.param WL_RESET=2.9V  	$ WL RESET voltage amplitude
.param SL_RESET=2.0V	$ SL RESET voltage amplitude 
.param SET_PULSE=5ns    $ SET pulse width
.param SET_START=2ns    $ SET operation delay
.param RESET_PULSE=5ns  $ RESET pulse width
.param RESET_START='SET_START+5n+SET_PULSE' $ RESET operation delay
.param T_FINAL='RESET_START+RESET_PULSE+5n' $ Final simulation time
.param vsweep_min=-2V vsweep_max=2V         $ PWL voltage amplitude

** RRAM cell **
X1  BL  0  RRAM  gap_ini = 1.4e-9   $ RRAM (using gap_ini to choose HRS/LRS)
$M1  Nb  WL  0  0    nmos    w=100n  l=32n   $ Transistor

** Voltage **
$V_WL_SET    WL  0   PULSE (0V WL_SET   'SET_START-1n'   tr  tf  'SET_PULSE+2n'   T_FINAL)
$V_WL_RESET  WL2 0   PULSE (0V WL_RESET 'RESET_START-1n' tr  tf  'RESET_PULSE+2n' T_FINAL)
$V_BL_SET    BL  0   PULSE (0V BL_SET   'SET_START'      tr  tf  SET_PULSE        T_FINAL)
$V_SL_RESET  SL  0   PULSE (0V SL_RESET 'RESET_START'    tr  tf  RESET_PULSE      T_FINAL)
** ------------- **
$Vin BL 0 PWL(0s 0V 5ns vsweep_max 15ns vsweep_min 20ns 0V) R
$Vin BL 0 PWL(0s 0V 100us vsweep_max 200us 0V) $set
$Vin BL 0 PWL(0s 0V 100us vsweep_min 200us 0V) $reset
V_BL_SET BL 0 PULSE (0V 1.8V 2ns 10ps 10ps 5ns 15ns)

** Transient **
.tran 1ps 15ns
.print V(BL) I(V_BL_SET)
.print PAR('abs(V(BL)/I(V_BL_SET))')
** ------------- **
$.print PAR('-I(Vin)') V(BL) PAR('log10(abs(I(Vin)))') PAR('abs(V(BL)/I(Vin))')
$.print V(X1.gap_out) V(X1.R_out)
$.probe V(X1.temp_out)
.end
