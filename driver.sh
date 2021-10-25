#!/bin/zsh

python -m sizing \
    -ip example/inputs.yml \
    -if example/input/ \
    -m bilevel \
    -s cbc \
    -o example/output/ \
    -v

