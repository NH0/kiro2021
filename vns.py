import logging
import random
import time
import math
import copy

import config as CONF


def find_t0(solution0, pi=CONF.VNS.PI, number_of_neighbors=CONF.VNS.NB_NEIGHBORS_T0):
    score0 = solution0.score
    medium_score = 0
    for i in range(number_of_neighbors):
        # MAKE A NEIGHBOR
        # medium_score += int(neighbor.score)
        pass
    medium_score = medium_score / number_of_neighbors
    delta_f = medium_score - score0

    return - delta_f / math.log(pi)


def v(solution, k=0):
    # RETURN A NEIGHBOR
    # THE STRUCT OF THE NEIGHBOR DEPENDS ON K
    return solution


def start_vns(solution, k_max=CONF.VNS.K_MAX, max_time=CONF.VNS.MAX_TIME,
              max_unimproving_iters=CONF.VNS.MAX_UNIMPROVING_ITERS, phi=CONF.VNS.PHI,
              steps=CONF.VNS.STEPS):
    best_solution = copy.deepcopy(solution)
    current_solution = copy.deepcopy(solution)
    t0 = find_t0(solution)
    temperature = t0
    print("----- Starting VNS ! -----")
    logging.debug("Temperature_0 {}".format(t0))
    scores = []
    start_time = time.time()
    iteration = 0
    unimproving_iterations = 0
    while (time.time() - start_time) < max_time and unimproving_iterations < max_unimproving_iters:
        k = 0
        print("Current VNS score : {}".format(best_solution.score))
        logging.info("Starting new VNS loop {}\t"
                     "Temperature is {:.2e}\t"
                     "Execution time is {:.2f}\t"
                     "Not increased best for {} interations".format(
                         iteration,
                         temperature,
                         time.time() - start_time,
                         unimproving_iterations))
        while k < k_max:
            solution_prim = v(copy.deepcopy(current_solution), k)
            # HERE IT MAY BE NECESSARY TO MAKE THE NEIGHBOR ADMISSIBLE (REPAIR)
            # OR TO OPTIMIZE IT LOCALLY
            # if not solution_prim.is_admissible():
            #     raise RuntimeError
            # solution_prim.optimize_locally()
            scores.append(solution_prim.score)

            logging.info("VNS score: {}\tCurrent score was {}\tBest score is {}\tk: {}\tTime {:.1f}".format(
                scores[-1],
                current_solution.score,
                best_solution.score,
                k,
                time.time() - start_time))
            logging.debug("Scores {}".format(scores))

            if scores[-1] < best_solution.score:
                best_solution = copy.deepcopy(solution_prim)
                unimproving_iterations = 0
            else:
                unimproving_iterations += 1

            # Simulated annealing
            delta_f = scores[-1] - current_solution.score
            if delta_f < 0:
                current_solution = solution_prim
                k = 0
            else:
                if temperature > 1e-4:
                    proba = math.exp(- delta_f / temperature)
                    logging.debug("Proba {}".format(proba))
                    if random.random() < proba and delta_f > 0:
                        current_solution = solution_prim
                        k = 0
                    else:
                        k += 1
                else:
                    k += 1

            iteration += 1
            if (unimproving_iterations + 1) % steps == 0:
                logging.info("Reducing temperature {}".format(temperature))
                temperature = phi * temperature
                # logging.info("Reorganizing")
                # current_solution = copy.deepcopy(best_solution)
                # current_solution.re_organize(int(current_solution.score / 2), multiproc=False)

    return best_solution, scores


if __name__ == "__main__":
    print("Start from main.py")