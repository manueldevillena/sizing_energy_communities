#! /bin/python
import pandas as pd

central_total = pd.read_csv('example_merygrid/output/central_dual/total_costs.csv', squeeze=True,
                            header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)
central_imports = pd.read_csv('example_merygrid/output/central_dual/imports_rec.csv', squeeze=True,
                              header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)
central_exports = pd.read_csv('example_merygrid/output/central_dual/exports_rec.csv', squeeze=True,
                              header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)
central_prices = pd.read_csv('example_merygrid/output/central_dual/dual_local_exchanges_eqn_scaled.csv', squeeze=True,
                             header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)

individual_total = pd.read_csv('example_merygrid/output/individual/total_costs.csv', squeeze=True,
                               header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)

isolated_total = pd.read_csv('example_merygrid/output/isolated/total_costs.csv', squeeze=True,
                             header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)

for u in central_total.index:
    print(f'\nMember {u}')

    central_explicit = central_total[u]
    #print('Explicit cost: ' + str(central_explicit))

    central_trade = central_imports[u].dot(central_prices) - central_exports[u].dot(central_prices)
    central_dual_cost = central_explicit + central_trade
    #print('Trade cost: ' + str(central_trade[0]))
    print(f'{central_dual_cost = :.4f}')

    individual_cost = individual_total[u]
    print(f'{individual_cost = :.4f}')

    isolated_cost = isolated_total[u]
    print(f'{isolated_cost = :.4f}')
