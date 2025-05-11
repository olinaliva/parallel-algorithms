from header import *
import matplotlib.cm as cm
from collections import defaultdict

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
        # aspects_list = [algs[name][aspect] if algs[name][aspect] is not None else 
        #           algs[name]["best seq"] for name in names]
        aspects_list = [algs[name][aspect] for name in names]
        aspects_list.sort() #this sort matters 'cuz it establishes ordering of categories
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
        aspects_list = [algs[name][aspect] for name in names]
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

def NEW_w_seq_span_comparison_best_vs_work_efficient(algs):
    num = len(algs)
    names = list(algs.keys())
    fun = complexity_category_1

    categories_dict = {}
    for aspect in ["bs span", "we span", "best seq"]:
        aspects_list = [algs[name][aspect] for name in names]
        aspects_list.sort()
        for raw_aspect in aspects_list:
            category = fun(raw_aspect)
            if category not in categories_dict:
                categories_dict[category] = {"bs span": 0, "we span": 0, "best seq": 0}
            categories_dict[category][aspect] += 1

    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(6.5, 6), dpi=200, layout='tight')  # Flatter graph

    categories = list(categories_dict.keys())
    best_span_values = [categories_dict[x]["bs span"] / num * 100 for x in categories]
    we_span_values = [categories_dict[x]["we span"] / num * 100 for x in categories]
    best_seq_values = [categories_dict[x]["best seq"] / num * 100 for x in categories]

    # Positioning for stacked bars
    y_positions = [0.8, 0.5, 0.2]  # Keeping them balanced
    # bar_height = 0.15  # Thin bars
    bar_height = 0.25 # thicker bars
    
    bottom_best = 0
    bottom_we = 0
    bottom_seq = 0 
    patches = []

    # Define category groups
    pre_linear = ["constant","logarithmic", "polylog","sublinear"]
    linear_group = ["linear", "quadratic", "cubic","supracubic/\nexponential"]
    # supercubic = ["supracubic/\nexponential"]

    # Generate color gradients for each group
    # pre_linear_colors = {cat: cm.Blues(i) for cat, i in zip(pre_linear, np.linspace(0.4, 1, len(pre_linear)))}
    #flips colors
    pre_linear_colors = {
        cat: cm.Blues(i)
        for cat, i in zip(pre_linear, np.linspace(0.4, 1, len(pre_linear))[::-1])
    }
    linear_colors = {cat: cm.Greens(i) for cat, i in zip(linear_group, np.linspace(0.4, 1, len(linear_group)))}
    # supercubic_colors = {cat: cm.Reds(i) for cat, i in zip(supercubic, np.linspace(0.4, 1, len(supercubic)))}

    # Combine into one dictionary
    # GRADIENT_COLORS = {**pre_linear_colors, **linear_colors, **supercubic_colors}
    GRADIENT_COLORS = {**pre_linear_colors, **linear_colors}

    # for i in range(len(categories)):
    #     color = GRADIENT_COLORS[categories[i]]
    #     ax.barh(y_positions[0], best_span_values[i], height=bar_height, color=color, left=bottom_best)
    #     ax.barh(y_positions[1], we_span_values[i], height=bar_height, color=color, left=bottom_we)
    #     ax.barh(y_positions[2], best_seq_values[i], height=bar_height, color=color, left=bottom_seq)
    #     bottom_best += best_span_values[i]
    #     bottom_we += we_span_values[i]
    #     bottom_seq += best_seq_values[i]
    #     patches.append(mpatches.Patch(color=color, label=categories[i]))

    category_max_bar = {}  # category -> (bar_index, value, left, y_position)
    for i in range(len(categories)):
        cat = categories[i]
        color = GRADIENT_COLORS[cat]

        vals = [best_span_values[i], we_span_values[i], best_seq_values[i]]
        y_locs = y_positions
        bottoms = [bottom_best, bottom_we, bottom_seq]

        for j, (y, val, bottom) in enumerate(zip(y_locs, vals, bottoms)):
            ax.barh(y, val, height=bar_height, color=color, left=bottom)
            bottoms[j] += val

            if cat not in category_max_bar or val > category_max_bar[cat][1]:
                category_max_bar[cat] = (j, val, bottom, y)

        bottom_best, bottom_we, bottom_seq = bottoms
    
    # Track right edge positions of bars for each category at each y-position
    category_edges = defaultdict(dict)  # category -> {y_position: (right_edge_x)}

    # Rebuild positions of bars (starting from zero each time)
    bottoms = [0, 0, 0]  # for each of the 3 bars

    for i, cat in enumerate(categories):
        vals = [best_span_values[i], we_span_values[i], best_seq_values[i]]

        for j, val in enumerate(vals):
            if val == 0:
                continue
            y = y_positions[j]
            left = bottoms[j]
            right = left + val
            category_edges[cat][y] = right
            bottoms[j] += val

    # Now draw dashed lines between right edges of matching categories
    for cat in categories:
        # From Span to Work-Efficient Span
        if y_positions[0] in category_edges[cat] or y_positions[1] in category_edges[cat]:
            x1 = category_edges[cat].get(y_positions[0], 0)
            x2 = category_edges[cat].get(y_positions[1], 0)
            y1 = y_positions[0] - bar_height / 2  # bottom of Span
            y2 = y_positions[1] + bar_height / 2  # top of Work-Efficient Span
            ax.plot([x1, x2], [y1, y2], linestyle='--', color='black', linewidth=0.8, alpha=0.6, zorder=3)

        # From Work-Efficient Span to Serial Runtime
        if y_positions[1] in category_edges[cat] or y_positions[2] in category_edges[cat]:
            x1 = category_edges[cat].get(y_positions[1], 0)
            x2 = category_edges[cat].get(y_positions[2], 0)
            y1 = y_positions[1] - bar_height / 2  # bottom of WE Span
            y2 = y_positions[2] + bar_height / 2  # top of Serial
            ax.plot([x1, x2], [y1, y2], linestyle='--', color='black', linewidth=0.8, alpha=0.6, zorder=3)

    for cat, (bar_idx, val, left, y) in category_max_bar.items():
        if cat == "supracubic/\nexponential":
            # # Draw line down from center of bar
            # ax.annotate('', xy=(left + val / 2, y - bar_height / 2), xytext=(left + val / 2 - 4, y - 0.5),
            #             arrowprops=dict(arrowstyle='-', color='black', lw=0.8), zorder=4)
            # # Write text under the arrow
            # ax.text(left + val / 2 - 4, y - 0.32, cat, ha='center', va='top', fontsize=7, color='black', zorder=5)
            ax.text(left + val/2-2, y-0.05, cat, ha='center', va='center', fontsize=7, color='white', zorder=5)
        else: 
            ax.text(left + val/2, y, cat, ha='center', va='center', fontsize=7, color='white', zorder=5)
    #this was for autosensing small category
    # for cat, (bar_idx, val, left, y) in category_max_bar.items():
    #     center_x = left + val / 2

    #     if val > 15:  # If there's enough room, write inside
    #         ax.text(center_x, y, cat, ha='center', va='center', fontsize=7, color='white', zorder=5)
    #     else:
    #         # Draw line down from center of bar
    #         ax.annotate('', xy=(center_x, y - bar_height / 2), xytext=(center_x, y - 0.5),
    #                     arrowprops=dict(arrowstyle='-', color='black', lw=0.8), zorder=4)
    #         # Write text under the arrow
    #         ax.text(center_x, y - 0.52, cat, ha='center', va='top', fontsize=7, color='black', zorder=5)


    # Adjust y-axis labels
    ax.set_yticks(y_positions)
    ax.set_yticklabels(["Span", "Work-Efficient\nSpan", "Serial\nRuntime"])

    # # Move legend outside to the right
    # # ax.legend(handles=patches, title="Complexity Class", loc="center left", bbox_to_anchor=(1.05, 0.5))
    # ax.legend(handles=patches, title="Complexity Class", loc="center left", bbox_to_anchor=(1.05, 0.5),
    #       ncol=2, fontsize=8, frameon=False)
    # #legend under graph
    # # ax.legend(handles=patches, title="Complexity Class", loc="upper center", bbox_to_anchor=(0.5, -0.2),
    #     #   ncol=len(patches), fontsize=8, frameon=False)
    
    ax.set_title("Best Span, Work-efficient Span and Serial Runtime for All Problems", fontsize=10)
    ax.set_xlabel("Percentage of Algorithm Problems")
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    
    plt.tight_layout()
    # plt.savefig(SAVE_LOC + 'NEW_w_seq_span_comparison_stacked.png')
    plt.savefig(SAVE_LOC + 'NEW_w_seq_span_comparison_stacked.png', bbox_inches='tight')
    # plt.show()