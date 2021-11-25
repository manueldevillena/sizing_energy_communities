#!/bin/zsh

python -m sizing \
    -ip example_merygrid/inputs.yml \
    -if example_merygrid/input/ \
    -m central_dual \
    -s gurobi \
    -o example_merygrid/output/ \
    -v
