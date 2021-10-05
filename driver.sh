#!/bin/zsh

python -m sizing \
    -i example/input/inputs.yml \
    -d example/input/demand.csv \
    -g example/input/generation.csv \
    -pgi example/input/prices_grid_import.csv \
    -pli example/input/prices_community_import.csv \
    -pge example/input/prices_grid_export.csv \
    -ple example/input/prices_community_export.csv \
    -ic example/input/initial_capacity.csv \
    -ct example/input/cost_technology.csv \
    -cf example/input/cost_technology_running_fixed.csv \
    -s cbc \
    -o example/output/ \
    -v

