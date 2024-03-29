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
    sol.score
    sol.read_sol("sol_PMP.json")
    sol, score = vns.start_vns(sol)
    # sol.greedy_2()
    sol.export()
    print('\n', sol.score)
    return 0

if __name__ == "__main__":
    main()




