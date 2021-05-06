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
    sol.greedy()
    sol.score
    sol, score = vns.start_vns(sol)
    # print(score)
    sol.export()
    print('\n', sol.pire_trains)
    return 0

if __name__ == "__main__":
    main()




