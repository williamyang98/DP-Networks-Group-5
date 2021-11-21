# %% Setup logger
import logging

file_logger = logging.FileHandler('solver_v1.log')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:%(message)s', datefmt="%H:%M:%S")
file_logger.setFormatter(formatter)

logging.basicConfig(handlers=[file_logger, console])
logging.getLogger().setLevel(logging.DEBUG)

# %% Script for testing our different solvers
from importlib import reload
import RealSnooperServer
import RealPostServer
import TestSnooperServer
import SolverV1
import PacketSniper
import time;

# fresh reload the module if we are updating it while testing
reload(SolverV1)
reload(RealSnooperServer)
reload(RealPostServer)
reload(TestSnooperServer)
reload(PacketSniper)

from RealSnooperServer import RealSnooper
from RealPostServer import RealPostServer
from TestSnooperServer import TestSnooper, OffsetGenerator
from SolverV1 import Solver_V1 as Solver
from PacketSniper import PacketSniper

# %% Startup the real snooper server
snooper = RealSnooper()
snooper.logger.setLevel(logging.INFO)
post_server = RealPostServer(SERVER_PORT=snooper.SERVER_PORT+1)

# %% Startup a test server
# snooper = TestSnooper([
#     "This is the first message\nAnd this is part of the first message",
#     "Hello world\n",
#     "This is the third message but quite long\n "*100,
#     "o"*5000,
# ])
# post_server = snooper

# snooper.offset_generator = OffsetGenerator()

# %% Run our solver against this
messages = []
sniper = PacketSniper()
startTime=time.time()
print(startTime)
while True:
    solver = Solver(snooper, sniper)
    solver.logger.setLevel(logging.DEBUG)
    
    final_msg = solver.run(sparse_guess=True)
    messages.append(final_msg)
    endTime=time.time()
    print(endTime)
    print(endTime-startTime)
    res = post_server.post_message(final_msg)
    if res < 400:
        logging.info(f"Message correct @ {solver.total_requests}")
    else:
        logging.error("Got an incorrect message")
        break
        
    if res == 205:
        break
# %%
