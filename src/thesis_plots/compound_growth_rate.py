from header import *
from src.thesis_plots.relative_speedup import *

# dataset: main model simulation


# for each problem, computes the "compound growth rate" as (f/b)^{1/t}-1, where
# f is the present-day best parallel speedup, b is the best sequential speedup,
# and t is the number of years since the first parallel algorithm (note: the 
# photo shows the bifurcation year). If there's no parallel algorithm (t=0), the
# compound growth rate is set to 0.

def compound_growth_rate_histo_grid(parallel_data,sequential_data,raw_buckets,
                                    n_values=[10**3,10**6,10**9],p_values=[8,10**3,10**6]):
    '''
    generates a grid of CGR distributions, for the provided p and n values
    '''
    fig, ax = plt.subplots(len(p_values),len(n_values),figsize=(7,7),dpi=200,layout='tight')
    for i in range(len(p_values)):
        p = p_values[i]
        top_val = 0
        for j in range(len(n_values)):
            # print("starting "+str(i)+","+str(j))
            n = n_values[j]
            loc_top_val = compound_growth_rate_distribution(ax[i,j],parallel_data,
                                            sequential_data,raw_buckets,n,p)
            top_val = max(top_val,loc_top_val)

        max_y_lim = max(ax[i,k].get_ylim() for k in range(len(n_values)))
        for j in range(len(n_values)):
            ax[i,j].set_ylim(max_y_lim)
            ax[i,j].set_yticks(np.arange(0, top_val+1, 25.0))

    fig.suptitle("Compound Growth Rates")
    fig.supylabel("Percentage of Problems with the Corresponding Compound Growth Rate")
    plt.savefig(SAVE_LOC+'compound_growth_rate.png')
    # plt.show()

    pass


def compound_growth_rate_distribution_graph(parallel_data,sequential_data,raw_buckets,n,p):
    plt.style.use('default')
    fig, ax = plt.subplots(1,1)
    compound_growth_rate_distribution(ax,parallel_data,sequential_data,raw_buckets,n,p)

    # nice_n = "$10^"+str(int(math.log(n,10)+1))+"$"
    # nice_p = "2^{"+str(int(math.log(p,2)))+"}" if p>4096 else str(p)
    ax.set_title("Distribution of Compound Growth Rates\nfor $n = "+get_nice_n(n)+
                 "$ and $p = "+get_nice_n(p)+"$")
    
    plt.show()
    pass





def compound_growth_rate_distribution(ax,parallel_data,sequential_data, raw_buckets,n,p):
    """
    TODO
    Returns the largest percentage plotted

    :parallel_data: *simulated* parallel dataset
    :sequential_data: sequential dataset
    :raw_buckets: list of dicts with the form {"max":,"label"}
    :n: problem size
    :p: number of processors
    """
    problems = get_problems(parallel_data)
    all_rates = []
    for problem in problems:
        par_curve = problem_relative_speedup_data(parallel_data,sequential_data,problem,n,p)
        par_speedup,_,par_name = par_curve[sorted(par_curve.keys())[-1]]
        seq_curve = problem_relative_speedup_data(parallel_data,sequential_data,problem,n,1)
        seq_speedup,_,seq_name = seq_curve[sorted(seq_curve.keys())[-1]]

        first_year = min([parallel_data[alg]["year"] for alg in parallel_data])
        cgr = (par_speedup/seq_speedup)**(1/(CUR_YEAR-first_year))-1
        all_rates.append(cgr)


    # find the distribution values to be plotted
    buckets = copy.deepcopy(raw_buckets)
    assert len(buckets) >= 2
    all_rates.sort()
    buckets[0]["index"] = bisect.bisect_left(all_rates, buckets[0]["max"])
    buckets[0]["count"] = buckets[0]["index"]
    for i in range(1,len(buckets)-1):
        max_val = buckets[i]["max"]
        buckets[i]["index"] = bisect.bisect_left(all_rates, max_val)
        buckets[i]["count"] = buckets[i]["index"] - buckets[i-1]["index"]
    buckets[-1]["count"] = len(all_rates) - buckets[-2]["index"]
    for i in range(len(buckets)):
        buckets[i]["share"] = buckets[i]["count"] / len(all_rates)

    # drawing the distribution histogram
    # plt.style.use('default')
    # fig, ax = plt.subplots(1,1)
    values = [buckets[i]["share"]*100 for i in range(len(buckets))]
    labels = [buckets[i]["label"] for i in range(len(buckets))]
    ax.bar(list(range(len(buckets))), values, align='center',color=SEQ_PAR_COLORS[1])
    nice_n = "$10^"+str(int(math.log(n,10)+1))+"$"
    nice_p = "2^{"+str(int(math.log(p,2)))+"}" if p>4096 else str(p)
    # ax.set_title("Distribution of Compound Growth Rates\nfor n = "+nice_n+" and p = $"+nice_p+"$")
    ax.set_xticks(list(range(len(buckets))),labels=labels, rotation=90)
    # print(max(buckets[i]["share"] for i in range(len(buckets))))
    # ax.set_yticks(np.arange(0, 100*max(buckets[i]["share"] for i in range(len(buckets)))+1, 10.0))
    x_label = "$n = "+get_nice_n(n)+"$ and $p = "+get_nice_n(p)+"$"
    ax.set_xlabel(x_label)
    ax.xaxis.set_label_position('top')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    # plt.show()

    return 100*max(buckets[i]["share"] for i in range(len(buckets)))    
    pass




