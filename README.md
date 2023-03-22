# Maestro-dataflow

## Setup docker
```
cd docker
bash build.sh
bash run.sh
cd ws && conda activate maestro-env
```
## Generate different dataflows (ws, os, nlr) of 2D PE array
```
python3 gen_2darray_dataflows.py
```
The generated dataflows and Maestro outputs are in `artifacts` folder
