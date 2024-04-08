from header import *
from project.thesis_plots.helper_improvements import *

# dataset: simulated dataset


# what this does is it takes all algorithms for a given problem, then decides for
# each whether the span, work, and runtime have (independently) improved, stayed
# the same, or got worse, as compared to the best algorithm for each metric. then
# it draws a 2D histogram of it (for all problems). It doesn't include the first
# parallel algorithm for a problem.
# 
# Basically if an algorithm improves pushes the pareto frontier, it might be
# calculated as part of the "better-better" category, but could just as well
# be in the "worse-worse" category, because spans and works (or runtimes) are
# being compared independently of each other.

def work_span_improvement_heatmap(data,seq_data={},all_data=None,lower=True,pareto=None):
    """
    Draws the span vs work improvement heatmap
    
    :data: *simulated* parallel dataset
    """
    _, ax = plt.subplots(1,1,figsize=(6.5,5),dpi=200,layout='tight')
    improvement_heatmap(data,ax,measure="wk",all_data=all_data,lower=lower,pareto=pareto,seq_data=seq_data)
    ax.set_title("Improvement Tradeoff between Work and Span")
    if pareto is None:
        plt.savefig(SAVE_LOC+'span_work_improvement.png')
    else:        
        plt.savefig(SAVE_LOC+'span_work_improvement_pareto.png')
    # plt.show()


# span/work improvement heatmap
# measure can be "wk" for work and "rt" for runtime
def improvement_heatmap(input_data,ax,measure,n=10**3,p=8,tsize=20,
                        all_data=None,lower=True,pareto=None,seq_data={}):
    """
    Modifies the given axis object to generate the span/work improvement heatmap
    (or span/runtime improvement)

    :input_data: *simulated* parallel dataset
    :ax: axis object to which the new plot should be added
    :measure: "wk" or "rt" - what to plot against span
    :n: problem size
    :p: number of processors
    :tsize: text size for annotations
    :raises ValueError: if measure is not one of "wk" or "rt"
    """
    if (measure != "wk") and (measure != "rt"):
        raise ValueError("measure has to be either 'wk' (work) or 'rt' (running time)")

    data = {}
    returned_data = get_impr_data(input_data,seq_data,n,p,all_data=all_data,lower=lower)
    if pareto is not None:
        for name in returned_data:
            # print(name)
            # break
            if name in pareto:
                data[name] = returned_data[name]
        print("dataset length:")
        print(len(data))
    else:
        data = returned_data

    # print(data)
    # print(len(data))
    cntr = 0
    for elem in data:
        if data[elem]["sp"] is None:
            # print(data[elem])
            cntr += 1
    # print(cntr)

    names = list(data.keys())    
    frequency_map = np.zeros((3,3))
    number = 0
    for name in names:
        sp_inc = data[name]["sp"]
        wk_inc = data[name][measure]
        if (sp_inc != None) & (wk_inc != None):
            frequency_map[sp_inc+1][wk_inc+1] += 1
            number += 1
            # if sp_inc==1 and wk_inc==-1:
            #     print(name)
    print(number)
        

    frequency_map = np.round(frequency_map/number*100,1)
    # print(frequency_map)
    frequency_map = frequency_map[::-1]
    
    ax.imshow(frequency_map)
    ax.set_xticks(np.arange(3))
    ax.set_yticks(np.arange(3))
    ax.set_xticklabels(["worse", "same", "better"])
    ax.set_yticklabels(["better", "same", "worse"])
    nice_n = "10^{"+str(int(math.log(n,10)+1))+"}"
    x_label = "Work" if measure=="wk" else "Runtime \nfor $n="+nice_n+", p="+get_nice_n(p)+"$"
    ax.set_xlabel(x_label)
    if measure=="rt":
        ax.xaxis.set_label_position('top')
    ax.set_ylabel("Span")
    for i in range(3):
        for j in range(3):
            ax.text(j, i, frequency_map[i, j],
                        ha="center", va="center", color="w", size=tsize)

def get_impr_data(par_data,seq_data={},n=10**3,p=8,all_data=None,lower=True):
    """
    Determines if each algorithm in the given dataset improved any of the 3 
    measures: span, work, and runtime; sets the first algorithm measures to None
    
    :data: *simulated* parallel dataset
    :n: problem size
    :p: number of processors
    :returns: a dictionary mapping each algorithm name in data to the follwing:
            {"sp":,"wk":,"rt":} mapping to 1 if there's an improvement, 0 if the
            measure is as good as the best algorithm so far, and -1 if it's worse
    """
    impr_data = copy.deepcopy(par_data)
    print(len(impr_data))
    for s_name in seq_data:
        tmp_dict = seq_data[s_name].copy()
        tmp_dict["span"] = tmp_dict["work"] = tmp_dict["time"]
        impr_data[s_name] = tmp_dict.copy()
    print(len(impr_data))

    data = par_data
    names = list(data.keys())
    names.sort(key= lambda name: (data[name]["year"], -1*data[name]["span"]))

    if all_data is None:
        all_data = data
    best_stats, first_stats = improvements(impr_data,n,p,lower=lower)
    new_data = {}
    for name in data:
        new_data[name] = {}
        year = data[name]["year"]
        prob = data[name]["problem"]
        if year == impr_data[first_stats[prob]]["year"]:
            new_data[name]["sp"] = None
            new_data[name]["wk"] = None
            new_data[name]["rt"] = None
            continue
        assert year > impr_data[first_stats[prob]]["year"]

        # span
        best_span = best_stats[prob][year-1]["bs alg"]
        new_data[name]["sp"] = (0 if data[name]["span"] == impr_data[best_span]["span"] 
                            else 1 if data[name]["span"] < impr_data[best_span]["span"] 
                            else -1)
        # work
        best_work = best_stats[prob][year-1]["bw alg"]
        new_data[name]["wk"] = (0 if data[name]["work"] == impr_data[best_work]["work"] 
                            else 1 if data[name]["work"] < impr_data[best_work]["work"] 
                            else -1)
        # runtime
        rt = best_stats[prob][year-1]["br alg"]
        current_runtime = get_runtime(data[name]["work"],data[name]["span"],n,p,lower=lower)
        best_runtime = get_runtime(impr_data[rt]["work"],impr_data[rt]["span"],n,p,lower=lower)
        new_data[name]["rt"] = (0 if current_runtime == best_runtime 
                                else 1 if current_runtime < best_runtime 
                                else -1)

        # if new_data[name]["sp"]==-1 and new_data[name]["wk"]==0 and new_data[name]["rt"]==-1:
        #     print(name)
        #     print(str(data[name]["span"])+" vs "+str(data[best_span]["span"])+" span")
        #     print(str(data[name]["work"])+" vs "+str(data[best_work]["work"])+" work")
        #     print(str(current_runtime)+" vs "+str(best_runtime)+" runtime")


    return new_data


MAX_CODE=10000
def pareto_frontier_pushing(par_data,seq_data,year_list=list(range(1968,CUR_YEAR))):
    """ 
    :par_data: *simulated* parallel dataset
    :seq_data: sequential dataset
    :year_list: list of years to consider
    """
    par_names = list(par_data.keys())
    par_names.sort(key= lambda name: (par_data[name]["year"], -1*par_data[name]["work"]))
    
    seq_names = list(seq_data.keys())
    seq_names.sort(key= lambda name: (seq_data[name]["year"], -1*seq_data[name]["time"]))

    problems = get_problems(par_data)
    par_i, seq_i = 0, 0
    par_all_so_far = {prob: set() for prob in problems} #includes all algos on the p frontier so far
    seq_best_so_far = {prob: MAX_CODE for prob in problems}

    pareto_count = 0
    pareto_algs = {}

    for year_i in range(len(year_list)):
        year = year_list[year_i]
        # sequential
        # go through all the seq algos in this year
        # if their time is better, replace the seq_best_so_far, inc count
        while seq_i<len(seq_names) and seq_data[seq_names[seq_i]]["year"] <= year:
            prob = seq_data[seq_names[seq_i]]["problem"]
            if prob not in problems:
                seq_i += 1
                continue
            cur_time = seq_data[seq_names[seq_i]]["time"]
            if seq_best_so_far[prob] > cur_time:
                seq_best_so_far[prob] = cur_time
            seq_i+=1

        # parallel
        # go through all the par algos is this decade
        # if they push the pareto frontier (tbd), replace par_so_far, inc count
        while par_i<len(par_names) and par_data[par_names[par_i]]["year"] <= year:
            prob = par_data[par_names[par_i]]["problem"]
            cur_span = par_data[par_names[par_i]]["span"]
            cur_work = par_data[par_names[par_i]]["work"]

            # improvement = better in at least one respect than all the algos
            frontier_push = True
            for prev in par_all_so_far[prob]:
                if prev[2] < year and prev[0] <= cur_span and prev[1] <= cur_work:
                    frontier_push = False
                    break
            if frontier_push:
                par_all_so_far[prob].add((cur_span,cur_work,year))
                # IF THE PARETO FRONTIER IS PUSHED
                pareto_count += 1
                pareto_algs[par_names[par_i]] = par_data[par_names[par_i]]

                # for prev in par_all_so_far[prob]

            par_i+=1




    
    assert len(pareto_algs) == pareto_count
    
    print(pareto_count)
    print(str(pareto_count/len(par_names)*100)+"%"+" of algorithms have pushed the pareto frontier")
   
    return pareto_algs
    # return pareto_count, str(pareto_count/len(par_names)*100)+"%"+"of algorithms have pushed the pareto frontier"
    # return all_seq_counts, all_par_counts





# test_data = {
# "13.13": {"sp": None, "wk": None},
# "13.17": {"sp": None, "wk": None},
# "13.18": {"sp": None, "wk": None},
# "13.14": {"sp": 0, "wk": -1},
# "13.15": {"sp": 0, "wk": 0},
# "13.19": {"sp": None, "wk": None},
# "13.122": {"sp": 0, "wk": 1},
# "13.11": {"sp": None, "wk": None},
# "13.12": {"sp": None, "wk": None},
# "13.16": {"sp": 0, "wk": 1},
# "13.110": {"sp": None, "wk": None},
# "13.119": {"sp": None, "wk": None},
# "13.113": {"sp": 1, "wk": -1},
# "13.117": {"sp": None, "wk": None},
# "13.118": {"sp": None, "wk": None},
# "13.120": {"sp": None, "wk": None},
# "13.121": {"sp": 0, "wk": 0},
# "13.112": {"sp": 0, "wk": -1},
# "13.115": {"sp": 0, "wk": 0},
# "13.111": {"sp": -1, "wk": 1},
# "13.116": {"sp": 0, "wk": 1},
# "13.114": {"sp": 0, "wk": -1},
# "14.12": {"sp": None, "wk": None},
# "14.13": {"sp": None, "wk": None},
# "14.14": {"sp": None, "wk": None},
# "14.15": {"sp": None, "wk": None},
# "14.16": {"sp": None, "wk": None},
# "14.17": {"sp": 0, "wk": -1},
# "14.18": {"sp": 0, "wk": 0},
# "14.19": {"sp": None, "wk": None},
# "14.110": {"sp": 0, "wk": 1},
# "14.111": {"sp": 1, "wk": 1},
# "14.112": {"sp": 1, "wk": -1},
# "14.11": {"sp": None, "wk": None},
# "171": {"sp": None, "wk": None},
# "172": {"sp": None, "wk": None},
# "173": {"sp": None, "wk": None},
# "174": {"sp": None, "wk": None},
# "175": {"sp": None, "wk": None},
# "176": {"sp": None, "wk": None},
# "177": {"sp": -1, "wk": 1},
# "1711": {"sp": None, "wk": None},
# "178": {"sp": 0, "wk": 1},
# "179": {"sp": 1, "wk": 1},
# "1710": {"sp": None, "wk": None},
# "339": {"sp": None, "wk": None},
# "331": {"sp": None, "wk": None},
# "332": {"sp": 1, "wk": -1},
# "3310": {"sp": -1, "wk": 0},
# "335": {"sp": 1, "wk": -1},
# "336": {"sp": -1, "wk": 0},
# "337": {"sp": None, "wk": None},
# "338": {"sp": None, "wk": None},
# "3312": {"sp": -1, "wk": 0},
# "3311": {"sp": None, "wk": None},
# "333": {"sp": 1, "wk": 1},
# "334": {"sp": 0, "wk": 0},
# }

# improvement_heatmap(data)

