.title <PULSE_RRAM_SET>

*****************Important Note*************************
*This dynamic model reproduces AC switching behaviors
*by simulating pulse voltage operations using
*transient mode of HSPICE simulation.
********************************************************

.hdl "RRAM_v_3_1.va"
.option converge = 0
.option RUNLVL = 6
.option METHOD=gear
.option gmindc=1e-14
.option INGOLD=1
.option POST


.param VDD = 1.5
.param edge = 10ns
.param width = 50ns
.param total = 120ns


************RRAM_SET Cell*************************
.subckt RRAM_SET p1 p2 
X1 p1 p2 RRAM_v_3_1 Cv0=0.1    **Cv0 is initial conditions for SET, you can add other modified parameters.
.ends RRAM_SET
****************************************************


X_RRAM 1 0 RRAM_SET

Vin 1 0 PULSE 0.1V VDD 0 edge edge width total

.tran 0.1ns 14.4us

.print PAR('-I(Vin)')

.end

