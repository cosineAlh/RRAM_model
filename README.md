# RRAM Model

RRAM model by python.

## Description

This RRAM model is a python version of the Verilog-A model. We realize the basic DC and pulse tests, and included the thermal effect variation.

## Requirements

* HSPICE
* Python 3

## Simulation

### Start

Run `test.py` under folders.

## Directory

```
|-- README.md              # README file
|-- /1.0                   # version 1
    |-- /PDF               # Resistance distribution
    |-- /test              # test scripts
    |-- /v1                # v1.0
    `-- /v2                # v2.0 (final version)
|-- /2.0                   # version 2
    |-- /RRAM2_0_Beta      # Origin Hspice files
    |-- rram.py            # RRAM
    `-- test.py            # testbench
`-- /RRAM_analog           # Analog version (not tested)
```

## References

1. https://github.com/bcrafton/rram
