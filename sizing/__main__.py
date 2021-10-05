import argparse
import os
import time

from . import OptimisationInputs, Central, Rural


if __name__ == "__main__":

    # Argument parsing
    parser = argparse.ArgumentParser(description="Parses the inputs for the module to run.")
    parser.add_argument('-ip', '--input_parameters', dest='input_parameters', help="YML file with several options")
    parser.add_argument('-if', '--input_files', dest='input_files', help='Path to the input files (csv files)')
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
        input_parameters=args.input_parameters,
        input_files=args.input_files,
        output_path=args.output
    )

    tac = time.time()
    if args.is_verbose:
        print(f"Input files read in {(tac - tic):.2f} seconds.")

    problem = Rural(solver=args.solver, inputs=inputs, is_debug=args.is_debug)
    # problem = Central(solver=args.solver, inputs=inputs, is_debug=args.is_debug)

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
