from header import *


################################################################################
########### Histograms #########################################################
################################################################################

# histogram of the given aspect (e.g. "span", "work") for all problems
def all_algorithms_histo(data, aspect, normalized=False):
    if aspect == "span" or aspect == "work eff":
        fun = complexity_category_1
    elif aspect == "work":
        fun = complexity_category_n
    elif aspect == "bs span" or aspect == "bs overhead":
        fun = complexity_category_1
    else:
        raise ValueError("Can't plot the historgram for this aspect of parallel algorithms: "+str(aspect))
    
    if aspect == "bs span" or aspect == "bs overhead":
        algs = data
    else:
        algs = {k: v for k, v in data.items() if v["sim"]==0}
    names = list(algs.keys())

    spans_list = sorted([algs[name][aspect] for name in names])
    span_categories_list = [fun(raw_span) for raw_span in spans_list]
    span_categories_dict = {}
    for span in span_categories_list:
        if span in span_categories_dict:
            span_categories_dict[span] += 1
        else:
            span_categories_dict[span] = 1

    if normalized:
        values = [x/len(spans_list) for x in span_categories_dict.values()]
    else:
        values = span_categories_dict.values()

    plt.style.use('default')
    fig, ax = plt.subplots(1,1)
    ax.bar(span_categories_dict.keys(), values, align='center')
    ax.set_title(aspect+" complexity frequency for all parallel algorithms")
    ax.set_xticklabels(span_categories_dict.keys(), rotation=90) # TODO: change to set_xticks(ticks, labels)
    if normalized:
        vals = ax.get_yticks()
        ax.set_yticklabels(['{:,.1%}'.format(x) for x in vals])
    # ax.hist(overhead_list,bins=4)
    plt.show()

# all_algorithms_histo(full_data, "span", normalized=False)

