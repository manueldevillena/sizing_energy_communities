import argparse
import os
import time

from . import OptimisationInputs, Central


if __name__ == "__main__":

    # Argument parsing
    parser = argparse.ArgumentParser(description="Parses the inputs for the module to run.")
    parser.add_argument('-i', '--input_options', dest='input_options', help="YML file with several options: interest_rate")
    parser.add_argument("-d", "--demand_members", dest="demand", help="Input file (csv) with the demand of the users.")
    parser.add_argument("-g", "--generation_members", dest="generation", help="Input file (csv) with the generation of the users.")
    parser.add_argument("-pgi", "--prices_import_grid_members", dest="prices_grid_import", help="Input file (csv) with the grid electricity import prices of the users.")
    parser.add_argument("-pli", "--prices_import_local_members", dest="prices_local_import", help="Input file (csv) with the local electricity import prices of the users.")
    parser.add_argument("-pge", "--prices_export_grid_members", dest="prices_grid_export", help="Input file (csv) with the grid electricity export prices of the users.")
    parser.add_argument("-ple", "--prices_export_local_members", dest="prices_local_export", help="Input file (csv) with the local electricity export prices of the users.")
    parser.add_argument("-ic", "--initial_capacity", dest="initial_capacity", help="Input file (csv) with the initial technology capacities of the users.")
    parser.add_argument("-ct", "--cost_technology", dest="cost_tech", help="Input file (csv) with the technology costs of the users.")
    parser.add_argument("-cf", "--cost_fixed", dest="cost_tech_fixed", help="Input file (csv) with the fixed running technology costs of the users.")
    parser.add_argument("-o", "--output_path", dest="output", help="Output path for the results.")
    parser.add_argument("-s", "--solver", dest="solver", help="Solver name (cbc, cplex ...)", default="cbc")
    parser.add_argument("-v", "--verbose", dest="is_verbose", action="store_true", help="Verbose mode")
    parser.add_argument("--debug", dest="is_debug", action="store_true", help="Debug mode")

    args = parser.parse_args()

    # Prepare output path
    os.makedirs(args.output, exist_ok=True)

    tic = time.time()
    # Read inputs
    inputs = OptimisationInputs(
        additional_inputs_path=args.input_options,
        demand_members_path=args.demand,
        production_members_path=args.generation,
        prices_import_grid_members_path=args.prices_grid_import,
        prices_import_local_members_path=args.prices_local_import,
        prices_export_grid_members_path=args.prices_grid_export,
        prices_export_local_members_path=args.prices_local_export,
        initial_capacity_path=args.initial_capacity,
        cost_technology_path=args.cost_tech,
        cost_technology_running_fixed_path=args.cost_tech_fixed,
        output_path=args.output
    )

    tac = time.time()
    if args.is_verbose:
        print(f"Input files read in {(tac - tic):.2f} seconds.")

    problem = Central(solver=args.solver, inputs=inputs, is_debug=args.is_debug)

    # Create problem
    tic = time.time()
    model = problem.create_model()
    tac = time.time()
    if args.is_verbose:
        print(f"Model created in {(tac - tic):.2f} seconds.")

    # Solve problem
    tic = time.time()
    results = problem.solve_model(model=model)
    tac = time.time()
    if args.is_verbose:
        print(f"Problem solved in {(tac - tic):.2f} seconds.")
