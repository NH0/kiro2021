# -- Library imports --


# -- Local imports --
import config as CONF
import utils
import Solution as S
import vns

def main():
    sol = S.Solution(CONF.file)
    print(sol.score)
    # vns.start_vns(sol)
    return 0

if __name__ == "__main__":
    main()