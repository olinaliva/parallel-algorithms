from header import *
from project.thesis_plots.span_work_imprvmnt import *

# dataset: simulated dataset


# same as work vs span improvement heatmap, but instead of work use running time
# parametrized on p (the number of processors)
# grid of 9 such graphs with different values of p (1, 64, 4096) and n

def performance_vs_span_improvement(data,seq_data={},p_values=[1,10**3,10**6],
            n_values=[10**3,10**6,10**9],all_data=None,lower=False,pareto=None):
    """
    Generates a grid of span-performance improvement heatmap graphs for all combos
    of given values for problem size n and numbers of processors p

    :data: *simulated* parallel dataset
    :p_values: list of number of processor values
    :n_values: list of problem size values
    """
    fig, ax = plt.subplots(len(p_values),len(n_values),figsize=(7,7),dpi=200,layout='tight')
    for i in range(len(p_values)):
        p = p_values[i]
        for j in range(len(n_values)):
            # print("starting "+str(i)+","+str(j))
            n = n_values[j]
            improvement_heatmap(data,ax[i,j],measure="rt",n=n,p=p,tsize=14,
                all_data=all_data,lower=lower,pareto=pareto,seq_data=seq_data)
    
    
    if pareto is None:
        plt.savefig(SAVE_LOC+'span_performance_heatmap.png')
    else:        
        plt.savefig(SAVE_LOC+'span_performance_heatmap_pareto.png')
    # plt.show()