import sys
from scipy.optimize import linprog
import time
import statistics
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) # Three of the methods used are deprecated

linprogs = {}

solvers = {"simplex" : {}, "highs" : {}, "highs-ds" : {}, "highs-ipm" : {}, "interior-point" : {}, "revised simplex" : {}}

# Generate an n-dimensional Klee-Minty Cube LP
def generate_kleeminty(n):
    # Objective Function
    c = [-1] * n # Maximize x1 + ... + xn

    # Constraints
    A_ub = []
    b_ub = []

    for i in range(n):
        row = [0] * n
        for j in range(i + 1):
            row[j] = 10 ** (i-j)
        A_ub.append(row)
        b_ub.append(5 * (10 ** i))

    return {"c" : c, "A_ub" : A_ub, "b_ub" : b_ub}

def solve_lps(n):
    for lp_name in linprogs.keys():
        print(f"Linear Program: {lp_name}\n")
        lp = linprogs[lp_name]
        for method in solvers.keys():
            times = []
            for _ in range(n):
                start_time = time.perf_counter()
                result = linprog(c=lp["c"],A_ub=lp["A_ub"],b_ub=lp["b_ub"],method=method,options={"presolve": False})
                end_time = time.perf_counter()
                times.append(end_time - start_time)
            solvers[method][lp_name] = [result.nit,statistics.mean(times)]
            print(f"{method}, Iterations: {result.nit}, Mean Runtime: {statistics.mean(times)}\n")

def minmax_iterations():
    max_dict = {}
    min_dict = {}
    for lp_name in linprogs.keys():
        max_dict[lp_name] = [None, 0]
        min_dict[lp_name] = [None, None]
        for method in solvers.keys():
            iters = solvers[method][lp_name][0]
            if iters > max_dict[lp_name][1]:
                max_dict[lp_name] = [method, iters]
            if not min_dict[lp_name][1] or iters < min_dict[lp_name][1]:
                min_dict[lp_name] = [method, iters]
        print(f"Max Iterations for {lp_name}:\n{max_dict[lp_name][0]} : {max_dict[lp_name][1]}")
        print(f"Min Iterations for {lp_name}:\n{min_dict[lp_name][0]} : {min_dict[lp_name][1]}\n")

def minmax_times():
    max_dict = {}
    min_dict = {}
    for lp_name in linprogs.keys():
        max_dict[lp_name] = [None, 0]
        min_dict[lp_name] = [None, None]
        for method in solvers.keys():
            time = solvers[method][lp_name][1]
            if time > max_dict[lp_name][1]:
                max_dict[lp_name] = [method, time]
            if not min_dict[lp_name][1] or time < min_dict[lp_name][1]:
                min_dict[lp_name] = [method, time]
        print(f"Max Runtime for {lp_name}:\n{max_dict[lp_name][0]} : {max_dict[lp_name][1]}")
        print(f"Min Runtime for {lp_name}:\n{min_dict[lp_name][0]} : {min_dict[lp_name][1]}\n")

def main(n):
    linprogs["Klee-Minty 3-Cube"] = generate_kleeminty(3)
    linprogs["Klee-Minty 5-Cube"] = generate_kleeminty(5)
    linprogs["Klee-Minty 7-Cube"] = generate_kleeminty(7)
    linprogs["Klee-Minty 9-Cube"] = generate_kleeminty(9) # Dimensions greater than 9 are unstable
    solve_lps(int(n))
    minmax_iterations()
    minmax_times()
    return
    
if __name__ == "__main__":
    main(sys.argv[1])