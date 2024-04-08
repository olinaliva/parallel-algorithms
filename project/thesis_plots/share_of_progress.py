from header import *
from project.thesis_plots.relative_speedup import *

# dataset: simulated dataset


# for each problem, it considers the best speedup achievable 1. sequentially,
# 2. with the max processors available in personal computers, and 3. with the
# max number of processors available in a supercomputer. Notice that they have
# to be in that order (1<=2<=3). We then express this as a geometric proportion (?) 
# aka what part of the "progress" is due to each of these 3. Notice again that
# the supercomputer metric will always be 100%. We then aggregate this data for
# all problems by taking the arithmetic mean. We plot this for multiple values
# of problem size n (currently 3).

MOST_PC_PROC = pc_processor_data[max(pc_processor_data.keys())][0]
MOST_TOP_PROC = top_processor_data[max(top_processor_data.keys())][0]

def share_of_progress_graph(parallel_data,sequential_data,possible_n=[10**3,10**6,10**9]):
    """
    Plots the arithmetic mean over all problems of geometric proportions of 
    sequential progress, PC-parallel progress, and supercomputer-parallel progress

    :parallel_data: *simulated* parallel dataset
    :sequential_data: sequential dataset
    :problem: problem number
    :possible_n: list of problem size values
    """
    n_num = len(possible_n)
    seq_bars, pc_bars, par_bars = share_of_progress_cummulative_data(parallel_data,
                                            sequential_data,possible_n=possible_n)
    assert len(seq_bars)==n_num
    assert len(pc_bars)==n_num
    assert len(par_bars)==n_num

    plt.style.use('default')
    fig, ax = plt.subplots(1,1,figsize=(6.55,4.5),dpi=200,layout='tight')
    ax.grid(axis='y', alpha=0.4)

    ax.bar(range(n_num), seq_bars, label='Sequential', alpha=0.5, color=PROCESSOR_COLORS[2])
    ax.bar(range(n_num), pc_bars, bottom=np.array(seq_bars),label='Personal Computers',alpha=0.5,color=PROCESSOR_COLORS[1])
    ax.bar(range(n_num), par_bars, bottom=np.array(seq_bars)+np.array(pc_bars),
           label='Top Supercomputers',alpha=0.5,color=PROCESSOR_COLORS[0])

    for i in range(n_num):
        ax.annotate(str(round(seq_bars[i]))+"%", xy=(i-0.07, seq_bars[i]/2-1))
        ax.annotate(str(round(pc_bars[i]))+"%", xy=(i-0.07, seq_bars[i]+pc_bars[i]/2-1),)
        ax.annotate(str(round(par_bars[i]))+"%", xy=(i-0.07, seq_bars[i]+pc_bars[i]+par_bars[i]/2-1))

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed(labels), loc='upper left',bbox_to_anchor=(1, 0.5))
    ax.set_title("Geometric Proportion of Relative Speedup Progress\nAveraged over all Problems")
    ax.set_xlabel("Problem Size")
    ax.set_xticks([0,1,2],["$"+get_nice_n(n)+"$" for n in possible_n])
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_ylabel("Average Percentage of Improvement")
    plt.savefig(SAVE_LOC+'share_of_progress.png')
    # plt.show()

def share_of_progress_cummulative_data(parallel_data,sequential_data,possible_n=[10**3,10**6,10**9]):
    """
    Computes the arithmetic mean of geometric proportions of sequential progress,
    PC-parallel progress, and supercomputer-parallel progress, over all problems

    :parallel_data: *simulated* parallel dataset
    :sequential_data: sequential dataset
    :problem: problem number
    :possible_n: list of problem size values
    :returns: tuple of 3 lists . All lists have length len(possible_n)
    """
    problems = get_problems(parallel_data)

    seq_bars = []
    pc_bars = []

    for n in possible_n:
        seq_share_sum = 0
        pc_share_sum = 0
        share_num = 0
        for problem in problems:
            geo_share_seq,geo_share_pc = share_of_progress_problem_data(parallel_data,
                                            sequential_data,problem,n=n)
            if geo_share_seq is not None:
                seq_share_sum+=geo_share_seq
                pc_share_sum+=geo_share_pc-geo_share_seq
                share_num += 1
        seq_bars.append(seq_share_sum/share_num*100)
        pc_bars.append(pc_share_sum/share_num*100)

    par_bars = [100-seq_bars[i]-pc_bars[i] for i in range(len(possible_n))]
    
    # print((seq_bars,pc_bars,par_bars))
    return seq_bars,pc_bars,par_bars

def share_of_progress_problem_data(parallel_data,sequential_data,problem,n=10**6):
    """
    For a given problem, gets the geometric proportion what the best speedups

    :parallel_data: *simulated* parallel dataset
    :sequential_data: sequential dataset
    :problem: problem number
    :n: problem size
    :returns: tuple of 2 geometric proportions: sequential, and max PC processors
    """
    # print(problem)
    seq_curve = problem_relative_speedup_data(parallel_data,sequential_data,problem,n,p=1)
    # print(seq_curve)
    seq_speedup = seq_curve[max(seq_curve.keys())][0]
    pc_curve = problem_relative_speedup_data(parallel_data,sequential_data,problem,n,p=MOST_PC_PROC)
    # print(pc_curve)
    pc_speedup = pc_curve[max(pc_curve.keys())][0]
    top_curve = problem_relative_speedup_data(parallel_data,sequential_data,problem,n,p=MOST_TOP_PROC)
    # print(top_curve)
    top_speedup = top_curve[max(top_curve.keys())][0]

    # print(seq_speedup)
    # print(pc_speedup)
    # print(top_speedup)

    assert seq_speedup <= pc_speedup
    assert pc_speedup <= top_speedup
    
    # print("TYPES:::::")
    # print(type(seq_speedup))
    # print(type(pc_speedup))
    # print(type(top_speedup))

    # print((seq_speedup,pc_speedup,top_speedup))
    if top_speedup == seq_speedup:
        return None, None
    return log(seq_speedup,top_speedup), log(pc_speedup,top_speedup)
