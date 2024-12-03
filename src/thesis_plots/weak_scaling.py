from header import *

# dataset: specific algorithm only (original)

def weak_scaling_comparison_graph(data,bs_name,we_name,p_values=[1,8,10**6]):
    
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
        handles = weak_scaling_helper(ax[x],data,alg_name,p_values=p_values,max_p=max_p,rel_name=we_name)

        ax[x].set_title(data[alg_name]["auth"]+" ("+str(data[alg_name]["year"])+")"+"\n"+title+" Algorithm")
    
    # ax.set_title("Absolute Speedup vs # of Processors\nfor the "+problem_name+" Algorithms by ")
    ax[0].legend(handles=handles)
    ax[0].set_ylabel("Running Time")

    plt.savefig(SAVE_LOC+'weak_scaling.png')
    # plt.show()
    pass


def weak_scaling_helper(ax,data,alg_name,p_values=[1,128,10**6],max_p=None,rel_name=None):
    """
    TODO
    """
    colors = list(mcolors.TABLEAU_COLORS.values())
    problem = data[alg_name]["problem"]
    problem_name = problem_dict[problem]
    span = data[alg_name]["span"]
    work = data[alg_name]["work"]

    if rel_name is None:
        rel_name = alg_name
    rel_span = data[rel_name]["span"]
    rel_work = data[rel_name]["work"]


    # fig, ax = plt.subplots(1,1)
    handles = []
    # max_p = work_fn(max(pr_sizes))/span_fn(max(pr_sizes))
    max_p = 10**6

    # x = np.logspace(1, int(1.2*math.log(max_p,10)), 10**3)
    x = np.linspace(1, max_p, 10**3)
    
    for i in range(len(p_values)):
        p = p_values[i]
        first_runtime = get_runtime(rel_work,rel_span,n=1,p=p)
        # print(work)
        def runtime_func(n):
            return get_runtime(work,span,n,p)
        rtfn = np.vectorize(runtime_func, excluded=[])
        y = rtfn(x)
        ax.plot(x,y, c=colors[i])
        new_patch = mpatches.Patch(color=colors[i], label="$p="+get_nice_n(p)+"$")
        handles.append(new_patch)

    # ax.legend(handles=handles)
    ax.set_xlabel("Problem Size")
    ax.set_ylim([-10**(6),10**7])
    # ax.set_xscale('log')
    # ax.set_yscale('log')
    # ax.set_xlim((1.0, 1e+22))
    # plt.show()
    
    return handles
