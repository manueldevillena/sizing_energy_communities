#!/bin/zsh

echo --------------------------
echo RUNNING CENTRAL_DUAL MODEL
echo --------------------------

python -m sizing \
    -ip example_merygrid/inputs.yml \
    -if example_merygrid/input/ \
    -m central_dual \
    -s gurobi \
    -o example_merygrid/output/central_dual \
    -v

echo --------------------------
echo EXTRACTING LOCAL PICE DATA
echo --------------------------

cp example_merygrid/output/central_dual/dual_local_exchanges_eqn_scaled.csv example_merygrid/input/prices_community_exchange.csv

echo ------------------------
echo RUNNING INDIVIDUAL MODEL
echo ------------------------

python -m sizing \
    -ip example_merygrid/inputs.yml \
    -if example_merygrid/input/ \
    -m individual \
    -s gurobi \
    -o example_merygrid/output/individual \
    -v

echo -------------------------
echo RUNNING COMPARISON SCRIPT
echo -------------------------

./compare.py
