#! /bin/python

import pandas as pd

central_total = pd.read_csv('example_merygrid/output/central_dual/total_costs.csv',\
    header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)
central_imports = pd.read_csv('example_merygrid/output/central_dual/imports_rec.csv',\
    header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)
central_exports = pd.read_csv('example_merygrid/output/central_dual/exports_rec.csv',\
    header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)
central_prices = pd.read_csv('example_merygrid/output/central_dual/dual_local_exchanges_eqn_scaled.csv',\
    header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)

individual_total = pd.read_csv('example_merygrid/output/individual/total_costs.csv',\
    header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)

isolated_total = pd.read_csv('example_merygrid/output/isolated/total_costs.csv',\
    header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)

for u in central_total.index:
    print('\nMember ' + u)

    central_explicit = central_total.loc[u][0]
    #print('Explicit cost: ' + str(central_explicit))

    central_trade = central_imports[u].dot(central_prices) - central_exports[u].dot(central_prices)
    #print('Trade cost: ' + str(central_trade[0]))
    print('central_dual cost: ' + str(central_explicit + central_trade[0]))

    individual_explicit = individual_total.loc[u][0]
    print('individual cost: ' + str(individual_explicit))

    isolated_explicit = isolated_total.loc[u][0]
    print('isolated cost: ' + str(isolated_explicit))
