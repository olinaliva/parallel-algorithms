# helper functions

import math
from src.standard_codes import *
from src.complexity_functions import *
from src.processed_data import *
#from standard_codes import *
#from complexity_functions import *
#from processed_data import *
import matplotlib
import numbers
import warnings
import bisect
import scipy


def standardize(l):
    '''
    Given a list of numbers, standardize the numbers such that the set of values 
    used is a continuous range starting from 1
    '''
    num_range = sorted(list(set(l)))
    return [num_range.index(i)+1 for i in l]

def standardize_comp(l, collapse=None):
    '''
    standardize, but also returns the time complexities corresponding to the new
    numbers
    '''
    num_range = sorted(list(set(l)))
    complexities = [""]
    if collapse == "span":
        for elem in num_range:
            if complexity_category_1(elem) not in complexities:
                complexities.append(complexity_category_1(elem))
        spans = []
        for elem in l:
            cat = complexity_category_1(elem)
            spans.append(complexities.index(cat))
        return spans, complexities

    for elem in num_range:
        try:
            complexities.append(TIME_CODES[elem])
        except KeyError as er:
            raise KeyError('This complexity class doesn\'t exist in the TIME_CODES dictionary yet: '+str(elem)) from er
    return [num_range.index(i)+1 for i in l], complexities

def standardize_mod(l):
    '''
    same as standardize but with models
    '''
    num_range = sorted(list(set(l)))
    complexities = [""]
    for elem in num_range:
        try:
            complexities.append(model_dict[elem])
        except KeyError as er:
            raise KeyError('This model doesn\'t exist in the model_dict dictionary yet: '+str(elem)) from er
    return [num_range.index(i)+1 for i in l], complexities

# same as above but with problems
# def standardize_prob(l):
#     num_range = sorted(list(set(l)))
#     complexities = [""]
#     for elem in num_range:
#         try:
#             complexities.append(problem_dict[elem])
#         except KeyError as er:
#             raise KeyError('This problem doesn\'t exist in the problem_dict dictionary yet: '+str(elem)) from er
#     return [num_range.index(i)+1 for i in l], complexities

def get_comp_fn(code):
    '''
    given the encoding of a complexity class, return the function that computes it
    e.g. for input 1.5 returns comp_fn_1_5000 (which computes log^{1.5}(n))
    '''
    tail = int(round((code%1),5)*10**4)
    fn_str = "comp_fn_"+str(int(code//1))+"_"+f'{tail:04}'
    #dealing with encodings that dont exist yet
    #return globals()[fn_str]
    # if fn_str not in globals().keys():
    #     to_return=globals()["comp_fn_"+str(int(1000//1))+"_"+f'{int(round((1000%1),5)*10**4):04}'] #plugged in a random encoding thats going to be very high and incorrect (2^n)
    # else:
    #     to_return=globals()[fn_str]
    to_return=globals()[fn_str]
    return to_return
    

def get_problems(data):
    '''
    given some data, returns the set of problem codes
    '''
    # probs = set()
    # for s in get_families_and_problems(data).values():
    #     probs |= s
    # return probs
    return set(data[name]["problem"] for name in data)

def get_families(data):
    '''
    given some data, returns the set of problem family names
    '''
    return set(get_families_and_problems(data).keys())

def get_families_and_problems(data):
    '''
    given some data, returns a dictionary mapping each problem family in the
    data to the set of its problem codes
    '''
    fams = {}
    vars = set(data[name]["problem"] for name in data)
    for var in vars:
        fam = var_weight_dict[var]["family"]
        if fam in fams:
            fams[fam].add(var)
        else:
            fams[fam] = {var}
    # print(fams)
    return fams

def get_runtime(work,span,n,p,lower=False, parallel=True):
    if lower:
        warnings.warn("Warning - using lower bound for runtime!")
        return get_lower_runtime(work,span,n,p)
    if parallel==False: return get_seq_runtime(work,n)
    assert p >= 1
    work_fn = get_comp_fn(work)
    span_fn = get_comp_fn(span)
    try:
        return work_fn(n)/p + span_fn(n)
    except OverflowError:
        return work_fn(n)//p + int(span_fn(n))
    
def get_lower_runtime(work,span,n,p):
    assert p >= 1
    work_fn = get_comp_fn(work)
    span_fn = get_comp_fn(span)
    try:
        return max(work_fn(n)/p, span_fn(n))
    except OverflowError:
        return max(work_fn(n)//p, int(span_fn(n)))

def get_seq_runtime(time,n):
    time_fn = get_comp_fn(time)
    return time_fn(n)

def get_nice_n(n):
    """
    Given n, return it as a power of 10 (in LaTeX form)

    :n: the number to be written as a power of 10
    :returns: string, power of 10
    """
    return "10^{"+str(int(math.log(n,10)+1))+"}" if n>999 else str(n)

def create_aux_data(par_data,seq_data):
    '''
    Creates the problem-level dataset

    for every problem in the parallel dataset, it aquires the following data:
        "best seq", "bs name", "bs span", "bs work", "bs par", "bs overhead",
        "we name", "we span", "we par", "we exist".
    '''
    # In addition, there are parts of the original aux_data that aren't used:
    # - "bs work"
    # - "we exist"
    # - "we work"

    prob_dict = {}

    # first, gather all the problems we're concerned with (only from parallel)
    for val in par_data:
        prob = par_data[val]["problem"]
        if prob not in prob_dict:
            prob_dict[prob] = {
                "best seq": par_data[val]["work"],
                "bs name": None,
                "bs span": None,
                "bs work": None,
                "bs par": None,
                "bs overhead": None,
                "we name": None,
                "we span": None,
                "we par": None,
                "we exist": False,
            }
        # set the best seq to the best work (in case there are no seq algos)
        #or best par work<best seq
        elif par_data[val]["work"] < prob_dict[prob]["best seq"]:
            prob_dict[prob]["best seq"] = par_data[val]["work"]

    # print(prob_dict)

    # find the best sequential algorithms for every problem
    for val in seq_data:
        prob = seq_data[val]["problem"]
        if prob in prob_dict:
            if seq_data[val]["time"] < prob_dict[prob]["best seq"]:
                prob_dict[prob]["best seq"] = seq_data[val]["time"]

    # for every parallel algorithm,
    for val in par_data:
    # - check to see if it has better span than the current bs for the problem
        prob = par_data[val]["problem"]
        sp = par_data[val]["span"]
        wk = par_data[val]["work"]
        if (prob_dict[prob]["bs span"] is None) or (prob_dict[prob]["bs span"] > sp or 
                                    (prob_dict[prob]["bs span"] == sp 
                                    and prob_dict[prob]["bs work"] > wk)):
    #   + if so, update the current bs
            prob_dict[prob]["bs name"] = val
            prob_dict[prob]["bs span"] = sp
            prob_dict[prob]["bs work"] = wk
            prob_dict[prob]["bs par"] = par_data[val]["par"]
    # - check to see if it's work-efficient
        if prob_dict[prob]["best seq"] == wk:
    #   + if it is, check to see if span is better
            if (prob_dict[prob]["we exist"] is None) or (prob_dict[prob]["we span"]!=None and prob_dict[prob]["we span"]>sp):
    #     = if so, update the current we
                prob_dict[prob]["we name"] = val
                # prob_dict[prob]["we span"] = par_data[val]["span"]
                prob_dict[prob]["we span"] = sp
                prob_dict[prob]["we par"] = par_data[val]["par"]
                prob_dict[prob]["we exist"] = True

    for prob in prob_dict:
        wk = prob_dict[prob]["bs work"]
        #print("prob: ",prob)
        #print("prob_dict[prob]: ",prob_dict[prob])
        #print("code_division", CODE_DIVISON[(wk,prob_dict[prob]["best seq"])])
        # #dealing with CODE_DIVISIONS that are still TODO
        # if wk==prob_dict[prob]["best seq"]:
        #     prob_dict[prob]["bs overhead"] = 0.0
        # elif (wk,prob_dict[prob]["best seq"]) in CODE_DIVISON.keys():
        #     prob_dict[prob]["bs overhead"]=CODE_DIVISON[(wk,prob_dict[prob]["best seq"])]
        # else:
        #     prob_dict[prob]["bs overhead"]=1 #no idea how badly this is going to mess shit up yikes
        
        #old code (if all CODE_DIVISON exist, should go back to this probably)
        prob_dict[prob]["bs overhead"] = (0.0 if wk==prob_dict[prob]["best seq"]
                            else CODE_DIVISON[(wk,prob_dict[prob]["best seq"])])

        # dealing with problems with no existing we algo
        if not prob_dict[prob]["we exist"]:
            prob_dict[prob]["we span"] = prob_dict[prob]["best seq"]
            prob_dict[prob]["we par"] = 0

    # for p in prob_dict:
    #     # print('('+str(prob_dict[p]["bs work"])+'": '+str(prob_dict[p]["best seq"])+"): ")
    #     # print('"'+str(p)+'": '+str(prob_dict[p])+",")
    #     pass
    return prob_dict


def get_best_sequential(seq_algos):
    '''
    returns the asymptotically fastest sequential algorithm if there are any,
    otherwise throws an error
    '''
    if len(seq_algos) > 0:
        return min(seq_algos,key=lambda k: seq_algos[k]["time"])
    raise ValueError("No sequential algorithms given")

def get_pareto_points(par_data,seq_data,problem,
                      allowed_models=set(model_dict.keys()),all_algos=False):
    '''
    returns a tuple of: lists of names of the parallel algos on the 
    pareto frontier for this problem; and the name of the best sequential algo

    if all_algos is False, only the earliest algorithm per point is given
    (i.e. if there are multiple algorithms with the same span and work, only
    the one published first will be returned; other ties are broken arbitrarily)
    '''
    seq_algs = {k: v for k, v in seq_data.items() if v["problem"]==problem}
    if len(seq_algs) > 0:
        best_seq = get_best_sequential(seq_algs)
        best_seq_time = seq_data[best_seq]["time"]
    else:
        best_seq = None
        best_seq_time = 0

    # initializing algs to contain all possible algorithms
    algs = {k: v for k, v in par_data.items() if v["problem"]==problem and 
                v["model"] in allowed_models}
    initial_names = list(algs.keys())

    # finding the pareto algorithms
    for name in initial_names:
        if (best_seq_time < algs[name]["work"] and
            best_seq_time < algs[name]["span"]):
            algs.pop(name)
            continue
        # pareto point = no other point has both better span and better work
        for other_name in algs:
            if (algs[other_name]["span"] < algs[name]["span"] and 
                algs[other_name]["work"] < algs[name]["work"]):
                algs.pop(name)
                break

    if all_algos:
        return list(algs.keys()), best_seq
    
    # cleaning up the multiple algos per pareto point
    names = list(algs.keys())
    names.sort(key= lambda name: (algs[name]["year"]))
    pareto_points = set()
    for name in names:
        if (algs[name]["span"],algs[name]["work"]) in pareto_points:
            algs.pop(name)
        else:
            pareto_points.add((algs[name]["span"],algs[name]["work"]))

    return list(algs.keys()), best_seq

def get_best_seq_time_from_par_algos(par_data,problem,allowed_models=set(model_dict.keys())):
    '''
    given a problem that doesn't have any sequential algorithms, find the fastest
    parallel algorithm on 1 processor; returns the time code that such an
    algorithm would run in
    '''
    warnings.warn("There is no sequential algorithm for problem "+problem)
    relevant_par_algs = {k: v for k, v in par_data.items() if v["problem"]==problem and v["model"] in allowed_models}
    if len(relevant_par_algs) == 0:
        raise ValueError("No relevant parallel algorithms for the "+problem+" problem")
    
    best_time = math.inf
    for alg_name in relevant_par_algs:
        work = par_data[alg_name]["work"]
        best_time = min(best_time,work)

    return best_time


def best_algos_by_speedup(par_data,seq_data,problem,n=10**6,max_p=10**9,
                          allowed_models=set(model_dict.keys())):
    '''
    helper function that for a given problem and problem size finds the names of 
    the best algorithms to use for any number of processors (as a function of 
    proc number)

    returns a list of "segments", where each segment is a tuple of
    (interval start p, speedup, algo name, True if parallel or False otherwise)
    '''
    pareto_points, best_seq = get_pareto_points(par_data,seq_data,problem,
                                                allowed_models=allowed_models)

    if best_seq is None:
        seq_time = get_best_seq_time_from_par_algos(par_data,problem)
        # TODO
    else:
        seq_time = seq_data[best_seq]["time"]
    seq_rt = get_seq_runtime(seq_time, n)
    # print(seq_data[best_seq])
    
    # finding the max p
    max_max_p = 2
    for par_pt in pareto_points:
        work = par_data[par_pt]["work"]
        span = par_data[par_pt]["span"]
        eff_p = get_comp_fn(work)(n) / get_comp_fn(span)(n)
        max_max_p = max(max_max_p,eff_p+1)

    # initialize the speedup envelope to the constant speedup = 1
    max_speedup = [(1,1,best_seq,False),(max_max_p,1,best_seq,False)]

    # progressively refine the top curve
    for par_pt in pareto_points[:1]:
        # print("PARETO POINT::::::::::::::::")
        # print(par_pt)
        work = par_data[par_pt]["work"]
        span = par_data[par_pt]["span"]
        eff_p = get_comp_fn(work)(n) / get_comp_fn(span)(n)

        # looping over relevant intervals
        i=0
        while i+1 < len(max_speedup):
            # print(max_speedup)
            # if max_speedup[i][0] > eff_p:
            #     break
            # print(max_speedup[i+1][0])
            # print(eff_p)
            # print(max_speedup[i+1][0] > eff_p)
            if max_speedup[i][0] < eff_p and max_speedup[i+1][0] > eff_p:
                # print("----CASE0")
                # create new interval at eff_p, breaking up ms[i] into 2
                new_interval = (eff_p,max_speedup[i][1],max_speedup[i][2],max_speedup[i][3])
                max_speedup.insert(i+1,new_interval)
                continue

            p1 = max_speedup[i][0]
            speedup1 = seq_rt / get_runtime(work,span,n,p=p1,lower=True)
            p2 = max_speedup[i+1][0]
            speedup2 = seq_rt / get_runtime(work,span,n,p=p2,lower=True)

            # def root_of(x):
            #     new_func = seq_rt / get_runtime(work,span,n,p=x,lower=True)
            #     old_name = max_speedup[i][2]
            #     if max_speedup[i][3]:
            #         old_func = seq_rt / get_runtime(par_data[old_name]["work"],
            #                     par_data[old_name]["span"],n,p=x,lower=True)
            #     else:
            #         old_func = seq_rt / get_seq_runtime(seq_data[old_name]["time"],n)
            #     return new_func-old_func

            if max_speedup[i][1] < speedup1 and max_speedup[i+1][1] <= speedup2:
                # print("----CASE1")
                # completely replace this interval
                new_interval = (max_speedup[i][0],speedup1,par_pt,True)
                max_speedup[i] = new_interval
                
            elif max_speedup[i][1] < speedup1 and max_speedup[i+1][1] > speedup2:
                # print("----CASE2")
                # possible_x_ints = scipy.optimize.fsolve(root_of,1)
                # print(possible_x_ints)

                # find intersection point
                x_int,y_int = find_lines_intersection(p1,p2,
                        max_speedup[i][1],speedup1,speedup2,max_speedup[i+1][1])

                # insert old interval at new intersection point
                new_interval_2 = (x_int,y_int,max_speedup[i][2],max_speedup[i][3])
                max_speedup.insert(i+1,new_interval_2)
                i += 1

                # insert new interval at p1
                new_interval_1 = (max_speedup[i][0],speedup1,par_pt,True)
                max_speedup[i] = new_interval_1

            elif max_speedup[i][1] >= speedup1 and max_speedup[i+1][1] < speedup2:
                # print("----CASE3")
                # print(max_speedup[i][1])
                # print(speedup1)
                # print(max_speedup[i+1][1])
                # print(speedup2)
                # find intersection point
                x_int,y_int = find_lines_intersection(p1,p2,
                        speedup1,max_speedup[i][1],max_speedup[i+1][1],speedup2)
                
                # print((int(x_int),int(y_int)))
                y_int = max(1,y_int)

                # insert new interval at intersection point with this point
                new_interval = (x_int,y_int,par_pt,True)
                max_speedup.insert(i+1,new_interval)
                i += 1

            elif max_speedup[i][1] >= speedup1 and max_speedup[i+1][1] >= speedup2:
                # print("----CASE4")
                # don't do anything; leave
                pass
            else:
                raise RuntimeError("Should never get here")

            i += 1


        # for inter in max_speedup:
            # print((int(inter[0]),int(inter[1]),inter[2],inter[3]))

        # check the last 2 intervals - if they're different, check the last one's
        # speedup, it should be smaller (if not raise an error); replace the last
        # interval
        if max_speedup[-1][2] != max_speedup[-2][2]:    
            assert max_speedup[-1][1] <= max_speedup[-2][1]
            new_interval = (max_speedup[-1][0],max_speedup[-2][1],max_speedup[-2][2],max_speedup[-2][3])
            max_speedup[-1] = new_interval
                
    # cleaning up and consolidating intervals
    i = 0
    while i+1 < len(max_speedup):
        if max_speedup[i][2] == max_speedup[i+1][2]:
            max_speedup.pop(i+1)
        else:
            i+=1
    
    # print(max_speedup)
    # print("-----------------------")

    max_p_i = bisect.bisect_left([x[0] for x in max_speedup],max_p)
    max_speedup = max_speedup[:max_p_i]
    
    # print(max_speedup)
    # print("---------------------------------------------------")
    return max_speedup

def find_lines_intersection(x1,x2,y1,y2,z1,z2):
    '''
    Given 2 line segments - (x1,y1)-(x2,z2) and (x1,y2)-(x2,z1), find their
    intersection point; requires x1<=x2, y1<=y2, z1<=z2

    returns the intersection point as coordinates x,y
    '''
    assert x1<=x2
    assert y1<=y2
    assert z1<=z2
    # print("y2 = "+str(y2)+"; y1 = "+str(y1)+"; z2 = "+str(z2)+"; z1 = "+str(z1)+";")
    ratio = (y2-y1)/(y2-y1+z2-z1)

    int_x = x1 + (x2-x1)*ratio
    int_y = y1 + (z2-y1)*ratio


    return int_x, int_y

# helper function that, given a parallel algorithm (by name), returns true
# if the algorithm is work efficient or not
def is_work_efficient(par_data,seq_data,problem,par_name,allowed_models=set(model_dict.keys())):
   
    seq_algs = {k: v for k, v in seq_data.items() if v["problem"]==problem}
    if len(seq_algs) > 0:
        best_seq = get_best_sequential(seq_algs)
        best_seq_time = seq_data[best_seq]["time"]
        print(best_seq_time)

        best_seq_time = min(best_seq_time,get_best_seq_time_from_par_algos(par_data,
                                        problem,allowed_models=allowed_models))

        print("final best seq time = "+str(best_seq_time))
    else:
        best_seq_time = get_best_seq_time_from_par_algos(par_data,problem,allowed_models=allowed_models)
        print("noseq seq time = "+str(best_seq_time))

    work = par_data[par_name]["work"]
    print("work = "+str(work))

    if work < best_seq_time:
        raise RuntimeError("Should never get here")
    if work > best_seq_time:
        return False
    return True

# https://stackoverflow.com/questions/579310/formatting-long-numbers-as-strings
def human_format(num,sigdig=3,decdig=2):
    assert sigdig > 0
    assert decdig >= 0
    # num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    sigfm = "{:."+str(sigdig)+"g}"
    decfm = "{:."+str(decdig)+"f}"
    num=float(sigfm.format(num))
    num=float(decfm.format(num))
    #added Qa, Qi, Sx because i think we're hitting big numbers yikes
    #print("magnitude",magnitude)
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T','Qa','Qi','Sx'][magnitude])

def long_human_format(num):
    res = human_format(num,decdig=0)
    res = res.replace("K"," thousand")
    res = res.replace("M"," million")
    res = res.replace("B"," billion")
    return res




if __name__ == '__main__':
    # l = [1.1, 1, 1.15, 0.9, 5, 5, 2, 1, 0, 2, 1, 0.1]
    # print(standardize_comp(l, "span"))
    # print(get_comp_fn(20))
    # print(get_comp_fn(1)(8))
    print(get_problems(full_data))
    pass

