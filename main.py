import config as CONF
import utils

def main():
    json_obj = utils.read_json(CONF.file)
    print(json_obj['services'][1])
    return 0

if __name__ == "__main__":
    main()