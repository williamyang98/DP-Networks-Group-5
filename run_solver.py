# %% Script for testing our different solvers
from RealSnooperServer import RealSnooper
from TestSnooperServer import TestSnooper

# fresh reload the module if we are updating it while testing
from importlib import reload
import SolverV1
reload(SolverV1)

from SolverV1 import Solver_V1 as Solver

# %% Startup the real snooper server
snooper = RealSnooper()

# %% Startup a test server
snooper = TestSnooper([
    "This is the first message\nAnd this is part of the first message",
    "Hello world\n",
    "This is the third message but quite long\n "*100,
])

# %% Run our solver against this
messages = []
sniping_errors = []

while True:
    solver = Solver(snooper)
    # 60% of the time we have a snipe offset of 1
    solver.SNIPE_OFFSET = 1

    solver.PRINT_INFO = True
    solver.PRINT_DEBUG = True
    
    final_msg = solver.run()
    messages.append(final_msg)
    sniping_errors.extend(solver.snipe_errors)

    res = snooper.post_message(final_msg)
    if res < 400:
        print("[SUCCESS] Message correct\n\n")
    else:
        print("[ERROR] Got an incorrect message\n\n")
        break
        
    if res == 205:
        break

# %% Visualise the sniping errors
import matplotlib.pyplot as plt
import numpy as np

sniping_errors = np.array(sniping_errors)
sniping_success_rate = np.sum(sniping_errors == 0) / len(sniping_errors)
print(f"sniping_success_rate={sniping_success_rate*100:.2f}%")
print(np.mean(sniping_errors), np.std(sniping_errors))
plt.hist(sniping_errors)
