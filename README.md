- Planning tool written in python 3.9.7

- Requires solver (CPLEX, Gurobi, CBC)

- Best working on virtual environment:
    - To create it: `python3 -m venv NAME`, where `NAME` is the name you choose for the virtual environment.
    - To activate it: `source NAME/bin/activate`.

- Install requirements with pip: `pip install --upgrade pip && pip install -r requirements.txt`.

- Run the example using: 
    `
    python -m sizing \
    -ip example_merygrid/inputs.yml \
    -if example_merygrid/input/ \
    -m central_dual \
    -s gurobi \
    -o example_merygrid/output/ \
    -v
    `
- A complete help can be found with: `python sizing -h`
