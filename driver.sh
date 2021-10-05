#!/bin/zsh

python -m sizing \
    -ip example/inputs.yml \
    -if example/input/ \
    -s cbc \
    -o example/output/ \
    -v

