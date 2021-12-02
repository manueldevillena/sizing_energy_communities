#! /bin/python

import pandas as pd

total = pd.read_csv('example_merygrid/output/total_costs.csv',\
    header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)
imports = pd.read_csv('example_merygrid/output/imports_rec.csv',\
    header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)
exports = pd.read_csv('example_merygrid/output/exports_rec.csv',\
    header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)
prices = pd.read_csv('example_merygrid/output/dual_local_exchanges_eqn.csv',\
    header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)

for u in total.index:
    print('\nMember ' + u)

    explicit = total.loc[u][0]
    print('Explicit cost: ' + str(explicit))

    trade = imports[u].dot(prices) - exports[u].dot(prices)
    print('Trade cost: ' + str(trade[0]))
    print('Total cost: ' + str(explicit + trade[0]))
