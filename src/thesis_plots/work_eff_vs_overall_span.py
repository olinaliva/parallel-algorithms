from header import *
import matplotlib.cm as cm

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

    ax.set_title("Best Span vs Best Work-efficient Algorithm Span\nfor all (Parallel) Problems")
    ax.set_xticks(ax.get_xticks(), categories_dict.keys(), rotation=90)
    # ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_yticks(ax.get_yticks(),["{:.0f}".format(x)+"%" for x in ax.get_yticks()])
    ax.set_xlabel("Best Span Complexity Class")
    ax.set_ylabel("Percentage of Algorithm Problems")
    plt.savefig(SAVE_LOC+'span_comparison.png')
    # plt.show()

def NEW_span_comparison_best_vs_work_efficient(algs):
    num = len(algs)
    names = list(algs.keys())
    fun = complexity_category_1

    categories_dict = {}
    for aspect in ["bs span", "we span"]:
        aspects_list = [algs[name][aspect] if algs[name][aspect] is not None else 
                        algs[name]["best seq"] for name in names]
        aspects_list.sort()
        for raw_aspect in aspects_list:
            category = fun(raw_aspect)
            if category not in categories_dict:
                categories_dict[category] = {"bs span": 0, "we span": 0}
            categories_dict[category][aspect] += 1

    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(6.5, 2), dpi=200, layout='tight')  # Flatter graph

    categories = list(categories_dict.keys())
    best_span_values = [categories_dict[x]["bs span"] / num * 100 for x in categories]
    we_span_values = [categories_dict[x]["we span"] / num * 100 for x in categories]

    # Positioning for stacked bars
    y_positions = [0.6, 0.4]  # Keeping them balanced
    bar_height = 0.15  # Thin bars
    
    bottom_best = 0
    bottom_we = 0
    patches = []

    # # Define category groups
    # pre_linear = ["log", "sublinear"]
    # linear_group = ["linear", "quadratic", "cubic"]
    # supercubic = ["supercubic"]

    # # Generate color gradients for each group
    # pre_linear_colors = [cm.Blues(i) for i in np.linspace(0.4, 1, len(pre_linear))]
    # linear_colors = [cm.Greens(i) for i in np.linspace(0.4, 1, len(linear_group))]
    # supercubic_colors = [cm.Reds(i) for i in np.linspace(0.4, 1, len(supercubic))]
    # GRADIENT_COLORS = pre_linear_colors + linear_colors + supercubic_colors

    # Define category groups
    pre_linear = ["constant","logarithmic", "polylog","sublinear"]
    linear_group = ["linear", "quadratic", "cubic"]
    supercubic = ["supracubic/\nexponential"]

    # Generate color gradients for each group
    pre_linear_colors = {cat: cm.Blues(i) for cat, i in zip(pre_linear, np.linspace(0.4, 1, len(pre_linear)))}
    linear_colors = {cat: cm.Greens(i) for cat, i in zip(linear_group, np.linspace(0.4, 1, len(linear_group)))}
    supercubic_colors = {cat: cm.Reds(i) for cat, i in zip(supercubic, np.linspace(0.4, 1, len(supercubic)))}

    # Combine into one dictionary
    GRADIENT_COLORS = {**pre_linear_colors, **linear_colors, **supercubic_colors}

    for i in range(len(categories)):
        color = GRADIENT_COLORS[categories[i]]
        ax.barh(y_positions[0], best_span_values[i], height=bar_height, color=color, left=bottom_best)
        ax.barh(y_positions[1], we_span_values[i], height=bar_height, color=color, left=bottom_we)
        bottom_best += best_span_values[i]
        bottom_we += we_span_values[i]
        patches.append(mpatches.Patch(color=color, label=categories[i]))

    # Adjust y-axis labels
    ax.set_yticks(y_positions)
    ax.set_yticklabels(["Best Span", "Work-Efficient Span"])

    # Move legend outside to the right
    # ax.legend(handles=patches, title="Complexity Class", loc="center left", bbox_to_anchor=(1.05, 0.5))
    ax.legend(handles=patches, title="Complexity Class", loc="center left", bbox_to_anchor=(1.05, 0.5),
          ncol=2, fontsize=8, frameon=False)
    #legend under graph
    # ax.legend(handles=patches, title="Complexity Class", loc="upper center", bbox_to_anchor=(0.5, -0.2),
        #   ncol=len(patches), fontsize=8, frameon=False)

    ax.set_title("Best Span vs Work-efficient Span for All Problems", fontsize=10)
    ax.set_xlabel("Percentage of Algorithm Problems")
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    
    plt.savefig(SAVE_LOC + 'NEW_span_comparison_stacked.png')
    # plt.show()