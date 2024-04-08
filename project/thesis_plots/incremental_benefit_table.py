from header import *

# dataset: specific algorithm only


# given some base n, computes the relative speedup for some values of p and
# some increase factors to n. computes the speedup as follows:
# speedup = (work_fn(base_n) + span_fn(base_n)) / (work_fn(n)/p + span_fn(n))

# this one is a table
# incremental benefit from strong scaling
def incremental_benefit_scaling(data,alg_name,base_n=10**3,p_values=[1,8,64,2**20],n_factor_values=[1,2,10,100,1000]):
    """
    Generates a table showing the relative speedup possible when increasing the
    number of processors and/or the problem size

    :data: dataset to use for the algorithm (original dataset)
    :alg_name: name of the algorithm for which analysis is needed
    :base_n: initial problem size
    :p_values: considered values for the number of processors
    :n_factor_values: considered values for increase factors to the problem size
    """
    span_fn = get_comp_fn(data[alg_name]["span"])
    span = data[alg_name]["span"]
    work_fn = get_comp_fn(data[alg_name]["work"])
    work = data[alg_name]["work"]

    table = np.zeros((len(p_values),len(n_factor_values)))
    p_labels = []
    for i in range(len(p_values)):
        p = p_values[i]
        p_labels.append("$1 \\rightarrow$ "+str(p))
        for j in range(len(n_factor_values)):
            n = base_n*n_factor_values[j]
            speedup = get_runtime(work,span,base_n,1) / get_runtime(work,span,n,p)
            table[i][j] = round(speedup,2-int(floor(log10(abs(speedup)))))

    p_labels[0] = "1 processor"
    n_labels = [str(i)+"$\\times$" for i in n_factor_values]
    
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    
    df = pd.DataFrame(table, columns=n_labels, index=p_labels)
    ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='top')
    ax.set_title("Problem size",pad=70)
    fig.tight_layout()
    plt.show()


