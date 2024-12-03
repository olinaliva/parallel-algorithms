from header import *

# dataset: specific algorithm only

# generates a graph with 2 side-by-side subgraphs of speedup for the
# number of processors, for 2 different algorithms: best parallelism, and best
# work efficient algos. The point is to show that work efficiency is not always
# the better than other algorithms
def strong_scaling_comparison(data,bs_name,we_name,pr_sizes=[10**3,10**6,10**9]):
    
    problem = data[bs_name]["problem"]
    problem_name = problem_dict[problem]
    # max_p = work_fn(max(pr_sizes))/span_fn(max(pr_sizes))
    # x = np.logspace(1, int(1.2*math.log(max_p,10)), 10**3)
    
    fig, ax = plt.subplots(1,2,sharey=True,figsize=(6.5,3.5),dpi=200,layout='tight')
    max_p=10**18
    for x,alg_name,title in [(1,bs_name,"Best Span"),(0,we_name,"Work Efficient")]:
    
        # span_fn = get_comp_fn(data[alg_name]["span"])
        # work_fn = get_comp_fn(data[alg_name]["work"])
        # ax[0, x].plot()
        max_p,handles = strong_scaling_helper(ax[x],data,alg_name,pr_sizes=pr_sizes,max_p=max_p,rel_name=we_name)

        ax[x].set_title(data[alg_name]["auth"]+" ("+str(data[alg_name]["year"])+")"+"\n"+title+" Algorithm")
    
    # ax[1].set_xlim(ax[0].get_xlim())
    ax[0].legend(handles=handles)
    ax[0].set_ylabel("Speedup") 
    
    # ax.set_title("Absolute Speedup vs # of Processors\nfor the "+problem_name+" Algorithms by ")
    
    plt.savefig(SAVE_LOC+'strong_scaling.png')
    # plt.show()
    pass


# this is just plotting the absolute speedup T_1/T_p, which is 
# (work+span)/(work/p + span)

def strong_scaling(data,alg_name,pr_sizes=[10**3,10**6,10**9]):
    """
    Generates the absolute speedup curve for a given algorithm, parametrized on
    problem size n (each n gets a different curve)

    :data: dataset to be used
    :alg_name: name of the algorithm
    :pr_sizes: list of problem size values
    """
    problem = data[alg_name]["problem"]
    problem_name = problem_dict[problem]
    fig, ax = plt.subplots(1,1)
    max_p,handles = strong_scaling_helper(ax,data,alg_name,pr_sizes=pr_sizes,max_p=10**18)
    ax.set_title("Absolute Speedup vs # of Processors\nfor the "+problem_name+" Algorithm \nby "+
                 data[alg_name]["auth"]+" ("+str(data[alg_name]["year"])+")")
    ax.legend(handles=handles)
    ax.set_ylabel("Speedup")

    plt.show()


def strong_scaling_helper(ax,data,alg_name,pr_sizes=[10**3,10**6,10**9],max_p=None,rel_name=None):
    """
    TODO
    """
    colors = list(mcolors.TABLEAU_COLORS.values())
    problem = data[alg_name]["problem"]
    problem_name = problem_dict[problem]
    span_fn = get_comp_fn(data[alg_name]["span"])
    span = data[alg_name]["span"]
    work_fn = get_comp_fn(data[alg_name]["work"])
    work = data[alg_name]["work"]

    if rel_name is None:
        rel_name = alg_name
    rel_span_fn = get_comp_fn(data[rel_name]["span"])
    rel_span = data[rel_name]["span"]
    rel_work_fn = get_comp_fn(data[rel_name]["work"])
    rel_work = data[rel_name]["work"]
    # print(data[rel_name]["span"])
    # print(data[rel_name]["work"])

    # fig, ax = plt.subplots(1,1)
    handles = []
    if max_p is None:
        max_p = work_fn(max(pr_sizes))/span_fn(max(pr_sizes))
    # print(max_p)
    x = np.logspace(1, int(1.2*math.log(max_p,10)), 10**3)
    x = np.insert(x, 0, 1)
    # print(x)
    
    for i in range(len(pr_sizes)):
        n = pr_sizes[i]
        def abs_speedup(p):
            return get_runtime(rel_work,rel_span,n,1) / get_runtime(work,span,n,p)
        # print(abs_speedup(1))
        y = [abs_speedup(z) for z in x]
        ax.plot(x,y, c=colors[i])
        nice_n = "$10^"+str(int(math.log(n,10)+1))+"$"
        new_patch = mpatches.Patch(color=colors[i], label="$n=$"+nice_n)
        handles.append(new_patch)

    ylims = ax.get_ylim()
    ax.vlines(x=64,ymin=ylims[0],ymax=ylims[1],color=PROCESSOR_COLORS[1],lw=1,alpha=1,linestyles='dashed')
    ax.vlines(x=19860000,ymin=ylims[0],ymax=ylims[1],color=PROCESSOR_COLORS[0],lw=1,alpha=1,linestyles='dashed')
    # ax.set_ylim(ylims)


    # ax.legend(handles=handles)
    # ax.set_title("Absolute Speedup vs # of Processors\nfor the "+problem_name+" Algorithm \nby "+
    #              alg_name[8:])
    # ax.set_title("Absolute Speedup for the "+problem_name+" Algorithm vs \# of Processors\nby "+
    #              data[alg_name]["auth"]+" ("+data[alg_name]["year"]+")")
    ax.set_xlabel("Number of Processors")
    ax.set_xscale('log')
    ax.set_yscale('log')
    xlims = (0.1, 1e+15)
    ax.set_xlim(xlims)
    ticknum = 5
    ax.set_xticks(np.logspace(0,ticknum*round(math.log(xlims[1],10)/ticknum),num=ticknum+1,base=10))

    return max_p, handles
    # plt.show()
