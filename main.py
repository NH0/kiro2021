# -- Library imports --


# -- Local imports --
import config as CONF
import utils
import Solution as S
import vns

def main():
    sol = S.Solution(CONF.file)
    sol.compute_admissible()
    sol.contrainte_par_itin()
    sol.greedy_2()
    sol.export()
    # vns.start_vns(sol)
    return 0

if __name__ == "__main__":
    main()




