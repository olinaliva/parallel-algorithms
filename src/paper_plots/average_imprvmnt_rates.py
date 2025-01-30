from header import *
from src.thesis_plots.relative_speedup import *

# dataset: main model simulation


################################################################################
########### Average yearly improvement rate ####################################
################################################################################

# Distribution of average yearly improvement rates (original paper figure 3)


def yearly_impr_rate_histo_grid(data,raw_buckets,n_values=[10**3,10**6,10**9],
                                p_values=[8,10**3,10**6],measure="rt"):
    fig, ax = plt.subplots(len(p_values),len(n_values),figsize=(7,7),dpi=200,layout='tight',sharey='all')
    #got mad about argument "layout"
    #fig, ax = plt.subplots(len(p_values),len(n_values),figsize=(7,7),dpi=200, sharey='all')
    
    
    for i in range(len(p_values)):
        p = p_values[i]
        for j in range(len(n_values)):
            n = n_values[j]
            yearly_impr_rate_histo_helper(ax[i,j],data,raw_buckets,n,p,measure=measure)
            # ax[i,j].set_title("$n="+get_nice_n(n)+"$ \# processors = "+get_nice_n(p)+"$")
            
    labels = [raw_buckets[i]["label"] for i in range(len(raw_buckets))]
    for j in range(len(n_values)):
        ax[len(p_values)-1,j].set_xticks(list(range(len(labels))),labels=labels, rotation=90)
        #ax[len(p_values)-1,j].set_xticks(list(range(len(labels))), rotation=90)

        for i in range(len(p_values)-1):
            ax[i,j].get_xaxis().set_visible(False)

    # max_y_lim = max(ax[i,k].get_ylim() for i in range(len(p_values)) for k in range(len(n_values)))
    # print(max_y_lim)
    for i in range(len(p_values)):
        ax[i,0].yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f%%'))
        for j in range(1,len(n_values)):
            # ax[i,j].set_ylim(max_y_lim)
            ax[i,j].get_yaxis().set_visible(False)

            
    ax[0,0].set_title("Problem size ($n$) =\n"+long_human_format(n_values[0]))
    ax[0,1].set_title("Problem size ($n$) =\n"+long_human_format(n_values[1]))
    ax[0,2].set_title("Problem size ($n$) =\n"+long_human_format(n_values[2]))
    ax[0,0].set_ylabel("# processors = \n"+long_human_format(p_values[0]))
    ax[1,0].set_ylabel("# processors = \n"+long_human_format(p_values[1]))
    ax[2,0].set_ylabel("# processors = \n"+long_human_format(p_values[2]))
            
    fig.suptitle("Algorithm Problem Average Yearly Improvement Rate\n(Sequential and Parallel)")
    
    plt.savefig(SAVE_LOC+'average_improvement_rate.png')
    # plt.show()

# requires at least 2 buckets
# used_measure can be either "rt" (running time) or "sp" (span)
def yearly_impr_rate_histo(data, raw_buckets, n,p, measure="rt"):
    
    fig, axis = plt.subplots(1,1)
    yearly_impr_rate_histo_helper(axis,data, raw_buckets, n,p, measure=measure)

    labels = [raw_buckets[i]["label"] for i in range(len(raw_buckets))]
    axis.set_xticks(list(range(len(labels))),labels=labels, rotation=90)
    # nice_n = "$10^"+str(int(math.log(n,10)+1))+"$"
    # ax.set_title("Distribution of average yearly improvement rates\nfor n = "+nice_n+" and p = "+str(p))
    axis.set_title("Distribution of average yearly improvement rates\nfor n = "+str(n))
    plt.show()


# requires at least 2 buckets
# measure can be either "rt" (running time) or "sp" (span)
def yearly_impr_rate_histo_helper(ax,data, raw_buckets, n, p, measure="rt"):
    assert measure == "sp" or measure == "rt"
    def get_measure_value(measure,work,span,n,p):
        '''
        returns running time (if measure is "rt") or span
        :measure: either "sp" for span or "rt" for runtime
        TODO
        '''
        if measure == "sp":
            return get_comp_fn(span)(n)
        elif measure == "rt":
            return get_runtime(work,span,n,p)

    # sort the algos based on increasing year, then based on decreasing span
    names = list(data.keys())
    # if measure == "rt":
    #     names.sort(key= lambda name: (data[name]["year"], -1*data[name]["work"]))
    #     # names.sort(key= lambda name: (data[name]["year"], -1*get_runtime(data[name]["work"],data[name]["span"],n,p)))
    # else:
    names.sort(key= lambda name: (data[name]["year"], -1*data[name]["span"]))
    print("finished sorting")

    #calculates all improvement rates in the same year between worst algorithm and every other one in that problem
    #calculates rate of improvement in strictly greater year
    #does not look at things in the same year (probably never occurs so not a problem...?)
    #NEED best in each problem (each problem only gets one)
    #also check this is a definition of rate?
    #average yearly = 
    #1. ~speedup between first and best &years = between first and 2024 or first and algo year)
    #2. ~speedup between first and every one that improves (care about steepest slope)
    #leaning towards fastest algo ever - normalize by current year or year algo discovered?
    # -> first algo chronologically and best algo
    worst_algs = {} # dict of problems started and their worst alg found
    all_rates = []
    # for name in names:
    #     algo = data[name]
    #     if algo["problem"] not in worst_algs:
    #         worst_algs[algo["problem"]] = name
    #     else:
    #         worst = data[worst_algs[algo["problem"]]]
    #         algo_rt = get_measure_value(measure, algo["work"], algo["span"],n,p)
    #         worst_rt = get_measure_value(measure, worst["work"], worst["span"],n,p)
    #         # only consider legal algorithms (with a valid rate of improvement)
    #         if algo["year"] > worst["year"] and algo_rt <= worst_rt:
    #             impr_ratio = worst_rt / algo_rt
    #             yearly_impr_rate = impr_ratio ** (1/(algo["year"]-worst["year"]))-1
    #             all_rates.append(yearly_impr_rate)

    problems=get_problems(data)
    best_stats, first_stats=improvements(data,n,p)
    for problem in problems:
        #take 1st chronological algo
        first=first_stats[problem]
        #^format example is "44658Narayanaswami (1996)"
        first_algo=data[first]
        #print("first: ")
        #print(first)
        #print("first algo: ")
        #print(first_algo)
        first_rt = get_measure_value(measure, first_algo["work"], first_algo["span"],n,p)
        #take bast algo
        #print("best stats: ")
        #print(best_stats[problem])
        best=best_stats[problem][2024]["bs alg"]
        #print("best: ")
        #print(best)
        best_algo=data[best]
        best_rt = get_measure_value(measure, best_algo["work"], best_algo["span"],n,p)
        print("best rate: ", best_rt, " first rate: ", first_rt)
        impr_ratio = first_rt / best_rt
        print("improvement ratio: ", impr_ratio)
        #if first rate and best rate are in the same year?
        #option 1: don't count it at all (that problem doesn't exist when talking about improvement)
        #option 2: count it, somehow penalize it(?) as having no improvement
        #went with option 1 for now
        # if (best_algo["year"]>first_algo["year"]):
        #     yearly_impr_rate = impr_ratio ** (1/(best_algo["year"]-first_algo["year"]))-1
        #     all_rates.append(yearly_impr_rate)
        #here is option 2
        # time=best_algo["year"]-first_algo["year"]
        # if (time==0):
        #     yearly_impr_rate=0
        # else:
        #     yearly_impr_rate = impr_ratio ** (1/time)-1
        # all_rates.append(yearly_impr_rate)
        #option 3: delta time is from first to now (2025?)
        yearly_impr_rate = impr_ratio ** (1/(2025-first_algo["year"]))-1
        all_rates.append(yearly_impr_rate)




    print("finished finding worst algos")

    # find the distribution values to be plotted
    buckets = copy.deepcopy(raw_buckets)
    assert len(buckets) >= 2
    all_rates.sort()
    # print(all_rates) # (11x0.0) 14, 9, 6, 2, 3, 3, 2, 1, 1, 1, 4, 0
    buckets[0]["index"] = bisect.bisect_left(all_rates, buckets[0]["max"])
    buckets[0]["count"] = buckets[0]["index"]
    for i in range(1,len(buckets)-1):
        max_val = buckets[i]["max"]
        buckets[i]["index"] = bisect.bisect_left(all_rates, max_val)
        buckets[i]["count"] = buckets[i]["index"] - buckets[i-1]["index"]
    buckets[-1]["count"] = len(all_rates) - buckets[-2]["index"]
    for i in range(len(buckets)):
        buckets[i]["share"] = buckets[i]["count"] / len(all_rates)

    print("finished finding the distribution")

    # drawing the distribution histogram
    values = [buckets[i]["share"]*100 for i in range(len(buckets))]
    ax.bar(list(range(len(buckets))), values, align='center')


g_buckets = [{"max": 0.1, "label": "0-10%"},
            {"max": 0.2, "label": "10-20%"},
            {"max": 0.3, "label": "20-30%"},
            {"max": math.inf, "label": ">30%"},]

many_g_buckets = [{"max": 0.1, "label": "0-10%"},
            {"max": 0.2, "label": "10-20%"},
            {"max": 0.3, "label": "20-30%"},
            {"max": 0.4, "label": "30-40%"},
            {"max": 0.5, "label": "40-50%"},
            {"max": 0.6, "label": "50-60%"},
            {"max": 0.7, "label": "60-70%"},
            {"max": 0.8, "label": "70-80%"},
            {"max": 0.9, "label": "80-90%"},
            {"max": 1, "label": "90-100%"},
            {"max": 10, "label": "100-1000%"},
            {"max": math.inf, "label": ">1000%"},]

# yearly_impr_rate_histo(full_data, g_buckets, 10**3)


#this is copy paste from thesis_plots/helper_improvements because i didn't want to deal with file managment :(
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


def first_seq_names(data):
    '''returns: first_algos: dictionary by problem of algorithm names for the 1st algo of that problem'''
    #sort em
    #going to assume that first algo is the worst one, if multiple in one year; for seq data just use time
    names = list(data.keys())
    names.sort(key= lambda name: (data[name]["year"], -1*data[name]["time"])) 
    first_algos={}
    #go through all, if no algo for problem yet, add it
    for algo in names:
        prob=data[algo]["problem"]
        if prob not in first_algos.keys():
            first_algos[prob]=algo
    return first_algos



#new improvement rate graph function
def NEW_yearly_impr_rate_histo_grid(par_data, seq_data, raw_buckets,n_values=[10**3,10**6,10**9],
                                p_values=[8,10**3,10**6],measure="rt"):
    fig, ax = plt.subplots(len(p_values),len(n_values),figsize=(7,7),dpi=200,layout='tight',sharey='all')
    #got mad about argument "layout"
    #fig, ax = plt.subplots(len(p_values),len(n_values),figsize=(7,7),dpi=200, sharey='all')
    
    
    for i in range(len(p_values)):
        p = p_values[i]
        for j in range(len(n_values)):
            n = n_values[j]
            NEW_yearly_impr_rate_histo_helper(ax[i,j],par_data,seq_data,raw_buckets,n,p,measure=measure)
            # ax[i,j].set_title("$n="+get_nice_n(n)+"$ \# processors = "+get_nice_n(p)+"$")
            
    labels = [raw_buckets[i]["label"] for i in range(len(raw_buckets))]
    for j in range(len(n_values)):
        ax[len(p_values)-1,j].set_xticks(list(range(len(labels))),labels=labels, rotation=90)
        #ax[len(p_values)-1,j].set_xticks(list(range(len(labels))), rotation=90)

        for i in range(len(p_values)-1):
            ax[i,j].get_xaxis().set_visible(False)

    # max_y_lim = max(ax[i,k].get_ylim() for i in range(len(p_values)) for k in range(len(n_values)))
    # print(max_y_lim)
    for i in range(len(p_values)):
        ax[i,0].yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f%%'))
        for j in range(1,len(n_values)):
            # ax[i,j].set_ylim(max_y_lim)
            ax[i,j].get_yaxis().set_visible(False)

            
    ax[0,0].set_title("Problem size ($n$) =\n"+long_human_format(n_values[0]))
    ax[0,1].set_title("Problem size ($n$) =\n"+long_human_format(n_values[1]))
    ax[0,2].set_title("Problem size ($n$) =\n"+long_human_format(n_values[2]))
    ax[0,0].set_ylabel("# processors = \n"+long_human_format(p_values[0]))
    ax[1,0].set_ylabel("# processors = \n"+long_human_format(p_values[1]))
    ax[2,0].set_ylabel("# processors = \n"+long_human_format(p_values[2]))
            
    fig.suptitle("Algorithm Problem Average Yearly Improvement Rate\n(Sequential and Parallel)")
    
    plt.savefig(SAVE_LOC+'NEW_average_improvement_rate.png')
    # plt.show()

#requires at least 2 buckets
# measure can be either "rt" (running time) or "sp" (span)
def NEW_yearly_impr_rate_histo_helper(ax,par_data,seq_data, raw_buckets, n, p, measure="rt"):
    assert measure == "sp" or measure == "rt"
    def get_measure_value(measure,work,span,n,p):
        '''
        returns running time (if measure is "rt") or span
        :measure: either "sp" for span or "rt" for runtime
        TODO
        '''
        if measure == "sp":
            return get_comp_fn(span)(n)
        elif measure == "rt":
            return get_runtime(work,span,n,p)

    # sort the algos based on increasing year, then based on decreasing span
    names = list(par_data.keys())
    names.sort(key= lambda name: (par_data[name]["year"], -1*par_data[name]["span"]))
    print("finished sorting")

    #for each problem, takes 1st sequential algo and best parallel algo
    #best=smallest run time for the problem size and processor number
    
    all_rates = []
    problems=get_problems(par_data) #takes problems from parallel data, do we want ALL problems instead?
    best_stats, first_stats=improvements(par_data,n,p)
    #get first sequential algos
    first_seq=first_seq_names(seq_data)
    for problem in problems:
        if problem in first_seq.keys():
            #take 1st chronological algo
            first=first_seq[problem]
            #^format example is "44658Narayanaswami (1996)"
            first_algo=seq_data[first]
            first_algo_time=first_algo["time"]
            first_rt = get_seq_runtime(first_algo_time,n)
        else:
            first=first_stats[problem]
            #^format example is "44658Narayanaswami (1996)"
            first_algo=par_data[first]
            first_rt = get_measure_value(measure, first_algo["work"], first_algo["span"],n,p)
        #take best algo
        best=best_stats[problem][2024]["bs alg"]
        best_algo=par_data[best]
        best_rt = get_measure_value(measure, best_algo["work"], best_algo["span"],n,p)
        #print("best rate: ", best_rt, " first rate: ", first_rt)
        impr_ratio = first_rt / best_rt
        #print("improvement ratio: ", impr_ratio)
        #delta t is from first seq to now (2025)
        print(first_algo["year"])
        print(impr_ratio)
        print(impr_ratio ** (1/(2025-first_algo["year"])))
        #double check formula!!
        #yearly_impr_rate = impr_ratio ** (1/(2025-first_algo["year"]))-1
        yearly_impr_rate = impr_ratio ** (1/(2025-first_algo["year"]))
        all_rates.append(yearly_impr_rate)

    print("finished finding improvement rates")

    # find the distribution values to be plotted
    buckets = copy.deepcopy(raw_buckets)
    assert len(buckets) >= 2
    all_rates.sort()
    # print(all_rates) # (11x0.0) 14, 9, 6, 2, 3, 3, 2, 1, 1, 1, 4, 0
    buckets[0]["index"] = bisect.bisect_left(all_rates, buckets[0]["max"])
    buckets[0]["count"] = buckets[0]["index"]
    for i in range(1,len(buckets)-1):
        max_val = buckets[i]["max"]
        buckets[i]["index"] = bisect.bisect_left(all_rates, max_val)
        buckets[i]["count"] = buckets[i]["index"] - buckets[i-1]["index"]
    buckets[-1]["count"] = len(all_rates) - buckets[-2]["index"]
    for i in range(len(buckets)):
        buckets[i]["share"] = buckets[i]["count"] / len(all_rates)

    print("finished finding the distribution")

    # drawing the distribution histogram
    values = [buckets[i]["share"]*100 for i in range(len(buckets))]
    ax.bar(list(range(len(buckets))), values, align='center')


g_buckets = [{"max": 0.1, "label": "0-10%"},
            {"max": 0.2, "label": "10-20%"},
            {"max": 0.3, "label": "20-30%"},
            {"max": math.inf, "label": ">30%"},]

many_g_buckets = [{"max": 0.1, "label": "0-10%"},
            {"max": 0.2, "label": "10-20%"},
            {"max": 0.3, "label": "20-30%"},
            {"max": 0.4, "label": "30-40%"},
            {"max": 0.5, "label": "40-50%"},
            {"max": 0.6, "label": "50-60%"},
            {"max": 0.7, "label": "60-70%"},
            {"max": 0.8, "label": "70-80%"},
            {"max": 0.9, "label": "80-90%"},
            {"max": 1, "label": "90-100%"},
            {"max": 10, "label": "100-1000%"},
            {"max": math.inf, "label": ">1000%"},]