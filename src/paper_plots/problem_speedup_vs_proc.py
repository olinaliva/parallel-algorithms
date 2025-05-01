from header import *


# draws the best speedup for all processors (the envelope of speedup vs
# processor plots for all algorithms) for a given problem
def OLD_problem_speedup_vs_proc(par_data,seq_data,problem,n_values=[10**3],
                             allowed_models=set(model_dict.keys()),max_p=10**9):
    
    #find best sequential algo for given problem
    seq_algs = {k: v for k, v in seq_data.items() if v["problem"]==problem}
    best_seq = get_best_sequential(seq_algs)
    seq_time = seq_data[best_seq]["time"]
    #TODO: get best seq algo from all algos best work instead
    
    #set up plot
    plt.style.use('default')
    fig, ax = plt.subplots(1,1,figsize=(6.55,3),dpi=200,layout='tight')

    n_max_x = 0 #track maximum x-axis value for scaling later
    all_max_speedups = {} #store the best speedup for each n
    for n in n_values: #loop through each problem size
        #sequential runtime for problem size n
        seq_rt = get_seq_runtime(seq_time, n)
        #gets best speedup for given processor #s p
        #TODO: check that best_algos_by_speedup is correct 
        #format it spits things out is list of "fragments" (tuples): 
        #(interval start p, speedup, algo name, True if parallel or False otherwise)
        max_speedup = best_algos_by_speedup(par_data,seq_data,problem,n,max_p=max_p,
                            allowed_models=allowed_models)
        print("max speedup: ",max_speedup)
        all_max_speedups[n] = max_speedup #save it

        # print(n)
        # print(max_speedup)
        
        # computing the largest value of x that would be interesting to look at
        #basically at what # of processors to end x axis
        #TODO: understand whats going on here and comment it
        if not max_speedup[-1][3]: 
            la_eff_p = max_speedup[-1][0]
        else:
            la_name = max_speedup[-1][2]
            la_work = par_data[la_name]["work"]
            la_span = par_data[la_name]["span"]
            la_eff_p = get_comp_fn(la_work)(n) / get_comp_fn(la_span)(n)
        print(la_eff_p)
        print(n_max_x)
        n_max_x = max(n_max_x,la_eff_p*2)

    # print(all_max_speedups)
    print("========================================================")

    #cap x-axis limit
    n_max_x = min(n_max_x,max_p)
    #sample 1000 points along x-axis
    sampling_rate = max(1,n_max_x/1000)
    j=0 #color index
    handles = [] #legend handles
    final_y_vals = [] #track final y-values for label positioning

    #loop through n again to plot each problem size n
    for n in n_values:
        # print(n)
        seq_rt = get_seq_runtime(seq_time, n) #runtime
        max_speedup = all_max_speedups[n] #speedup
        n_color = COLORS[j] #pick a color
        new_patch = mpatches.Patch(color=n_color, label="$n="+get_nice_n(n)+"$")
        handles.append(new_patch)
        j+=1
        # new_interval = (max_p, None, None, None)
        # max_speedup.append(new_interval)

        #plot each speedup
        #TODO: understand and comment this code bit
        for i in range(len(max_speedup)):
            start_p, int_speedup, alg_name, if_par = max_speedup[i]

            #x1 = max(1,math.floor(start_p//sampling_rate))
            #the // seems unnecessary if using math.floor idk
            x1 = max(1,math.floor(start_p/sampling_rate))
            #what's start_p/sampling_rate? 
            # --> probably a number for data pts?
            if i < len(max_speedup)-1:
                largest_p_for_x2 = min(max_speedup[i+1][0],n_max_x)
                #2 = math.floor(largest_p_for_x2//sampling_rate)
                x2 = math.floor(largest_p_for_x2/sampling_rate)
            else:
                #x2 = math.ceil(n_max_x//sampling_rate)
                x2 = math.ceil(n_max_x/sampling_rate)
                
            x = list(range(x1,x2+1))
            x = [a*sampling_rate for a in x]
            if x1==1:
                x.insert(0,1)
            # print(x[:10])
            #i think all that^ should basically just give the x coords (number of p) for data pts
            #not 100% sure though

            #compute speedup values (y-axis) ??
            #if algo is parallel get speedup value, 
            #if algo is sequential, speedup is 1
            if if_par:
                work = par_data[alg_name]["work"]
                span = par_data[alg_name]["span"]
                def abs_speedup(p):
                    #return seq_rt / get_runtime(work,span,n,p,lower=True)
                    #why were we using lower=True?
                    #GRAPH CHANGES SIGNIFICANTLY!!
                    return seq_rt / get_runtime(work,span,n,p)
                #okay, so for every number of proc data pt, get speedup
                y = [abs_speedup(z) for z in x]
            else:
                y = [1 for z in x] #baseline ??

            ax.plot(x,y,c=n_color)
        final_y_vals.append(y[-1])


    #add annotations for problem sizes
    ax.text(n_max_x*1.05,final_y_vals[2]*10,"Problem \nSize (n)",color="black",fontsize=10,verticalalignment='center')
    ax.text(n_max_x*1.05,final_y_vals[0],"1 thousand",color=COLORS[0],fontsize=10,verticalalignment='center')
    ax.text(n_max_x*1.05,final_y_vals[1],"1 million",color=COLORS[1],fontsize=10,verticalalignment='center')
    ax.text(n_max_x*1.05,final_y_vals[2],"1 billion",color=COLORS[2],fontsize=10,verticalalignment='center')

    #dashed line for breakeven (speedup=1)
    ax.hlines(y=1,xmin=1,xmax=n_max_x,color='black',linestyle='dashed')
    ax.text(n_max_x*1.05,0.3,"Breakeven\nPoint",color="black",fontsize=10,verticalalignment='center')

    #set axis to log scale
    ax.set_xscale('log')
    ax.set_yscale('log')

    #label axis
    # ax.legend(handles=handles)
    ax.set_ylabel("Speedup")
    ax.set_xlabel("Number of processors")

    #format tick labels
    ax.set_yticks(ax.get_yticks(),[str(round(x))+"$\\times$" if round(x)>2 else "1$\\times$" if 
            round(x)==1 else "1/"+str(round(1/x))+"$\\times$" for x in ax.get_yticks()])
    ax.set_xticks(ax.get_xticks(),[long_human_format(x) for x in ax.get_xticks()])
    ax.tick_params(axis='both', which='major', labelsize=7)

    #axis limits
    ax.set_xlim(0.8,n_max_x*1.04)
    ax.set_ylim(10**-3.1,10**3.3)
    # print(x[-1])
    # print(y[-1])
    # ax.set_ylim(0,y[-1])
    # ax.set_xlim(0,n_max_x)

    #title
    ax.set_title("Speed of Parallel\n"+problem_dict[problem])
   
            
    # plt.show()
    #print(n_max_x)
    plt.savefig(SAVE_LOC+'OLD_speedup_vs_proc'+'.png')

    pass

def get_processor_breakpoints(algorithms, n,
                               min_processors=1, max_processors=10_000_000):
    """
    Find processor breakpoints where the best algorithm changes and return them as a dictionary.

    Parameters:
    - algorithms: dictionary
        algorithms[name][...]
    - n: int
        Problem size `n` to be passed into the runtime function.
    - min_processors: int
        Minimum number of processors to test (default: 1).
    - max_processors: int
        Maximum number of processors to test (default: 10 million).
    - num_points: int
        Number of processor values to test (logarithmically spaced).

    Returns:
    - breakpoints_dict: dict[int, str]
        A dictionary mapping each breakpoint processor count to the best algorithm used
        from that point onward until the next breakpoint.
    """
    def best_algo_at(p):
        runtimes = {}
        works = {}
        for algo in algorithms:
            work = algorithms[algo]["work"]
            span = algorithms[algo]["span"]
            parallel = algorithms[algo]["parallel"]
            rt = get_runtime(work, span, n, p, parallel)
            runtimes[algo] = rt
            works[algo] = get_seq_runtime(work,n)
        best = min(runtimes, key=runtimes.get)
        return best, runtimes[best], works[best]

    def search_breakpoints(start, end, start_algo, start_runtime, end_algo, end_runtime):
        if end - start <= 1:
            return {}

        mid = (start + end) // 2
        # mid_algo, mid_runtime = best_algo_at(mid)
        mid_algo, mid_runtime, mid_work = best_algo_at(mid)

        breakpoints = {}
        if start_algo != mid_algo:
            left_breaks = search_breakpoints(start, mid, start_algo, start_runtime, mid_algo, mid_runtime)
            breakpoints.update(left_breaks)
            # breakpoints[mid] = {"algorithm": mid_algo, "runtime": mid_runtime}
            breakpoints[mid] = {"algorithm": mid_algo, "runtime": mid_runtime, "work": mid_work}

        if mid_algo != end_algo:
            right_breaks = search_breakpoints(mid, end, mid_algo, mid_runtime, end_algo, end_runtime)
            breakpoints.update(right_breaks)

        return breakpoints

    # Initialize endpoints
    # start_algo, start_runtime = best_algo_at(min_processors)
    # end_algo, end_runtime = best_algo_at(max_processors)
    start_algo, start_runtime, start_work = best_algo_at(min_processors)
    end_algo, end_runtime, end_work = best_algo_at(max_processors) 

    breakpoints = {}

    if start_algo != end_algo:
        breakpoints = search_breakpoints(min_processors, max_processors,
                                         start_algo, start_runtime,
                                         end_algo, end_runtime)
        # breakpoints[min_processors] = {"algorithm": start_algo, "runtime": start_runtime}
        # breakpoints[max_processors] = {"algorithm": end_algo, "runtime": end_runtime}
        breakpoints[min_processors] = {"algorithm": start_algo, "runtime": start_runtime, "work": start_work}
        breakpoints[max_processors] = {"algorithm": end_algo, "runtime": end_runtime, "work": end_work}
    else:
        # breakpoints[min_processors] = {"algorithm": start_algo, "runtime": start_runtime}
        breakpoints[min_processors] = {"algorithm": start_algo, "runtime": start_runtime, "work": start_work}

    # Remove redundant entries where the algorithm hasn't changed
    # cleaned_breakpoints = {}
    # prev_algo = None
    # for p in sorted(breakpoints):
    #     algo = breakpoints[p]["algorithm"]
    #     if algo != prev_algo:
    #         cleaned_breakpoints[p] = breakpoints[p]
    #         prev_algo = algo
    cleaned_breakpoints = {}
    prev_algo = None
    sorted_keys = sorted(breakpoints)
    for i, p in enumerate(sorted_keys):
        algo = breakpoints[p]["algorithm"]
        is_last = (i == len(sorted_keys) - 1)
        if algo != prev_algo or is_last:
            cleaned_breakpoints[p] = breakpoints[p]
            prev_algo = algo

    print("cleaned breakpoints",cleaned_breakpoints)
    return cleaned_breakpoints

    #this was the old func (trying every proc value)
    # breakpoints_dict = {}
    # prev_best = None


    # for p in range(min_processors,max_processors+1):
    #     # print("p:",p)
    #     runtimes = {algo: get_runtime(algorithms[algo]["work"],algorithms[algo]["span"], n, p, algorithms[algo]["parallel"]) for algo in algorithms}
    #     # print("runtimes",runtimes)
    #     best_algo = min(runtimes, key=runtimes.get)
    #     # print("best algo", best_algo)
    #     best_runtime = runtimes[best_algo]

    #     if best_algo != prev_best:
    #         breakpoints_dict[p] = {
    #             "algorithm": best_algo,
    #             "runtime": best_runtime
    #         }
    #         prev_best = best_algo
    # print("breakpoints dict",breakpoints_dict)
    # return breakpoints_dict

def problem_speedup_vs_proc(all_data, problem, n_values=[10**3],max_p=10**9):
    
    #TODO: rewrite this bit
    all_data_prob = {
        name: info
        for name, info in all_data.items()
        if info.get("problem") == problem
    }

    #setup plot
    # plt.figure(figsize=(10, 6))
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    #for each n in n_values
    for n in n_values:
        print("n:",n)
        #get breakpoints
        processor_data = get_processor_breakpoints(all_data_prob,n,min_processors=1,max_processors=max_p)
        print("processor data",processor_data)
        processor_counts = list(processor_data.keys())
        print("processor counts",processor_counts)

        #compute speedups at breakpoints
        speedups = [
            processor_data[1]["runtime"] / processor_data[p]["runtime"] #1 processor will give best seq
            for p in processor_counts
        ]
        print("speedups:", speedups)

        # plt.plot(processor_counts, speedups, linestyle='--', marker=None, label=f"n = {n}")
        # plt.scatter(processor_counts, speedups, marker='o')
        ax1.plot(processor_counts, speedups, linestyle='--', marker=None, label=f"n = {n}")
        ax1.scatter(processor_counts, speedups, marker='o')

        serial_work = processor_data[1]["work"]
        work_overheads = [
            processor_data[p]["work"] / serial_work
            for p in processor_counts
        ]
        # ax2.plot(processor_counts, work_overheads, linestyle='--', marker=None, label=f"n = {n}")
        ax2.step(processor_counts, work_overheads, where='post', linestyle='--', label=f"n = {n}")
        ax2.scatter(processor_counts, work_overheads, marker='o')

        

    # #final plot formatting
    # plt.xscale('log')
    # plt.xlabel('Number of Processors (log scale)')
    # # plt.xlabel('Number of Processors')
    # plt.ylabel('Speedup (Best Serial / Best Parallel Runtime)')
    # plt.title(f"Speedup vs Processors for Problem: {problem}")
    # plt.grid(True, which='both', ls='--', linewidth=0.5)
    # plt.legend()
    # plt.tight_layout()

    # plt.savefig(SAVE_LOC+'speedup_vs_proc_'+problem+'.png')

    ax1.set_xscale('log')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax1.set_yscale('log')
    ax1.axhline(y=1, color='gray', linestyle=':', linewidth=1)
    ax2.axhline(y=1, color='gray', linestyle=':', linewidth=1)

    ax1.set_ylabel('Speedup (Best Serial / Parallel Runtime) (log scale)')
    ax1.set_title(f"Speedup and Work Overhead vs Processors for Problem: {problem}")
    ax1.grid(True, which='both', ls='--', linewidth=0.5)
    ax1.legend()

    ax2.set_xlabel('Number of Processors (log scale)')
    ax2.set_ylabel('Work Overhead (Parallel Work / Serial Work) (log scale)')
    ax2.grid(True, which='both', ls='--', linewidth=0.5)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(SAVE_LOC + f'speedup_and_work_overhead_{problem}.png')

