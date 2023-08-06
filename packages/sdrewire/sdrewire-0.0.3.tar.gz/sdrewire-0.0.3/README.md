# Python tools for SDReWire

This repository contains Python tools for [SDReWire](https://github.com/randomplum/sdrewire).
Currently the command line utility `sdrewirectl` is the only utility.

Check if SDReWire devices are available:
```
$ sdrewire list
Found the following devices:
Device: 101, Manufacturer: SliwaIO, Product: SDReWire v1.0, Serial: SDRW00004
Device: 104, Manufacturer: SliwaIO, Product: SDReWire v1.0, Serial: SDRW00003
```

Muxing can be controlled using:
```
$ sdrewire --serial SDRW00003 sdmux --ts
$ sdrewire --serial SDRW00003 sdmux --status
SD mux connected to: TS
$ sdrewire --serial SDRW00003 sdmux --dut
$ sdrewire --serial SDRW00003 sdmux --status
SD mux connected to: DUT
```
