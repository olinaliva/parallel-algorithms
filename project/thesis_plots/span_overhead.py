from header import *

# dataset: problem dataset

# for each problem, it gets the best span algorithm, then figures out in which
# bin to put it based on its span and its work overhead. computes a histogram.

SMALL_CATEGORIES = {
    "constant": 0,
    # "log log": 0.1,
    "log": 1,
    "polylog": 5,
    "linear": 10,
    # "subexp": 100,
    "exponential": 10000,
}

# this is the big matrix
def span_overhead_matrix(data,categories=SMALL_CATEGORIES):
    """
    Plots a 2D heatmap histogram with the best span category on one side and its
    work overhead on the other.

    :data: problem dataset
    :categories: complexity categories to be used, as a dict mapping their names
            to their max code (e.g. "log": 1)
    """
    names = list(data.keys())
    upper_limit_list = sorted(categories.values())
    label_list = sorted(categories.keys(), key=lambda item: categories[item])
    m_size = len(label_list)
    so_matrix = np.zeros((m_size,m_size))

    for name in names:
        bs_sp = data[name]["bs span"]
        sp_ind = bisect.bisect_left(upper_limit_list, bs_sp)
        bs_oh = data[name]["bs overhead"]
        print(bs_oh)
        oh_ind = bisect.bisect_left(upper_limit_list, bs_oh)
        so_matrix[sp_ind][oh_ind] += 1
    so_matrix = so_matrix/sum(sum(so_matrix))*100

    so_matrix_totals = np.zeros((m_size+1,m_size+1))
    so_matrix_totals[:m_size,:m_size] = so_matrix
    for i in reversed(range(m_size)):
        so_matrix_totals[i,-1] = sum(so_matrix[i,:m_size+1])
        so_matrix_totals[-1,i] = sum(so_matrix[:m_size+1,i])
        if so_matrix_totals[i,-1]==0 and so_matrix_totals[-1,i]==0:
            so_matrix_totals = np.delete(so_matrix_totals,(i),axis=0)
            so_matrix_totals = np.delete(so_matrix_totals,(i),axis=1)
            upper_limit_list.pop(i)
            label_list.pop(i)
            m_size -= 1
    assert round(sum(so_matrix_totals[m_size,:m_size+1]))==100
    assert round(sum(so_matrix_totals[:m_size+1,m_size]))==100
    so_matrix_totals[-1,-1] = 100

    # print(so_matrix_totals)

    plt.style.use('default')
    _, ax = plt.subplots(1,1,figsize=(6.5,5),dpi=200,layout='tight')
    _ = ax.imshow(so_matrix_totals)    
    ax.set_xticks(np.arange(m_size+1))
    ax.set_yticks(np.arange(m_size+1))
    ax.set_xticklabels(label_list+["Total"])
    ax.set_yticklabels(label_list+["Total"])
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)    
    ax.xaxis.set_label_position('top') 
    ax.set_xlabel("Overhead")
    ax.set_ylabel("Span")
    ax.set_title("Work Overhead among Algorithms with the Lowest Span\nfor all Problems")
    
    ax.add_patch(Rectangle((m_size-0.5,-0.5),1,m_size+1,fill=False,edgecolor='white',lw=3,zorder=5))
    ax.add_patch(Rectangle((-0.5,m_size-0.5),m_size+1,1,fill=False,edgecolor='white',lw=3,zorder=5))

    for i in range(m_size+1):
        for j in range(m_size+1):
            ax.text(j, i, str(round(so_matrix_totals[i, j])),
                        ha="center", va="center", color="w", size=20)
    plt.savefig(SAVE_LOC+'span_tradeoff_matrix.png')
    # plt.show()

# print(span_overhead_matrix(aux_data))

