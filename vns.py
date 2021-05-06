import logging
import random
import time
import math
import copy

import config as CONF

def v1(solution, nb_to_change):
    blacklist = set([])
    new_sol = copy.deepcopy(solution)
    for i in range(min(len(solution.pire_trains), nb_to_change)):
        pire_pair = solution.pire_trains[i]
        train1 = int(pire_pair[0])
        train2 = int(pire_pair[1])
        to_change = 1
        best_new_it = ""
        best_new_score = 5800000
        to_blacklist = ""
        # Pour chaque itineraire possible du train ..
        for it in solution.admissible[int(train1)]:
            if best_new_score == 0:
                break
            # .. qui est different de l'actuel et n'est pas blacklisté ..
            if it != solution.solution[str(train1)] and it not in blacklist:
                if len(solution.contraintes_par_itineraire[it]) > 0:
                    # .. si le train fait partie d'un quintuplet de contrainte contenant cet itineraire ..
                    for ind_contraintes in solution.contraintes_par_itineraire[it]:
                        sol_contraintes = solution.contraintes[ind_contraintes]
                        if train1 == sol_contraintes[0]:
                            # .. et que l'autre itineraire est utilisé ..
                            if solution.solution[str(sol_contraintes[2])]["itineraire"] == sol_contraintes[3]:
                                # .. alors le meilleur score est celui du cout d'intersection
                                if sol_contraintes[4] < best_new_score :
                                    best_new_it = it
                                    best_new_score = sol_contraintes[4]
                            # .. sinon c'est 0 parce qu'on a trouvé un itineraire sans conflit
                            else:
                                best_new_it = it
                                best_new_score = 0
                                # .. alors on ne veut pas toucher au deuxième itineraire, on le blacklist
                                to_blacklist = sol_contraintes[3]
                                break
                        elif train1 == sol_contraintes[2]:
                            if solution.solution[str(sol_contraintes[0])]["itineraire"] == sol_contraintes[1]:
                                if sol_contraintes[4] < best_new_score :
                                    best_new_it = it
                                    best_new_score = sol_contraintes[4]
                            else:
                                best_new_it = it
                                best_new_score = 0
                                to_blacklist = sol_contraintes[1]
                                break
                else:
                    best_new_it = it
                    best_new_score = 0
                    # pas de blacklist car l'itinéraire ne crée aucun conflit
                    break
        if best_new_score < 5800000 and best_new_score > 0:
            for it in solution.admissible[int(train2)]:
                if best_new_score == 0:
                    break
                # .. qui est different de l'actuel et n'est pas blacklisté ..
                if it != solution.solution[str(train2)] and it not in blacklist:
                    if len(solution.contraintes_par_itineraire[it]) > 0:
                        # .. si le train fait partie d'un quintuplet de contrainte contenant cet itineraire ..
                        for ind_contraintes in solution.contraintes_par_itineraire[it]:
                            list_contraintes = solution.contraintes[ind_contraintes]
                            if train2 == list_contraintes[0]:
                                # .. et que l'autre itineraire est utilisé ..
                                if solution.solution[str(list_contraintes[2])]["itineraire"] == list_contraintes[3]:
                                    # .. alors le meilleur score est celui du cout d'intersection
                                    if list_contraintes[4] < best_new_score :
                                        best_new_it = it
                                        best_new_score = list_contraintes[4]
                                        to_change = 2
                                # .. sinon c'est 0 parce qu'on a trouvé un itineraire sans conflit
                                else:
                                    best_new_it = it
                                    best_new_score = 0
                                    to_change = 2
                                    # .. alors on ne veut pas toucher au deuxième itineraire, on le blacklist
                                    to_blacklist = list_contraintes[3]
                                    break
                            elif train2 == list_contraintes[2]:
                                if solution.solution[str(list_contraintes[0])]["itineraire"] == list_contraintes[1]:
                                    if list_contraintes[4] < best_new_score :
                                        best_new_it = it
                                        best_new_score = list_contraintes[4]
                                        to_change = 2
                                else:
                                    best_new_it = it
                                    best_new_score = 0
                                    to_blacklist = list_contraintes[1]
                                    to_change = 2
                                    break
                    else:
                        best_new_it = it
                        best_new_score = 0
                        to_change = 2
                        # pas de blacklist car l'itinéraire ne crée aucun conflit
                        break
        # si on a trouvé mieux
        if best_new_score < 5800000:
            blacklist.add(to_blacklist)
            if to_change == 1:
                new_sol.solution[str(train1)] = {"voieAQuai": solution.itineraires[best_new_it]["voieAQuai"], "itineraire" : best_new_it}
            else:
                new_sol.solution[str(train2)] = {"voieAQuai": solution.itineraires[best_new_it]["voieAQuai"], "itineraire" : best_new_it}
    
    # for i in range(nb_to_assign):
    return new_sol


def v2(solution, nb_to_assign):
    new_sol = copy.deepcopy(solution)
    for i in range(min(nb_to_assign, len(solution.unassigned))):
        train = int(solution.unassigned[i])
        it = random.randint(0, len(solution.admissible[train]))
        new_sol.solution[str(train)] = {"voieAQuai": solution.itineraires[it]["voieAQuai"], "itineraire" : it}
    return new_sol

def find_t0(solution0, pi=CONF.VNS.PI, number_of_neighbors=CONF.VNS.NB_NEIGHBORS_T0):
    score0 = solution0.score
    medium_score = 0
    for i in range(number_of_neighbors):
        # MAKE A NEIGHBOR
        # medium_score += int(neighbor.score)
        neighbor = v1(solution0, int(len(solution0.trains)/10))
        medium_score += float(neighbor.score)
    medium_score = medium_score / number_of_neighbors
    delta_f = medium_score - score0

    return - delta_f / math.log(pi)


def v(solution, k=0):
    # RETURN A NEIGHBOR
    # THE STRUCT OF THE NEIGHBOR DEPENDS ON K
    if k == 0:
        neighbor = v1(solution, int(len(solution.trains)/10))
    else:
        neighbor = v2(solution, int(len(solution.trains)/10))
    return neighbor


def start_vns(solution, k_max=CONF.VNS.K_MAX, max_time=CONF.VNS.MAX_TIME,
              max_unimproving_iters=CONF.VNS.MAX_UNIMPROVING_ITERS, phi=CONF.VNS.PHI,
              steps=CONF.VNS.STEPS):
    best_solution = copy.deepcopy(solution)
    best_score = best_solution.score
    current_solution = copy.deepcopy(solution)
    current_score = current_solution.score
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
        print("Current VNS score : {}".format(best_score))
        logging.info("Starting new VNS loop {}\t"
                     "Temperature is {:.2e}\t"
                     "Execution time is {:.2f}\t"
                     "Not increased best for {} interations".format(
                         iteration,
                         temperature,
                         time.time() - start_time,
                         unimproving_iterations))
        while k < k_max:
            solution_prim = v(current_solution, k)
            # HERE IT MAY BE NECESSARY TO MAKE THE NEIGHBOR ADMISSIBLE (REPAIR)
            # OR TO OPTIMIZE IT LOCALLY
            # if not solution_prim.is_admissible():
            #     raise RuntimeError
            # solution_prim.optimize_locally()
            scores.append(solution_prim.score)

            # logging.info("VNS score: {}\tCurrent score was {}\tBest score is {}\tk: {}\tTime {:.1f}".format(
            #     scores[-1],
            #     current_solution.score,
            #     best_solution.score,
            #     k,
            #     time.time() - start_time))
            # logging.debug("Scores {}".format(scores))

            if scores[-1] < best_score:
                best_solution = copy.deepcopy(solution_prim)
                best_score = scores[-1]
                unimproving_iterations = 0
            else:
                unimproving_iterations += 1

            # Simulated annealing
            delta_f = scores[-1] - current_score
            if delta_f < 0:
                current_solution = solution_prim
                current_score = score[-1]
                k = 0
            else:
                if temperature > 1e-4:
                    proba = math.exp(- delta_f / temperature)
                    logging.debug("Proba {}".format(proba))
                    if random.random() < proba and delta_f > 0:
                        current_solution = solution_prim
                        current_score = scores[-1]
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