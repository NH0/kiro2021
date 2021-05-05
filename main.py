# -- Library imports --


# -- Local imports --
import config as CONF
import utils
import Solution as S
import vns

def main():
    json_obj = utils.read_json(CONF.file)
    sol = S.Solution(CONF.file)
    vns.start_vns(sol)
    return 0

if __name__ == "__main__":
    main()