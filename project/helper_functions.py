# helper functions

import math
from project.standard_codes import *
from project.complexity_functions import *
from project.processed_data import *
import matplotlib
import numbers
import warnings


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
    return globals()[fn_str]

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

def get_runtime(work,span,n,p,lower=False):
    if lower:
        warnings.warn("Warning - using lower bound for runtime!")
        return get_lower_runtime(work,span,n,p)

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
            if not prob_dict[prob]["we exist"] or (prob_dict[prob]["we span"]>sp):
    #     = if so, update the current we
                prob_dict[prob]["we name"] = val
                prob_dict[prob]["we span"] = par_data[val]["span"]
                prob_dict[prob]["we par"] = par_data[val]["par"]
                prob_dict[prob]["we exist"] = True

    for prob in prob_dict:
        wk = prob_dict[prob]["bs work"]
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





if __name__ == '__main__':
    # l = [1.1, 1, 1.15, 0.9, 5, 5, 2, 1, 0, 2, 1, 0.1]
    # print(standardize_comp(l, "span"))
    # print(get_comp_fn(20))
    # print(get_comp_fn(1)(8))
    print(get_problems(full_data))
    pass

