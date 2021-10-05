\* Source Pyomo model name=unknown *\

min 
objective_eqn:
+17.351433344597091 annual_electricity_bills
-17.351433344597091 annual_electricity_revenue
+17.351433344597091 annual_investment_costs
+17.351433344597091 annual_operational_costs

s.t.

c_e__annual_investments_eqn_:
+1 annual_investment_costs
= 0

c_e__annual_operational_costs_eqn_:
+1 annual_operational_costs
= 0

c_e__annual_electricity_bills_eqn_:
+1 annual_electricity_bills
-0.13 imports_rec(2017_04_01_09_00_00_00_00_Member1)
-0.13 imports_rec(2017_04_01_09_00_00_00_00_Member2)
-0.13 imports_rec(2017_04_01_09_15_00_00_00_Member1)
-0.13 imports_rec(2017_04_01_09_15_00_00_00_Member2)
-0.22 imports_retailer(2017_04_01_09_00_00_00_00_Member1)
-0.20000000000000001 imports_retailer(2017_04_01_09_00_00_00_00_Member2)
-0.22 imports_retailer(2017_04_01_09_15_00_00_00_Member1)
-0.20000000000000001 imports_retailer(2017_04_01_09_15_00_00_00_Member2)
= 0

c_e__annual_electricity_revenue_eqn_:
+1 annual_electricity_revenue
-0.14000000000000001 exports_rec(2017_04_01_09_00_00_00_00_Member1)
-0.14000000000000001 exports_rec(2017_04_01_09_00_00_00_00_Member2)
-0.14000000000000001 exports_rec(2017_04_01_09_15_00_00_00_Member1)
-0.14000000000000001 exports_rec(2017_04_01_09_15_00_00_00_Member2)
-0.040000000000000001 exports_retailer(2017_04_01_09_00_00_00_00_Member1)
-0.029999999999999999 exports_retailer(2017_04_01_09_00_00_00_00_Member2)
-0.040000000000000001 exports_retailer(2017_04_01_09_15_00_00_00_Member1)
-0.029999999999999999 exports_retailer(2017_04_01_09_15_00_00_00_Member2)
= 0

c_e__technology_generation_eqn(2017_04_01_09_00_00_00_00_Member1)_:
-1 battery_outflow(2017_04_01_09_00_00_00_00_Member1)
+1 electricity_produced(2017_04_01_09_00_00_00_00_Member1)
= 0

c_e__technology_generation_eqn(2017_04_01_09_00_00_00_00_Member2)_:
-1 battery_outflow(2017_04_01_09_00_00_00_00_Member2)
+1 electricity_produced(2017_04_01_09_00_00_00_00_Member2)
= 0

c_e__technology_generation_eqn(2017_04_01_09_15_00_00_00_Member1)_:
-1 battery_outflow(2017_04_01_09_15_00_00_00_Member1)
+1 electricity_produced(2017_04_01_09_15_00_00_00_Member1)
-0.20000000000000001 optimal_capacity(Member1_p)
= 0

c_e__technology_generation_eqn(2017_04_01_09_15_00_00_00_Member2)_:
-1 battery_outflow(2017_04_01_09_15_00_00_00_Member2)
+1 electricity_produced(2017_04_01_09_15_00_00_00_Member2)
-0.23999999999999999 optimal_capacity(Member2_p)
= 0

c_u__technology_consumption_eqn(2017_04_01_09_00_00_00_00_Member1)_:
+1 battery_inflow(2017_04_01_09_00_00_00_00_Member1)
-1 electricity_consumed(2017_04_01_09_00_00_00_00_Member1)
<= 0

c_u__technology_consumption_eqn(2017_04_01_09_00_00_00_00_Member2)_:
+1 battery_inflow(2017_04_01_09_00_00_00_00_Member2)
-1 electricity_consumed(2017_04_01_09_00_00_00_00_Member2)
<= 0

c_u__technology_consumption_eqn(2017_04_01_09_15_00_00_00_Member1)_:
+1 battery_inflow(2017_04_01_09_15_00_00_00_Member1)
-1 electricity_consumed(2017_04_01_09_15_00_00_00_Member1)
<= 0

c_u__technology_consumption_eqn(2017_04_01_09_15_00_00_00_Member2)_:
+1 battery_inflow(2017_04_01_09_15_00_00_00_Member2)
-1 electricity_consumed(2017_04_01_09_15_00_00_00_Member2)
<= 0

c_e__state_of_charge_eqn(2017_04_01_09_00_00_00_00_Member1)_:
+1 battery_soc(2017_04_01_09_00_00_00_00_Member1)
-1 battery_soc(2017_04_01_09_15_00_00_00_Member1)
= 0

c_e__state_of_charge_eqn(2017_04_01_09_00_00_00_00_Member2)_:
+1 battery_soc(2017_04_01_09_00_00_00_00_Member2)
-1 battery_soc(2017_04_01_09_15_00_00_00_Member2)
= 0

c_e__state_of_charge_eqn(2017_04_01_09_15_00_00_00_Member1)_:
+0.94999999999999996 battery_inflow(2017_04_01_09_15_00_00_00_Member1)
-1.0526315789473684 battery_outflow(2017_04_01_09_15_00_00_00_Member1)
-1 battery_soc(2017_04_01_09_00_00_00_00_Member1)
+1 battery_soc(2017_04_01_09_15_00_00_00_Member1)
= 0

c_e__state_of_charge_eqn(2017_04_01_09_15_00_00_00_Member2)_:
+0.94999999999999996 battery_inflow(2017_04_01_09_15_00_00_00_Member2)
-1.0526315789473684 battery_outflow(2017_04_01_09_15_00_00_00_Member2)
-1 battery_soc(2017_04_01_09_00_00_00_00_Member2)
+1 battery_soc(2017_04_01_09_15_00_00_00_Member2)
= 0

c_u__state_of_charge_limit_eqn(2017_04_01_09_00_00_00_00_Member1)_:
+1 battery_soc(2017_04_01_09_00_00_00_00_Member1)
-1 optimal_capacity(Member1_b)
<= 0

c_u__state_of_charge_limit_eqn(2017_04_01_09_00_00_00_00_Member2)_:
+1 battery_soc(2017_04_01_09_00_00_00_00_Member2)
-1 optimal_capacity(Member2_b)
<= 0

c_u__state_of_charge_limit_eqn(2017_04_01_09_15_00_00_00_Member1)_:
+1 battery_soc(2017_04_01_09_15_00_00_00_Member1)
-1 optimal_capacity(Member1_b)
<= 0

c_u__state_of_charge_limit_eqn(2017_04_01_09_15_00_00_00_Member2)_:
+1 battery_soc(2017_04_01_09_15_00_00_00_Member2)
-1 optimal_capacity(Member2_b)
<= 0

c_u__limit_inflow_eqn(2017_04_01_09_00_00_00_00_Member1)_:
+1 battery_inflow(2017_04_01_09_00_00_00_00_Member1)
-0.33333333333333331 optimal_capacity(Member1_b)
<= 0

c_u__limit_inflow_eqn(2017_04_01_09_00_00_00_00_Member2)_:
+1 battery_inflow(2017_04_01_09_00_00_00_00_Member2)
-0.33333333333333331 optimal_capacity(Member2_b)
<= 0

c_u__limit_inflow_eqn(2017_04_01_09_15_00_00_00_Member1)_:
+1 battery_inflow(2017_04_01_09_15_00_00_00_Member1)
-0.33333333333333331 optimal_capacity(Member1_b)
<= 0

c_u__limit_inflow_eqn(2017_04_01_09_15_00_00_00_Member2)_:
+1 battery_inflow(2017_04_01_09_15_00_00_00_Member2)
-0.33333333333333331 optimal_capacity(Member2_b)
<= 0

c_u__limit_outflow_eqn(2017_04_01_09_00_00_00_00_Member1)_:
+1 battery_outflow(2017_04_01_09_00_00_00_00_Member1)
-0.33333333333333331 optimal_capacity(Member1_b)
<= 0

c_u__limit_outflow_eqn(2017_04_01_09_00_00_00_00_Member2)_:
+1 battery_outflow(2017_04_01_09_00_00_00_00_Member2)
-0.33333333333333331 optimal_capacity(Member2_b)
<= 0

c_u__limit_outflow_eqn(2017_04_01_09_15_00_00_00_Member1)_:
+1 battery_outflow(2017_04_01_09_15_00_00_00_Member1)
-0.33333333333333331 optimal_capacity(Member1_b)
<= 0

c_u__limit_outflow_eqn(2017_04_01_09_15_00_00_00_Member2)_:
+1 battery_outflow(2017_04_01_09_15_00_00_00_Member2)
-0.33333333333333331 optimal_capacity(Member2_b)
<= 0

c_e__energy_balance_eqn(2017_04_01_09_00_00_00_00_Member1)_:
+1 electricity_consumed(2017_04_01_09_00_00_00_00_Member1)
-1 electricity_produced(2017_04_01_09_00_00_00_00_Member1)
+1 exports_rec(2017_04_01_09_00_00_00_00_Member1)
+1 exports_retailer(2017_04_01_09_00_00_00_00_Member1)
-1 imports_rec(2017_04_01_09_00_00_00_00_Member1)
-1 imports_retailer(2017_04_01_09_00_00_00_00_Member1)
= -2.1000000000000001

c_e__energy_balance_eqn(2017_04_01_09_00_00_00_00_Member2)_:
+1 electricity_consumed(2017_04_01_09_00_00_00_00_Member2)
-1 electricity_produced(2017_04_01_09_00_00_00_00_Member2)
+1 exports_rec(2017_04_01_09_00_00_00_00_Member2)
+1 exports_retailer(2017_04_01_09_00_00_00_00_Member2)
-1 imports_rec(2017_04_01_09_00_00_00_00_Member2)
-1 imports_retailer(2017_04_01_09_00_00_00_00_Member2)
= 0

c_e__energy_balance_eqn(2017_04_01_09_15_00_00_00_Member1)_:
+1 electricity_consumed(2017_04_01_09_15_00_00_00_Member1)
-1 electricity_produced(2017_04_01_09_15_00_00_00_Member1)
+1 exports_rec(2017_04_01_09_15_00_00_00_Member1)
+1 exports_retailer(2017_04_01_09_15_00_00_00_Member1)
-1 imports_rec(2017_04_01_09_15_00_00_00_Member1)
-1 imports_retailer(2017_04_01_09_15_00_00_00_Member1)
= -3.2000000000000002

c_e__energy_balance_eqn(2017_04_01_09_15_00_00_00_Member2)_:
+1 electricity_consumed(2017_04_01_09_15_00_00_00_Member2)
-1 electricity_produced(2017_04_01_09_15_00_00_00_Member2)
+1 exports_rec(2017_04_01_09_15_00_00_00_Member2)
+1 exports_retailer(2017_04_01_09_15_00_00_00_Member2)
-1 imports_rec(2017_04_01_09_15_00_00_00_Member2)
-1 imports_retailer(2017_04_01_09_15_00_00_00_Member2)
= 0

c_e__local_exchanges_eqn(2017_04_01_09_00_00_00_00)_:
+1 exports_rec(2017_04_01_09_00_00_00_00_Member1)
+1 exports_rec(2017_04_01_09_00_00_00_00_Member2)
-1 imports_rec(2017_04_01_09_00_00_00_00_Member1)
-1 imports_rec(2017_04_01_09_00_00_00_00_Member2)
= 0

c_e__local_exchanges_eqn(2017_04_01_09_15_00_00_00)_:
+1 exports_rec(2017_04_01_09_15_00_00_00_Member1)
+1 exports_rec(2017_04_01_09_15_00_00_00_Member2)
-1 imports_rec(2017_04_01_09_15_00_00_00_Member1)
-1 imports_rec(2017_04_01_09_15_00_00_00_Member2)
= 0

c_u__limit_exports_eqn(2017_04_01_09_00_00_00_00_Member1)_:
-1 electricity_produced(2017_04_01_09_00_00_00_00_Member1)
+1 exports_rec(2017_04_01_09_00_00_00_00_Member1)
+1 exports_retailer(2017_04_01_09_00_00_00_00_Member1)
<= 0

c_u__limit_exports_eqn(2017_04_01_09_00_00_00_00_Member2)_:
-1 electricity_produced(2017_04_01_09_00_00_00_00_Member2)
+1 exports_rec(2017_04_01_09_00_00_00_00_Member2)
+1 exports_retailer(2017_04_01_09_00_00_00_00_Member2)
<= 0

c_u__limit_exports_eqn(2017_04_01_09_15_00_00_00_Member1)_:
-1 electricity_produced(2017_04_01_09_15_00_00_00_Member1)
+1 exports_rec(2017_04_01_09_15_00_00_00_Member1)
+1 exports_retailer(2017_04_01_09_15_00_00_00_Member1)
<= 0

c_u__limit_exports_eqn(2017_04_01_09_15_00_00_00_Member2)_:
-1 electricity_produced(2017_04_01_09_15_00_00_00_Member2)
+1 exports_rec(2017_04_01_09_15_00_00_00_Member2)
+1 exports_retailer(2017_04_01_09_15_00_00_00_Member2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= optimal_capacity(Member1_b) <= 1000
   0 <= optimal_capacity(Member1_p) <= 1000
   0 <= optimal_capacity(Member2_b) <= 1000
   0 <= optimal_capacity(Member2_p) <= 1000
   0 <= electricity_produced(2017_04_01_09_00_00_00_00_Member1) <= +inf
   0 <= electricity_produced(2017_04_01_09_00_00_00_00_Member2) <= +inf
   0 <= electricity_produced(2017_04_01_09_15_00_00_00_Member1) <= +inf
   0 <= electricity_produced(2017_04_01_09_15_00_00_00_Member2) <= +inf
   0 <= electricity_consumed(2017_04_01_09_00_00_00_00_Member1) <= +inf
   0 <= electricity_consumed(2017_04_01_09_00_00_00_00_Member2) <= +inf
   0 <= electricity_consumed(2017_04_01_09_15_00_00_00_Member1) <= +inf
   0 <= electricity_consumed(2017_04_01_09_15_00_00_00_Member2) <= +inf
   0 <= imports_retailer(2017_04_01_09_00_00_00_00_Member1) <= +inf
   0 <= imports_retailer(2017_04_01_09_00_00_00_00_Member2) <= +inf
   0 <= imports_retailer(2017_04_01_09_15_00_00_00_Member1) <= +inf
   0 <= imports_retailer(2017_04_01_09_15_00_00_00_Member2) <= +inf
   0 <= imports_rec(2017_04_01_09_00_00_00_00_Member1) <= +inf
   0 <= imports_rec(2017_04_01_09_00_00_00_00_Member2) <= +inf
   0 <= imports_rec(2017_04_01_09_15_00_00_00_Member1) <= +inf
   0 <= imports_rec(2017_04_01_09_15_00_00_00_Member2) <= +inf
   0 <= exports_retailer(2017_04_01_09_00_00_00_00_Member1) <= +inf
   0 <= exports_retailer(2017_04_01_09_00_00_00_00_Member2) <= +inf
   0 <= exports_retailer(2017_04_01_09_15_00_00_00_Member1) <= +inf
   0 <= exports_retailer(2017_04_01_09_15_00_00_00_Member2) <= +inf
   0 <= exports_rec(2017_04_01_09_00_00_00_00_Member1) <= +inf
   0 <= exports_rec(2017_04_01_09_00_00_00_00_Member2) <= +inf
   0 <= exports_rec(2017_04_01_09_15_00_00_00_Member1) <= +inf
   0 <= exports_rec(2017_04_01_09_15_00_00_00_Member2) <= +inf
   0 <= battery_outflow(2017_04_01_09_00_00_00_00_Member1) <= +inf
   0 <= battery_outflow(2017_04_01_09_00_00_00_00_Member2) <= +inf
   0 <= battery_outflow(2017_04_01_09_15_00_00_00_Member1) <= +inf
   0 <= battery_outflow(2017_04_01_09_15_00_00_00_Member2) <= +inf
   0 <= battery_inflow(2017_04_01_09_00_00_00_00_Member1) <= +inf
   0 <= battery_inflow(2017_04_01_09_00_00_00_00_Member2) <= +inf
   0 <= battery_inflow(2017_04_01_09_15_00_00_00_Member1) <= +inf
   0 <= battery_inflow(2017_04_01_09_15_00_00_00_Member2) <= +inf
   0 <= battery_soc(2017_04_01_09_00_00_00_00_Member1) <= +inf
   0 <= battery_soc(2017_04_01_09_00_00_00_00_Member2) <= +inf
   0 <= battery_soc(2017_04_01_09_15_00_00_00_Member1) <= +inf
   0 <= battery_soc(2017_04_01_09_15_00_00_00_Member2) <= +inf
   0 <= annual_investment_costs <= +inf
   0 <= annual_operational_costs <= +inf
   0 <= annual_electricity_bills <= +inf
   0 <= annual_electricity_revenue <= +inf
end
