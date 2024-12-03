from header import *


################################################################################
########### Share of families improved each decade #############################
################################################################################

# helper function that returns problems and their improvements (for span and work) 
# independently. needs to keep track of for every problem and year with an improvement, 
# what's the best span and best work (independently), and the names of the algos for
# each of those
# also needs to return the first algo for every problem
# returns: best_stats - dict by problem of dict by year of {"bs alg": name, "bw alg": name}
#          first_stats - dict mapping problem to name of its first algorithm
# Note that if there are ties, an arbitrary algorithm is returned/referenced
def span_work_improvements(data):
    # sort the algos based on increasing year, then based on decreasing span
    names = list(data.keys())
    names.sort(key= lambda name: (data[name]["year"], -1*data[name]["span"]))

    first_year = data[names[0]]["year"]
    cur_year = 2024 # TODO

    probs = get_problems(data)
    best_stats = {}
    for prob in probs:
        best_stats[prob] = {}
        for year in range(first_year,cur_year+1):
            best_stats[prob][year] = {"bs alg": None, "bw alg": None}
            pass
    first_stats = {} # for every problem, keeps track of its first algo

    y = first_year
    alg_i = 0
    while y <= cur_year+1 and alg_i <= len(names):
        if alg_i < len(names):
            name = names[alg_i]
            year = data[name]["year"]
        else:
            year = cur_year+1
        while y < year:
            # update all remaining problems
            for prob in probs:
                if best_stats[prob][y]["bs alg"] is None and y>first_year:
                    best_stats[prob][y]["bs alg"] = best_stats[prob][y-1]["bs alg"]
                if best_stats[prob][y]["bw alg"] is None and y>first_year:
                    best_stats[prob][y]["bw alg"] = best_stats[prob][y-1]["bw alg"]
            y += 1
        assert y == year
        if y == cur_year+1:
            break

        prob = data[name]["problem"]
        # initialize if it's the first algorithm
        if year == first_year or best_stats[prob][year-1]["bs alg"] is None:
            best_stats[prob][year]["bs alg"] = name
            best_stats[prob][year]["bw alg"] = name
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
# print(span_work_improvements(test_data_1))


# Share of known algorithm families improved each decade
# here improvement is defined as either span or work or both independently, 
# depending on the input "aspects" (which defaults to both independently)
def improvement_decades(data, decades, aspects=["span","work"]):
    cur_year = 2024
    probs = get_problems(data)
    improvement_dict, first_algos = span_work_improvements(data)

    years_to_be_checked = [dec["max"] for dec in decades]
    while years_to_be_checked[-1] > cur_year:
        del years_to_be_checked[-1]
    if len(years_to_be_checked) < len(decades):
        years_to_be_checked.append(cur_year)

    # initializing the final data structure
    decade_impr = [0]*len(years_to_be_checked)
    for prob in probs:
        first_algo = first_algos[prob]
        for i in range(len(years_to_be_checked)):
            year = years_to_be_checked[i]
            if data[first_algo]["year"] > year:
                continue

            if i == 0 or data[first_algo]["year"] > years_to_be_checked[i-1]:
                prev_year = data[first_algo]["year"]
            else:
                prev_year = years_to_be_checked[i-1]

            for asp in aspects:
                name = improvement_dict[prob][year]["b"+asp[0]+" alg"]
                prev_name = improvement_dict[prob][prev_year]["b"+asp[0]+" alg"]
                if data[name][asp] < data[prev_name][asp]:
                    decade_impr[i] += 1
                    # print("improvement detected at algorithm "+name)
                    break

    # draw the histogram
    decade_impr_norm = [x/sum(decade_impr) for x in decade_impr] + [0]*(len(decades)-len(decade_impr))
    print(decade_impr_norm)
    plt.style.use('default')
    fig, ax = plt.subplots(1,1)
    labels = [x["label"] for x in decades]
    ax.bar(range(len(decades)), decade_impr_norm, align='center')
    ax.set_title("Share of families improved each decade")
    ax.set_xticks(range(len(decades)),labels=labels)#, rotation=90)
    plt.show()

g_decades = [{"max": 1950, "label": "40s"}, 
            {"max": 1960, "label": "50s"}, 
            {"max": 1970, "label": "60s"}, 
            {"max": 1980, "label": "70s"}, 
            {"max": 1990, "label": "80s"}, 
            {"max": 2000, "label": "90s"}, 
            {"max": 2010, "label": "00s"}, 
            {"max": 2020, "label": "10s"}, 
            {"max": 2030, "label": "20s"},]

test_data = {
    "name1": {"problem": 1, "year": 2020, "span":20, "work": 40},
    "name2": {"problem": 15.3, "year": 2023, "span":11, "work": 19},
    "name3": {"problem": 1, "year": 2021, "span":24, "work": 36},
    "name4": {"problem": 2, "year": 2024, "span":10, "work": 30},
    "name5": {"problem": 1, "year": 2022, "span":18, "work": 38},
    "name6": {"problem": 2, "year": 2020, "span":20, "work": 40},
    "name7": {"problem": 1, "year": 2023, "span":30, "work": 50},
}
test_decades = [{"max": 2020, "label": "40s"}, 
            {"max": 2021, "label": "50s"}, 
            {"max": 2022, "label": "60s"}, 
            {"max": 2023, "label": "10s"}, 
            {"max": 2024, "label": "20s"},]
# print(improvement_decades(full_data, g_decades, aspects=["work"]))
# print(span_work_improvements(full_data)[1])
