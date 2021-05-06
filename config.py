# Configuration file for the repo

path = "./data/"
filename = "PMP.json"
file = path + filename

C0 = 2000

# VNS parameters
class VNS:
    ## Simulated annealing
    PI = 0.3
    NB_NEIGHBORS_T0 = 10
    K_MAX = 2
    MAX_TIME = 5 # in seconds
    MAX_UNIMPROVING_ITERS = 50
    PHI = 0.8
    STEPS = 15
