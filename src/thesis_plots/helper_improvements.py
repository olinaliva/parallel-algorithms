from header import *

# dataset: simulated


# helper function that returns problems' improvements (for span, work, and runtime)
# (independenly) in the form of names of the best algorithms for every year.
# needs to keep track of for every problem and year with an improvement, 
# what's the best span and best work and best runtime (independently), and the names of 
# the algos for each of those.

# should not use sequential algorithms (e.g. when there's no work-efficient algorithm,
# best work should not be sequential) bc this is a helper function used for parallel-
# specific things

def improvements(data, n=10**3,p=8,lower=False):
    """
    Finds the best algorithms for every year for each aspect out of span, work,
    and runtime. If there are ties, an arbitrary algorithm is returned.

    :data: dataset to be used (*simulated* parallel)
    :n: problem size for runtime calculation
    :p: number of processors for runtime calculation
    :returns: best_stats - dict by problem of dict by year of {"bs alg": name, 
                            "bw alg": name, "br alg": name}
                            (bs = span, bw = work, br = running time)
              first_stats - dict mapping problem to name of its first algorithm
    """
    # sort the algos based on increasing year, then based on decreasing span
    names = list(data.keys())
    names.sort(key= lambda name: (data[name]["year"], -1*data[name]["span"]))

    first_year = data[names[0]]["year"]

    probs = get_problems(data)
    best_stats = {}
    for prob in probs:
        best_stats[prob] = {}
        for year in range(first_year,CUR_YEAR+1):
            best_stats[prob][year] = {"bs alg": None, "bw alg": None, "br alg": None}
    first_stats = {} # for every problem, keeps track of its first algo

    y = first_year
    alg_i = 0
    while y <= CUR_YEAR+1 and alg_i <= len(names):
        if alg_i < len(names):
            name = names[alg_i]
            year = data[name]["year"]
        else:
            year = CUR_YEAR+1
        while y < year:
            # update all remaining problems
            for prob in probs:
                if best_stats[prob][y]["bs alg"] is None and y>first_year:
                    best_stats[prob][y]["bs alg"] = best_stats[prob][y-1]["bs alg"]
                if best_stats[prob][y]["bw alg"] is None and y>first_year:
                    best_stats[prob][y]["bw alg"] = best_stats[prob][y-1]["bw alg"]
                if best_stats[prob][y]["br alg"] is None and y>first_year:
                    best_stats[prob][y]["br alg"] = best_stats[prob][y-1]["br alg"]
            y += 1
        assert y == year
        if y == CUR_YEAR+1:
            break

        prob = data[name]["problem"]
        # initialize if it's the first algorithm
        if year == first_year or best_stats[prob][year-1]["bs alg"] is None:
            best_stats[prob][year]["bs alg"] = name
            best_stats[prob][year]["bw alg"] = name
            best_stats[prob][year]["br alg"] = name
            first_stats[prob] = name

        # update the best span algorithm if necessary
        if best_stats[prob][year]["bs alg"] is None:
            best_span = data[best_stats[prob][year-1]["bs alg"]]["span"]
        else:
            best_span = data[best_stats[prob][year]["bs alg"]]["span"]
        if data[name]["span"] < best_span:
            best_stats[prob][year]["bs alg"] = name

        # update the best work algorithm if necessary
        if best_stats[prob][year]["bw alg"] is None:
            best_work = data[best_stats[prob][year-1]["bw alg"]]["work"]
        else:
            best_work = data[best_stats[prob][year]["bw alg"]]["work"]
        if data[name]["work"] < best_work:
            best_stats[prob][year]["bw alg"] = name
            
        # update the best running time algorithm if necessary
        if best_stats[prob][year]["br alg"] is None:
            old_name = best_stats[prob][year-1]["br alg"]
            wk = data[old_name]["work"]
            sp = data[old_name]["span"]
            best_runtime = get_runtime(wk,sp,n,p,lower=lower)
        else:
            old_name = best_stats[prob][year]["br alg"]
            wk = data[old_name]["work"]
            sp = data[old_name]["span"]
            best_runtime = get_runtime(wk,sp,n,p,lower=lower)
            
        wk = data[name]["work"]
        sp = data[name]["span"]
        cur_runtime = get_runtime(wk,sp,n,p,lower=lower)
        if cur_runtime < best_runtime:
            best_stats[prob][year]["br alg"] = name

        alg_i += 1

    return best_stats, first_stats

test_data_1 = {
    "name1": {"problem": 1, "year": 2020, "span":20, "work": 40},
    "name2": {"problem": 15.3, "year": 2023, "span":11, "work": 19},
    "name3": {"problem": 1, "year": 2021, "span":24, "work": 36},
    "name4": {"problem": 2, "year": 2024, "span":10, "work": 30},
    "name5": {"problem": 1, "year": 2022, "span":18, "work": 38},
    "name6": {"problem": 2, "year": 2020, "span":20, "work": 40},
    "name7": {"problem": 1, "year": 2023, "span":30, "work": 50},
}
expected_1 = {
    1: {
        2020: {"bs alg": "name1", "bw alg": "name1"},
        2021: {"bs alg": "name1", "bw alg": "name3"},
        2022: {"bs alg": "name5", "bw alg": "name3"},
        2023: {"bs alg": "name5", "bw alg": "name3"},
        2024: {"bs alg": "name5", "bw alg": "name3"}
          },
    2: {
        2020: {"bs alg": "name6", "bw alg": "name6"},
        2021: {"bs alg": "name6", "bw alg": "name6"},
        2022: {"bs alg": "name6", "bw alg": "name6"},
        2023: {"bs alg": "name6", "bw alg": "name6"},
        2024: {"bs alg": "name4", "bw alg": "name4"}
          },
    15.1: {
        2020: {"bs alg": None, "bw alg": None},
        2021: {"bs alg": None, "bw alg": None},
        2022: {"bs alg": None, "bw alg": None},
        2023: {"bs alg": "name2", "bw alg": "name2"},
        2024: {"bs alg": "name2", "bw alg": "name2"}
          }
}
# print(improvements(test_data_1))
