# BeamBeamTools
This project aims to merge together all the tools that can be used for Beam-Beam effect studies and its compensation in the CERN LHC and HL-LHC.

This module proposes a set of **postprocessing** functions, together with useful analysis tools.

Big acknoledgment to G. Sterbini for his input. 

We strongely recommend to use, in parallel the cl2pd package, available here: 
https://github.com/sterbini/cl2pd

This package indeed assumes that the raw data has already been downloaded. 

## Install the package
You can install the package, for instance on the SWAN terminal (www.swan.cern.ch), using:
```
pip install --user git+https://github.com/apoyet/BeamBeamTools.git
```
or to upgrade it
```
pip install --upgrade --user git+https://github.com/apoyet/BeamBeamTools.git
```
or to upgrade a fork of the project
```
pip install --upgrade --user git+https://github.com/apoyet/BeamBeamTools.git@fork_name
```

