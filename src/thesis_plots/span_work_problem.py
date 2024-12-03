from header import *


# for a given problem, this plots each algorithm as a dot


# same as the initial graph, but in one model only and showing the explicit
# pareto frontier line
# should use the non-simulated dataset
def problem_work_vs_span_pareto_frontier(par_data,seq_data,problem):
    seq_algs = {k: v for k, v in seq_data.items() if v["problem"]==problem}
    best_seq = min(seq_algs,key=lambda k: seq_algs[k]["time"])

    (spans, span_complexities, works, work_complexities, colors, years, 
            used_models, pareto_spans,pareto_works) = pareto_frontier_helper(par_data,seq_data,problem)

    plt.style.use('default')
    fig, ax = plt.subplots(1,1,figsize=(7,4.5),dpi=200,layout='tight')
    # ax.grid(alpha=0.4)
    ax.scatter(spans,works,c=colors,zorder=100,edgecolors='black',linewidth=0.7)
    ax.step(pareto_spans,pareto_works)
    # ax.vlines(x=leftmost_pnt[0],ymin=leftmost_pnt[1],ymax=max(spans)+1)
    # ax.hlines(y=rightmost_pnt[1],xmin=rightmost_pnt[0],xmax=max(works)+2)

    span_ranges = list(range(0,len(span_complexities)))
    work_ranges = list(range(0,len(work_complexities)))
    ax.set_xticks(span_ranges,span_complexities, rotation=90)
    ax.set_yticks(work_ranges,work_complexities)
    ax.set_ylabel("Work Complexity")
    ax.set_xlabel("Span Complexity")
    ax.set_title("Work - Span Tradeoff for Parallel Algorithms\nfor the "+problem_dict[problem]+" Problem")
    done = set()
    for i in range(len(years)):
        if (spans[i],works[i]) not in done:
            ax.annotate(years[i],(spans[i],works[i]),zorder=101)
            done.add((spans[i],works[i]))
    ax.annotate(seq_algs[best_seq]["year"],(spans[-1],works[-1]),zorder=101)

    ax.set_xlim([min(spans)-0.5, max(spans)+0.5])
    ax.set_ylim([min(works)-0.5, max(works)+0.5])

    # legends
    handles = []
    for i in used_models:
        new_patch = mpatches.Patch(color=str(MODEL_COLORS[i]), label=model_dict[i])
        handles.append(new_patch)
    ax.legend(handles=handles, title="Models")#,loc='lower left', bbox_to_anchor=(1, 0.5))

    plt.savefig(SAVE_LOC+'span_vs_work_pareto.png')
    # plt.show()
    pass

# TODO: use allowed_models
def pareto_frontier_helper(par_data,seq_data,problem,allowed_models=set(model_dict.keys())):
    algs = {k: v for k, v in par_data.items() if v["problem"]==problem}# and v["model"]!=600 and v["sim"]==0} # TODO: also 700?
    seq_algs = {k: v for k, v in seq_data.items() if v["problem"]==problem}
    best_seq = min(seq_algs,key=lambda k: seq_algs[k]["time"])
    best_seq_time = seq_algs[best_seq]["time"]
    # local_colors = list(mcolors.TABLEAU_COLORS.values())

    names = list(algs.keys())
    names.sort(key= lambda name: (algs[name]["year"], -1*algs[name]["span"], -1*algs[name]["work"]))
    years = [algs[name]["year"] for name in names]
    spans, span_complexities = standardize_comp([algs[name]["span"] for name in names]+[best_seq_time])
    works, work_complexities = standardize_comp([algs[name]["work"] for name in names]+[best_seq_time])

    models = [algs[name]["model"] for name in names]+[800]
    used_models = list(set(models))
    used_models.sort()
    complexity_models = [model_dict[mod] for mod in used_models]
    colors = [MODEL_COLORS[model] for model in models]

    # computing the pareto frontier
    pareto_points = set() # set of (x,y) tuples
    all_points = [(spans[i],works[i]) for i in range(len(names)+1)]
    # go through every "span":
    span_values = set(spans)
    prev_pareto_wk = max(works)
    for sp in sorted(list(span_values)):
        par_wk = min([y for x,y in all_points if x==sp])
        if par_wk < prev_pareto_wk:
            pareto_points.add((sp,par_wk))
            prev_pareto_wk = par_wk
    # works
    work_values = set(works)
    prev_pareto_sp = max(spans)
    for wk in sorted(list(work_values)):
        par_sp = min([x for x,y in all_points if y==wk])
        if par_sp < prev_pareto_sp:
            pareto_points.add((par_sp,wk))
            prev_pareto_sp = par_sp
    print(pareto_points)

    # computing the points to be plotted
    ordered_pareto_pnts = sorted(pareto_points,key=lambda elem:(elem[0],-elem[1]))
    pareto_spans = [x[0] for x in ordered_pareto_pnts]+[ordered_pareto_pnts[-1][0]]
    pareto_works = [ordered_pareto_pnts[0][1]]+[x[1] for x in ordered_pareto_pnts]

    # endpoints
    leftmost_pnt = min(pareto_points,key=itemgetter(0))
    rightmost_pnt = min(pareto_points,key=itemgetter(1))

    return (spans, span_complexities, works, work_complexities, colors, years, 
            used_models, pareto_spans,pareto_works)


# work vs span for 1 individual problem
def problem_work_vs_span(data,problem,aux_data):
    algs = {k: v for k, v in data.items() if v["problem"]==problem}
    name = problem_dict[problem]
    best_seq = aux_data[problem]["best seq"]

    names = list(algs.keys())
    names.sort(key= lambda name: (algs[name]["year"], -1*algs[name]["span"]))
    years = [algs[name]["year"] for name in names]
    ghosts = [algs[name]["sim"] for name in names]
    spans, span_complexities = standardize_comp([algs[name]["span"] for name in names]+[best_seq])
    works, work_complexities = standardize_comp([algs[name]["work"] for name in names]+[best_seq])
    models = [algs[name]["model"] for name in names]
    used_models = list(set(models))
    used_models.sort()
    complexity_models = [model_dict[mod] for mod in used_models]
    colors = [MODEL_COLORS[model] for model in models]

    # points = len(years)
    # assert len(spans) == points
    # assert len(works) == points
    # assert len(models) == points
    
    plt.style.use('default')
    fig, ax = plt.subplots(1,1)
    ax.grid(alpha=0.4)
    ax.scatter([spans[i] for i in range(len(spans)) if ghosts[i]==1], 
            [works[i] for i in range(len(works)) if ghosts[i]==1], 
            c=[colors[i] for i in range(len(colors)) if ghosts[i]==1], 
            marker='s',s=121,zorder=99,edgecolors='black',linewidth=0.7)
    ax.scatter([spans[i] for i in range(len(spans)) if ghosts[i]==0], 
            [works[i] for i in range(len(works)) if ghosts[i]==0], 
            c=[colors[i] for i in range(len(colors)) if ghosts[i]==0], 
            marker='o',zorder=100,edgecolors='black',linewidth=0.7)
    ax.set_title(name + " - Work vs Span")
    
    span_ranges = list(range(0,len(span_complexities)))
    work_ranges = list(range(0,len(work_complexities)))
    ax.set_xticks(span_ranges,span_complexities, rotation=90)
    ax.set_yticks(work_ranges,work_complexities)
    # ax.set_xticklabels(span_complexities, rotation=90)
    # ax.set_yticklabels(work_complexities)
    ax.set_ylabel("Work Complexity Class")
    ax.set_xlabel("Span Complexity Class")
    for i in range(len(algs)):
        ax.annotate(years[i],(spans[i],works[i]),zorder=101)

    # legends
    handles = []
    for i in used_models:
        new_patch = mpatches.Patch(color=str(MODEL_COLORS[i]), label=model_dict[i])
        handles.append(new_patch)
    model_legend = ax.legend(handles=handles,loc='lower left', bbox_to_anchor=(1, 0.5), title="Models")
    ax.add_artist(model_legend)
    pub_symbol = mlines.Line2D([], [], color='#ffff00', marker='o', linestyle='None',
                            markersize=6,markeredgecolor='black',linewidth=0.7, label='Published algorithms')
    sim_symbol = mlines.Line2D([], [], color='#ffff00', marker='s', linestyle='None',
                            markersize=9,markeredgecolor='black',linewidth=0.7, label='Simulated algorithms')
    handles=[pub_symbol, sim_symbol]
    ax.legend(handles=handles,loc='upper left', bbox_to_anchor=(1, 0.5), title="Symbols")
    plt.show()
    
