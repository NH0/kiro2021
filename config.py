# Configuration file for the repo

path = "./data/"
filename = "test_instance1.json"
file = path + filename

# VNS parameters
class VNS:
    ## Simulated annealing
    PI = 0.3
    NB_NEIGHBORS_T0 = 20
    K_MAX = 3
    MAX_TIME = 500 # in seconds
    MAX_UNIMPROVING_ITERS = 50
    PHI = 0.8
    STEPS = 15
