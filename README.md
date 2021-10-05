- Planning tool written in python 3.8.6

- Requires solver (CPLEX, Gurobi, CBC)

- Best working on virtual environment:
    - To create it: `python3 -m venv NAME`, where `NAME` is the name you choose for the virtual environment.
    - To activate it: `source NAME/bin/activate`.

- Install requirements with pip: `pip install --upgrade pip && pip install -r requirements.txt`.

- Run the example using: 
    `
    python -m sizing \
    -i example/input/inputs.yml \
    -d example/input/demand.csv \
    -g example/input/generation.csv \
    -pgi example/input/prices_global_import.csv \
    -pli example/input/prices_local_import.csv \
    -pge example/input/prices_global_export.csv \
    -ple example/input/prices_local_export.csv \
    -ic example/input/initial_capacity.csv \
    -ct example/input/cost_technology.csv \
    -cf example/input/cost_technology_running_fixed.csv \
    -s gurobi \
    -o example/output/ \
    -v
    `
- A complete help can be found with: `python sizing -h`
