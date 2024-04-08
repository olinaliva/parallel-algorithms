from header import *

# dataset: specific algorithm only (original)


# same as strong scaling, but instead of keeping p constant wrt n, the 3 lines 
# will be sqrt(n), n, and n^2
def varying_scaling_comparison_graph(data,bs_name,we_name):
    
    def p_1(n):
        return max(n**0.25,1)
    def p_2(n):
        return max(math.sqrt(n),1)
    def p_3(n):
        return max(n,1)
    
    p_fun_values = [p_1,p_2,p_3]
    p_labels = ["$n^{0.25}$","$\sqrt{n}$","$n$"]

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
        handles=varying_scaling_helper(ax[x],data,alg_name,p_fun_values,p_labels=p_labels,max_p=max_p,rel_name=we_name)

        ax[x].set_title(data[alg_name]["auth"]+" ("+str(data[alg_name]["year"])+")"+"\n"+title+" Algorithm")
    
    ax[0].legend(handles=handles)
    ax[0].set_ylabel("Running time")

    # ax.set_title("Absolute Speedup vs # of Processors\nfor the "+problem_name+" Algorithms by ")
    
    plt.savefig(SAVE_LOC+'varying_scaling.png')
    # plt.show()
    pass



def varying_scaling_helper(ax,data,alg_name,p_fun_values,p_labels,max_p=None,rel_name=None):
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
    first_runtime=get_runtime(rel_work,rel_span,1,1)

    # fig, ax = plt.subplots(1,1)
    handles = []
    # max_p = work_fn(max(pr_sizes))/span_fn(max(pr_sizes))
    max_p = 10**6

    # x = np.logspace(1, int(1.2*math.log(max_p,10)), 10**3)
    x = np.linspace(1, max_p, 10**3)
    
    for i in range(len(p_fun_values)):
        p_fun = p_fun_values[i]
        def runtime_func(n):
            if n==0:
                return get_runtime(work,span,1,p_fun(1))
            return get_runtime(work,span,n,p_fun(n))
        rtfn = np.vectorize(runtime_func, excluded=[])
        y = rtfn(x)
        ax.plot(x,y, c=colors[i])
        new_patch = mpatches.Patch(color=colors[i], label="p="+p_labels[i])
        handles.append(new_patch)

    # ax.legend(handles=handles)
    ax.set_xlabel("Problem Size")
    ax.set_ylim([-1*10**(3),5*10**4])
    ax.set_xticks(np.linspace(0,max_p,6))
    # plt.show()
    return handles
