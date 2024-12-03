from header import *

# TODO:
# - stagger overlapping lines

# for a given problem, it finds the best algorithm to use for each value of proc number
# and plots the work overhead required; best here is in terms of speedup
# (relative to the best sequential)

def problem_overhead_vs_proc(par_data,seq_data,problem,n_values=[10**3,10**6,10**9],
                             allowed_models=set(model_dict.keys())):
    
    plt.style.use('default')
    fig, ax = plt.subplots(1,1,figsize=(6.55,3),dpi=200,layout='tight')


    seq_algs = {k: v for k, v in seq_data.items() if v["problem"]==problem}
    best_seq = get_best_sequential(seq_algs)
    seq_time = seq_data[best_seq]["time"]

    j=0
    handles = []
    all_segments_to_be_plotted = []
    for n in n_values:
        segments_to_be_plotted_for_n = [] # segments are in form of (start_p,end_p,work_overhead)

        # colors
        n_color = COLORS[j]
        new_patch = mpatches.Patch(color=n_color, label="$n="+get_nice_n(n)+"$")
        handles.append(new_patch)
        j+=1

        max_speedup = best_algos_by_speedup(par_data,seq_data,problem,n,
                            allowed_models=allowed_models)
        for i in range(len(max_speedup)):
            start_p, int_speedup, alg_name, if_par = max_speedup[i]

            if if_par:
                work = par_data[alg_name]["work"]
                span = par_data[alg_name]["span"]
                work_overhead = get_comp_fn(work)(n)/get_seq_runtime(seq_time,n)
            else:
                work_overhead = 1+(3-j)*0.1

            if i+1 < len(max_speedup):
                end_p = max_speedup[i+1][0]
            elif i+1 == len(max_speedup):
                if if_par:
                    end_p = get_comp_fn(work)(n) / get_comp_fn(span)(n)
                else:
                    end_p = 1
        
            segments_to_be_plotted_for_n.append((start_p,end_p,work_overhead))

        prev_wo = None
        for segment in segments_to_be_plotted_for_n:
            start_p,end_p,work_overhead = segment
            ax.hlines(work_overhead,start_p,end_p,colors=n_color)
            if prev_wo is not None:
                ax.vlines(x=start_p,ymin=prev_wo,ymax=work_overhead,color=n_color,linestyle='-')
            prev_wo = work_overhead

        all_segments_to_be_plotted.append(segments_to_be_plotted_for_n)

    ax.text(20,100,"1 thousand",color=COLORS[0],fontsize=10,verticalalignment='center')
    ax.text(300,1000,"1 million",color=COLORS[1],fontsize=10,verticalalignment='center')
    ax.text(10**4,3000,"1 billion",color=COLORS[2],fontsize=10,verticalalignment='center')
    
    # ax.legend(handles=handles)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_ylabel("Work Overhead")
    ax.set_xlabel("Number of processors")
    ax.set_yticks(ax.get_yticks(),[str(round(x))+"$\\times$" if round(x)>2 else "1$\\times$" if 
            round(x)==1 else "1/"+str(round(1/x))+"$\\times$" for x in ax.get_yticks()])
    ax.set_xticks(ax.get_xticks(),[long_human_format(x) for x in ax.get_xticks()])
    ax.tick_params(axis='both', which='major', labelsize=7)
    ax.set_xlim(0.8,10**7*1.04)
    ax.set_ylim(0.6,10**4)
    ax.set_title("Work Overhead vs # of Processors\nfor the "+problem+" Problem")

    # plt.show()
    plt.savefig(SAVE_LOC+'overhead_vs_proc'+'.png')


    pass

# not used
# def algorithm_speedup_proc_pts(work,span,seq_time,n=10**6):
#     '''
#     for a given parallel algorithm (defined by work and span), computes the two 
#     points in the speedup vs number of processors graph
#     returns (1, speedup at p=1, smallest p with highest speedup, highest speedup)
#     '''
#     seq_rt = get_seq_runtime(seq_time, n)
#     speedup_p_1 = seq_rt / get_runtime(work,span,n,p=1)
#     eff_p = get_comp_fn(work)(n) / get_comp_fn(span)(n)
#     speedup_p_inf = seq_rt / get_runtime(work,span,n,p=eff_p)

#     return (1,speedup_p_1,eff_p,speedup_p_inf)

    