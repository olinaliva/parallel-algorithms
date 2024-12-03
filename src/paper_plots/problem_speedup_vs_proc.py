from header import *


# draws the best speedup for all processors (the envelope of speedup vs
# processor plots for all algorithms) for a given problem
def problem_speedup_vs_proc(par_data,seq_data,problem,n_values=[10**3],
                             allowed_models=set(model_dict.keys()),max_p=10**9):
    
    seq_algs = {k: v for k, v in seq_data.items() if v["problem"]==problem}
    best_seq = get_best_sequential(seq_algs)
    seq_time = seq_data[best_seq]["time"]
    
    plt.style.use('default')
    fig, ax = plt.subplots(1,1,figsize=(6.55,3),dpi=200,layout='tight')

    n_max_x = 0
    all_max_speedups = {}
    for n in n_values:
        seq_rt = get_seq_runtime(seq_time, n)
        max_speedup = best_algos_by_speedup(par_data,seq_data,problem,n,max_p=max_p,
                            allowed_models=allowed_models)
        all_max_speedups[n] = max_speedup

        # print(n)
        # print(max_speedup)
        
        # computing the largest value of x that would be interesting to look at
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

    n_max_x = min(n_max_x,max_p)
    sampling_rate = max(1,n_max_x/1000)
    j=0
    handles = []
    final_y_vals = []
    for n in n_values:
        # print(n)
        seq_rt = get_seq_runtime(seq_time, n)
        max_speedup = all_max_speedups[n]
        n_color = COLORS[j]
        new_patch = mpatches.Patch(color=n_color, label="$n="+get_nice_n(n)+"$")
        handles.append(new_patch)
        j+=1
        # new_interval = (max_p, None, None, None)
        # max_speedup.append(new_interval)
        for i in range(len(max_speedup)):
            start_p, int_speedup, alg_name, if_par = max_speedup[i]

            x1 = max(1,math.floor(start_p//sampling_rate))
            if i < len(max_speedup)-1:
                largest_p_for_x2 = min(max_speedup[i+1][0],n_max_x)
                x2 = math.floor(largest_p_for_x2//sampling_rate)
            else:
                x2 = math.ceil(n_max_x//sampling_rate)
                
            x = list(range(x1,x2+1))
            x = [a*sampling_rate for a in x]
            if x1==1:
                x.insert(0,1)
            # print(x[:10])

            if if_par:
                work = par_data[alg_name]["work"]
                span = par_data[alg_name]["span"]
                def abs_speedup(p):
                    return seq_rt / get_runtime(work,span,n,p,lower=True)
                y = [abs_speedup(z) for z in x]
            else:
                y = [1 for z in x]

            ax.plot(x,y,c=n_color)
        final_y_vals.append(y[-1])

    ax.text(n_max_x*1.05,final_y_vals[2]*10,"Problem \nSize (n)",color="black",fontsize=10,verticalalignment='center')

    ax.text(n_max_x*1.05,final_y_vals[0],"1 thousand",color=COLORS[0],fontsize=10,verticalalignment='center')
    ax.text(n_max_x*1.05,final_y_vals[1],"1 million",color=COLORS[1],fontsize=10,verticalalignment='center')
    ax.text(n_max_x*1.05,final_y_vals[2],"1 billion",color=COLORS[2],fontsize=10,verticalalignment='center')

    ax.hlines(y=1,xmin=1,xmax=n_max_x,color='black',linestyle='dashed')
    ax.text(n_max_x*1.05,0.3,"Breakeven\nPoint",color="black",fontsize=10,verticalalignment='center')

    # print(x[-1])
    # print(y[-1])
    # ax.set_xlim(0,n_max_x)
    ax.set_xscale('log')
    ax.set_yscale('log')
    # ax.legend(handles=handles)
    ax.set_ylabel("Speedup")
    ax.set_xlabel("Number of processors")
    ax.set_yticks(ax.get_yticks(),[str(round(x))+"$\\times$" if round(x)>2 else "1$\\times$" if 
            round(x)==1 else "1/"+str(round(1/x))+"$\\times$" for x in ax.get_yticks()])
    ax.set_xticks(ax.get_xticks(),[long_human_format(x) for x in ax.get_xticks()])
    ax.tick_params(axis='both', which='major', labelsize=7)
    ax.set_xlim(0.8,n_max_x*1.04)
    ax.set_ylim(10**-3.1,10**3.3)
    ax.set_title("Speed of Parallel\n"+problem_dict[problem])
    # ax.set_ylim(0,y[-1])
            
    # plt.show()
    print(n_max_x)
    plt.savefig(SAVE_LOC+'speedup_vs_proc'+'.png')

            
        

    pass
