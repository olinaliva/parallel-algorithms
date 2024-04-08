from header import *
# from thesis_plots.relative_speedup import *
from project.thesis_plots.improved_families import *


# pareto frontier (points which are not strictly dominated)

# returns the percentage of algos with a work-span tradeoff
def pareto_frontier_current_fractions(par_data,seq_data,decade_list):
    fractions = new_pareto_frontier_data(par_data,seq_data,decade_list)
    return str(fractions[-1]*100)+"%"


# The percentage of problem families in each decade that have a span-work tradeoff
# between algorithms on the Pareto frontier
def pareto_frontier_graph(par_data,seq_data,decade_list): #(data,decade_list,problems):
    # fractions = pareto_frontier_data(data,decade_list,problems)
    fractions = new_pareto_frontier_data(par_data,seq_data,decade_list)

    # print(fractions)

    first_nonzero_ind = next((i for i, x in enumerate(fractions) if x), None)
    fractions = fractions[first_nonzero_ind:]
    decade_list = decade_list[first_nonzero_ind:]

    dec_num = len(decade_list)
    plt.style.use('default')
    fig, ax = plt.subplots(1,1,figsize=(6,4.5),dpi=200,layout='tight')
    ax.bar(range(dec_num), [x*100 for x in fractions], color=SEQ_PAR_COLORS[1], align='center')
    ax.set_title("Problems with Work-Span Tradeoffs per Decade")
    ax.set_xticks(range(dec_num),[x["label"] for x in decade_list])
    ax.set_xlabel("Decade")
    ax.set_ylabel("Percentage of Problems with Tradeoffs")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.savefig(SAVE_LOC+'work_span_tradeoffs.png')
    # plt.show()


# The percentage of problem families in each decade that have a span-work tradeoff
# between algorithms on the Pareto frontier
def old_pareto_frontier_data(data,decade_list,problems):
    # print("somehow starting pareto frontier data")
    names = list(data.keys())
    names.sort(key= lambda name: (data[name]["year"], -1*data[name]["span"]))

    best_stats, first_stats = span_work_improvements(data)
    # returns: best_stats - dict by problem of dict by year of {"bs alg": name, "bw alg": name}
    #          first_stats - dict mapping problem to name of its first algorithm

    # print(best_stats['APSP'][2024])

    fractions = []
    for dec in decade_list:
        # print("decade "+str(dec))
        year = dec["max"] if dec["max"] <= CUR_YEAR else CUR_YEAR
        not_frontier_count = 0
        valid_pr_count = 0
        frontier_count = 0
        for problem in problems:
            if data[first_stats[problem]]["year"] <= year:
                valid_pr_count += 1
                bs_alg = best_stats[problem][year]["bs alg"]
                bw_alg = best_stats[problem][year]["bw alg"]
                # print(" bs span: "+str(data[bs_alg]["span"])+"bw work: "+str(data[bw_alg]["work"]))

                # need to change this condition
                # currently not checking if there are any other algos with the same span and work
                # check every single algorithm
                for name in names:
                    if (data[name]["problem"] == problem) and (data[name]["year"] <= year) and (
                        data[name]["work"]==data[bw_alg]["work"]) and (
                        data[name]["span"]==data[bs_alg]["span"]):
                        not_frontier_count += 1
                        # print(problem)
                        break
        # print(valid_pr_count)
        # print(not_frontier_count)


        if valid_pr_count > 0:
            fractions.append((valid_pr_count-not_frontier_count)/valid_pr_count)
        else:
            fractions.append(0)
    
    return fractions


def new_pareto_frontier_data(par_data,seq_data,decade_list):
    fractions = []
    for dec in decade_list:
        year = dec["max"] if dec["max"] <= CUR_YEAR else CUR_YEAR

        dec_par_data = {name: par_data[name] for name in par_data if par_data[name]["year"] <= year}
        dec_seq_data = {name: seq_data[name] for name in seq_data if seq_data[name]["year"] <= year}
        dec_prob_dict = create_aux_data(dec_par_data,dec_seq_data)
        # print("For decade "+str(dec))
        # if year == 1970:
        #     print(dec_prob_dict)
        valid_pr_count = len(dec_prob_dict)
        frontier_count = 0
        for prob in dec_prob_dict:
            if dec_prob_dict[prob]["bs work"] != dec_prob_dict[prob]["best seq"]:
                frontier_count += 1             

            # if year == 1970:
            #     print("==================")
            #     print(dec_prob_dict[prob]["bs work"])
            #     print(dec_prob_dict[prob]["best seq"])
            #     print(frontier_count)

        if valid_pr_count > 0:
            fractions.append(frontier_count/valid_pr_count)
        else:
            fractions.append(0)

    return fractions


