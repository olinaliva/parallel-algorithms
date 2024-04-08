from header import *

# data: this is problem-data (not algorithm-data)
def new_parallelism_graph(algs):
    num = len(algs)
    names = list(algs.keys())
    fun = complexity_category_1

    cat_list = get_category_1_list()
    
    categories_dict = {}
    for aspect in ["bs par","we par"]:
        aspects_list = sorted([algs[name][aspect] for name in names])
        for raw_aspect in aspects_list:
            category = fun(raw_aspect)
            if category not in categories_dict:
                categories_dict[category] = {"bs par":0, "we par":0}
            categories_dict[category][aspect] += 1

    i = 0
    while i < len(cat_list):
        if cat_list[i] not in categories_dict:
            del cat_list[i]
        else:
            i+=1

    plt.style.use('default')
    fig, ax = plt.subplots(1,1,figsize=(6.5,5),dpi=200,layout='tight')
    for i in range(2):
        aspect = ["bs par","we par"][i]
        aspect_num = sum(categories_dict[x][aspect] for x in cat_list)
        assert aspect_num == num
        aspect_values = [categories_dict[x][aspect]/aspect_num*100 for x in cat_list]
        ax.bar(cat_list, aspect_values, width=0.8*i-0.4,align='edge',color=COLORS[i])

    # legend
    handles = []
    handles.append(mpatches.Patch(color=COLORS[0], label="Best Span Algorithm"))
    handles.append(mpatches.Patch(color=COLORS[1], label="Work-efficient Algorithm"))
    ax.legend(handles=handles)

    ax.set_title("Available Parallelism for Best Span vs \n Work-efficient Algorithms for all Problems")
    ax.set_xticks(ax.get_xticks(), cat_list)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    # ax.set_yticks(ax.get_yticks(),['{:,.1%}'.format(x) for x in ax.get_yticks()])
    ax.set_xlabel("Available Parallelism Complexity Class")
    ax.set_ylabel("Percentage of Problems")
    plt.savefig(SAVE_LOC+'parallelism_comparison.png')
    # plt.show()
    pass