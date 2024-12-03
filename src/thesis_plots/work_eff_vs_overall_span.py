from header import *

# dataset: neither, but problem-dataset should be generated from the simulated dataset


# compares the following (one data point for each for each problem):
# 1. for the best span algorithm, plot span, 
# 2. for the work-efficient algorithm, the best span
# it plots the histogram of the above aspects of a problem

# data: this is problem-data (not algorithm-data)
# only_we: True if we only want to consider problems that have a work-efficient
# algorithm. The default is False (considering all problems)
def span_comparison_best_vs_work_efficient(algs):
    num = len(algs)
    names = list(algs.keys())
    fun = complexity_category_1
    
    categories_dict = {}
    for aspect in ["bs span","we span"]:
        aspects_list = [algs[name][aspect] if algs[name][aspect] is not None else 
                  algs[name]["best seq"] for name in names]
        aspects_list.sort()
        for raw_aspect in aspects_list:
            category = fun(raw_aspect)
            if category not in categories_dict:
                categories_dict[category] = {"bs span":0, "we span":0}
            categories_dict[category][aspect] += 1

    plt.style.use('default')
    fig, ax = plt.subplots(1,1,figsize=(6.5,4.25),dpi=200,layout='tight')
    for i in range(2):
        aspect = ["bs span","we span"][i]
        aspect_num = sum(categories_dict[x][aspect] for x in categories_dict)
        assert aspect_num == num
        aspect_values = [categories_dict[x][aspect]/aspect_num*100 for x in categories_dict]
        ax.bar(categories_dict.keys(), aspect_values, width=0.8*i-0.4,align='edge',color=COLORS[i])

    # legend
    handles = []
    handles.append(mpatches.Patch(color=COLORS[0], label="Fastest Algorithm (Best Span)"))
    handles.append(mpatches.Patch(color=COLORS[1], label="Most Efficient Algorithm"))
    ax.legend(handles=handles)

    ax.set_title("Best Span vs Best Work-efficient Algorithm Span\nfor all Problems")
    ax.set_xticks(ax.get_xticks(), categories_dict.keys(), rotation=90)
    # ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_yticks(ax.get_yticks(),["{:.0f}".format(x)+"%" for x in ax.get_yticks()])
    ax.set_xlabel("Best Span Complexity Class")
    ax.set_ylabel("Percentage of Algorithm Problems")
    plt.savefig(SAVE_LOC+'span_comparison.png')
    # plt.show()