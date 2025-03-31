from src.thesis_plots.strong_scaling import *
from src.thesis_plots.incremental_benefit_table import *
from src.thesis_plots.span_work_imprvmnt import *
from src.thesis_plots.span_perf_imprvmnt import *
from src.thesis_plots.relative_speedup import *
from src.thesis_plots.span_overhead import *
from src.thesis_plots.share_of_progress import *
from src.thesis_plots.work_eff_vs_overall_span import *
from src.thesis_plots.improved_families import *
from src.thesis_plots.decade_progress import *
from src.thesis_plots.pareto_frontier import *
from src.thesis_plots.aggregated_relative_speedup import *
from src.thesis_plots.span_work_problem import *
from src.thesis_plots.new_parallelism import *
from src.thesis_plots.weak_scaling import *
from src.thesis_plots.models import *
from src.thesis_plots.varying_scaling import *
from src.paper_plots.average_imprvmnt_rates import *
from src.paper_plots.span_work_more_probs import *
from src.paper_plots.num_overhead_vs_span import *
from src.paper_plots.problem_overhead_vs_proc import *
from src.paper_plots.problem_speedup_vs_proc import *
from src.paper_plots.aggregate_switch_to_work_ineff import *

from converter import *
from data.processor_data_acquisition import *



# from src.processed_data import *

print("starting main")

################################################################################
################## DATA ########################################################
################################################################################

########## Refactor data
#import src.data_processing
#print(src.data_processing.raw_database.populate_raw_database_parallel())
# IDK WHAT'S GOING ON HERE
#import src.processed_data
#print(src.processed_data.raw_database.populate_raw_database_parallel())



########## End of refactor data

# print(find_proc_increase_supercomputer())
# print(find_best_top_every_year("top500_pre_2008"))

# print(find_best_top_every_year("cpu_short"))
# print(find_proc_increase_commercial())

model_sheet_name = "data/par_models_FEB18"
old_sheet_name = "past_data/parallel_sheet_for_models_JAN_8"
mod_map = {
    100: 130,
    110: 110,
    120: 120,
    130: 130,
    131: 130,
    132: 130,
    133: 130,
    135: 130,
    200: 200,
    210: 200,
    220: 200,
    300: 300,
    310: 300,
    320: 300,
    330: 300,
    400: 400,
    500: 500,
    510: 500,
    520: 500,
    600: 600,
    610: 600,
    700: 700,
    800: 600}
# make_model_plots(model_sheet_name,mod_map)

# convert_csv_to_json("data/par_algos_1")
# apply_various_operations_to_change_the_json_file_so_its_usable(name="data/par_algos_1",
#         wanted_fields=PARALLEL_ALGO_FIELDS,
#         unwanted_values=PARALLEL_DISCARABLE_FIELD_VALUES,
#         allowed_model_list = PARALLEL_ALLOWABLE_MODELS)


# create_seq_data("data/Sheet1"+VERSION,"data/Sheet1_New_Entries"+VERSION)
# create_par_data("data/Parallel_Algos"+VERSION)

def make_model_dataset(par_algos):
    jsonArray = []
    for name in par_algos:
        year = par_algos[name]["year"]
        model = par_algos[name]["model"]
        alg_id = par_algos[name]["id"]
        jsonArray.append({"year":year,"model":model,"id":alg_id})

    newJsonFilePath = r'./data/par_models_FEB18.json'
    with open(newJsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)
    pass

# make_model_dataset(simulated_par_data)

# for elem in simulated_par_data:
#     # print(simulated_par_data[elem]['id'])
#     # print(type(simulated_par_data[elem]['id']))
#     # break
#     if simulated_par_data[elem]['id'] == '533':
#         print(simulated_par_data[elem]['id'])

# create_aux_data(simulated_par_data,full_seq_data)
# create_aux_data(full_data,rel_speedup_seq_data)

################################################################################
##### FINAL GRAPH CALLS ########################################################
################################################################################

#pset = get_problems(simulated_par_data)
# print(len(pset))
# print(len(simulated_par_data))
# print(pset)

# fset = get_families(simulated_par_data)
# print(len(fset))
# print(fset)

# # 4.1
# short_decs = [{"max":CUR_YEAR,"label":"all the time"}]
# average_improvement_over_decade_graph(simulated_par_data,full_seq_data,short_decs)
# average_improvement_over_decade_graph(simulated_par_data,full_seq_data,DECADES,var_weights="thesis_weight")

# # 4.2
# available_processors(top_processor_data,pc_processor_data)

# # 4.3
# print(speedup_for_available_processors(simulated_par_data,full_seq_data,'APSP',
#                                        top_processor_data,pc_processor_data,n=10**6,seq=True))

# # 4.4
# print(speedup_for_available_processors(simulated_par_data,full_seq_data,'2-Player',
#                                        top_processor_data,pc_processor_data,n=10**6,seq=True))
# problem_relative_speedup_graph(simulated_par_data,full_seq_data,['1D Maximum Subarray'],n=10**6) # debugging
# aggregated_relative_speedup(simulated_par_data,full_seq_data,n=10**6)
# new_aggregated_relative_speedup_graph(simulated_par_data,full_seq_data,n=10**6) 

# # 5.1
# problem_work_vs_span_pareto_frontier(original_par_data,full_seq_data,'LCS')

# # 5.2 - figure out if sequential algos should be counted
# pareto_frontier_graph(simulated_par_data,full_seq_data,DECADES)
# print(pareto_frontier_current_fractions(simulated_par_data,full_seq_data,DECADES))
# print(len(get_problems(simulated_par_data)))

# # 5.3
# span_comparison_best_vs_work_efficient(full_problem_data)

# # 5.4
# span_overhead_matrix(full_problem_data)

# # 5.5
# work_span_improvement_heatmap(simulated_par_data)

# # 6.1
# bs_mst_algo_name = "14475Johnson, Metaxas (1992)"
# we_mst_algo_name = "14457Deo and Yoo (1981)" #"14.1-10-Chin et al. (1982)"
# strong_scaling(simulated_par_data,bs_mst_algo_name,pr_sizes=[10**3,10**6,10**9])
# strong_scaling_comparison(simulated_par_data,bs_mst_algo_name,we_mst_algo_name)
# weak_scaling_comparison_graph(simulated_par_data,bs_mst_algo_name,we_mst_algo_name)
# varying_scaling_comparison_graph(simulated_par_data,bs_mst_algo_name,we_mst_algo_name)

# # 6.2
# new_parallelism_graph(full_problem_data)

# # 7.1 - something seems sus... looks very different from the work plot
# print(get_impr_data(simulated_par_data,n=10**3,p=8))
# performance_vs_span_improvement(simulated_par_data,lower=True)#,p_values=[1,10],n_values=[10**3,10**9])

# # 7.2
# compound_growth_rate_distribution_graph(simulated_par_data,full_seq_data,g_buckets,n=10**3,p=2**3)
# compound_growth_rate_histo_grid(simulated_par_data,full_seq_data,g_buckets,
#                                     n_values=[10**3,10**6,10**9],p_values=[8,10**3,10**6])

# # 7.3
# share_of_progress_graph(simulated_par_data,full_seq_data,possible_n=[10**3,10**6,10**9])
# print(share_of_progress_problem_data(simulated_par_data,full_seq_data,'OBST',n=10**6))



# # NEW 5.5 and 7.1 (only Pareto algorithms)
# pareto_algorithms = pareto_frontier_pushing(simulated_par_data,full_seq_data)
# work_span_improvement_heatmap(simulated_par_data,seq_data={},pareto=pareto_algorithms)
# performance_vs_span_improvement(simulated_par_data,pareto=pareto_algorithms,lower=True)

# print(pareto_algorithms)
# work_span_improvement_heatmap(pareto_algorithms,seq_data={},all_data=simulated_par_data)
# for algo in pareto_algorithms:
#     assert algo in simulated_par_data
#     assert pareto_algorithms[algo] == simulated_par_data[algo]



################################################################################
##### PAPER GRAPHS #############################################################
################################################################################    
# #{"max": 0.001, "label": "0-0.1%"},
# histo_buckets = [
#             {"max": 0.03, "label": "0.1-3%"},
#             {"max": 0.1, "label": "3-10%"},
#             {"max": 0.3, "label": "10-30%"},
#             {"max": 1, "label": "30-100%"},
#             {"max": 3, "label": "100-300%"},
#             {"max": 10, "label": "300-1000%"},
#             {"max": math.inf, "label": ">1000%"},]
#funstion in average_improvement_rate
#yearly_impr_rate_histo_grid(simulated_par_data, histo_buckets,n_values=[10**3,10**6,10**9],
#                                p_values=[8,10**3,10**6], measure="rt")
# NEW_yearly_impr_rate_histo_grid(simulated_par_data, full_seq_data, histo_buckets,n_values=[10**3,10**6,10**9],
#                                 p_values=[8,10**3,10**6], measure="rt",start_from="first_seq")
#NEW_yearly_impr_rate_histo_grid(simulated_par_data, full_seq_data, histo_buckets,n_values=[10**3,10**6,10**9],
#                                 p_values=[8,10**3,10**6], measure="rt",start_from="best_seq")
# NEW_yearly_impr_rate_histo_grid(simulated_par_data, full_seq_data, histo_buckets,n_values=[10**3,10**6,10**9],
#                                 p_values=[8,10**3,10**6], measure="rt",start_from="first_par")
# NEW_yearly_impr_rate_histo_grid(simulated_par_data, full_seq_data, histo_buckets,n_values=[10**3,10**6,10**9],
#                                 p_values=[8,10**3,10**6], measure="rt",start_from="stacked")

# names=first_seq_names(full_seq_data)
# first_seq_times=[]
# for algo in names.values():
#     first_seq_times.append(full_seq_data[algo]["time"])

# with open("first_seq.json", "w") as json_file:
#     json.dump(first_seq_times, json_file, indent=4)
# print(f"Dictionary saved")

# n=1000
# best_stats, first_stats=improvements(simulated_par_data,n,1)
# best_seq=best_seq_names(full_seq_data)
# problems=get_problems(simulated_par_data)
# work_dict={}
# for problem in problems:
#     best=best_stats[problem][2024]["br alg"]
#     if (problem not in best_seq.keys()):
#         work_dict[problem]=("no seq",best,simulated_par_data[best]["span"],simulated_par_data[best]["work"])
#     elif (get_seq_runtime(full_seq_data[best_seq[problem]]["time"],n)>
#           get_runtime(simulated_par_data[best]["work"], simulated_par_data[best]["span"],n,1)):
#         work_dict[problem]=(best_seq[problem],full_seq_data[best_seq[problem]]["time"],best,simulated_par_data[best]["span"],simulated_par_data[best]["work"])
# print(work_dict)


#print(first_seq_names(full_seq_data))
#print("checkpoint 1")
#funtions in span_work_more_probs
# span_vs_work_multiple_probs(simulated_par_data,full_seq_data,
#                 problems=['Topological Sorting','LCS','Bipartite Graph MCM'])
# span_vs_work_multiple_probs_pareto_frontier(simulated_par_data,full_seq_data,
#                 problems=['Topological Sorting','LCS','Bipartite Graph MCM'])
#print("checkpoint 2")
#function in numerical_overhead_vs_span
#print(simulated_par_data)
# numerical_overhead_vs_span(simulated_par_data,full_seq_data,
#             problems=['Topological Sorting','LCS','Bipartite Graph MCM'],n=10**6)
#print("checkpoint 3")
#function in numerical_speedup_vs_proc
#problem_speedup_vs_proc(simulated_par_data,full_seq_data,"Bipartite Graph MCM",n_values=[10**3,10**6,10**9],max_p=10**7)
#print("checkpoint 4")
#function in problem_overhead_vs_proc

# problem_overhead_vs_proc(simulated_par_data,full_seq_data,"Bipartite Graph MCM",n_values=[10**3,10**6,10**9],
#                              allowed_models=set(model_dict.keys()))
#print("checkpoint 5")
#small_pset = ['DFA Minimization','Stable Marriage Problem','Exact Laplacian Solver']

#print(problems_switch_to_work_inefficient(simulated_par_data,full_seq_data,small_pset,n=10**3,max_p=10**20))
#print("checkpoint 6")
#functions in aggregate_switch_to_work_ineff
# problems_switch_to_work_inefficient_graph(simulated_par_data,full_seq_data,pset,
#                             n_values = [10**3,10**6,10**9],max_p=10**10)
# problems_work_efficiency_by_processors_graph(simulated_par_data,full_seq_data,pset,
#                             n = 10**6, max_p=10**9,allowed_models=set(model_dict.keys()))
#print("checkpoint 7")

#print(work_overhead_histogram(simulated_par_data,full_seq_data,small_pset,p=10**3,n=10**3,
#                            upper_bounds=[0,10,50,100,math.inf],
#                            max_p=10**20,allowed_models=set(model_dict.keys()))) # TODO: numbers don't add up

#work_overhead_histogram_graph(simulated_par_data,full_seq_data,pset,p=10**3,n_values=[10**3,10**6,10**9],
#                            upper_bounds=[0,10,50,100,math.inf],
#                           max_p=10**9,allowed_models=set(model_dict.keys()))

# work_overhead_histogram_graph_multiple_p(simulated_par_data,full_seq_data,pset,p_values=[8,10**3,10**6],n_values=[10**3,10**6,10**9],
#                             upper_bounds=[0,10,100,1000,10000,math.inf],
#                             max_p=10**9,allowed_models=set(model_dict.keys()))

#print("checkpoint 8")


# helpers

print(best_algos_by_speedup(simulated_par_data,full_seq_data,"LCS",n=10**6,
                          allowed_models=set(model_dict.keys())))

print(get_pareto_points(simulated_par_data,full_seq_data,'LCS',allowed_models=PRAM_LIKE_MODELS))





################## Extra Functions ############################

def year_stats():
    problems = get_problems(simulated_par_data)
    year_dict = {}
    for alg in simulated_par_data:
        yr = simulated_par_data[alg]["year"]
        pr = simulated_par_data[alg]["problem"]
        if pr in year_dict:
            year_dict[pr] = min(year_dict[pr], yr)
        else:
            year_dict[pr] = yr
    year_list = year_dict.values()
    print(year_list)
    dec_dict = {}
    for yr in year_list:
        dc = get_decade(yr)
        if dc not in dec_dict:
            dec_dict[dc] = 1
        else:
            dec_dict[dc] += 1
    print(dec_dict)
# year_stats()

def overflow_debugging():
    code1 = 8011.0
    code2 = 8010.0
    n = 10**3

    huge1 = Huge(max(math.log(max(math.log(n,2),1),2),1),n-1)
    huge1 = huge1 * (n * max(math.log(n,2),1))
    base2 = max(math.log(max(math.log(n,2),1),2),1)
    huge2 = Huge(base2, n+math.log(n,base2))

    print(huge1)
    print(huge2)
    print(huge1.evaluate())
    print(huge1 > huge2)
    print(huge1 == huge2)

    print("--------------------------------------")

    print(max(math.log(n,2),1))
    print(max(math.log(max(math.log(n,2),1),2),1))
    print(decimal.Decimal(int(n-1)))

    print(get_seq_runtime(code1,n)==huge1)
    print(get_seq_runtime(code1,n)==huge1.evaluate())

    print("--------------------------------------")

    print(get_seq_runtime(code1,n))
    print(log(get_seq_runtime(code1,n),10))

    print(get_seq_runtime(code2,n))

    rt = get_runtime(code1,code2,n,p=1)

    print("runtime:")
    print(rt)

    pass
# overflow_debugging()




################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
##### OLD CALLS ################################################################
################################################################################

# absolute speedup vs processors for 3 values of n for 1 algorithm
name = "14.1-11-Johnson, Metaxas (1992)"
# absolute_speedup(full_data,name)
# incremental_benefit_scaling(full_data,name)
# print(performance_vs_span_improvement(full_data))

# rel_speedup_sus()
# print(problem_relative_speedup_data(full_data,rel_speedup_seq_data,14.1,n=10**6,p=2**30))
# problem_relative_speedup_graph(full_data,rel_speedup_seq_data,[17],n=10**6)
# available_processors(top_processor_data,pc_processor_data)
# print(speedup_for_available_processors(full_data,rel_speedup_seq_data,17,
#                                        top_processor_data,pc_processor_data,n=10**6,seq=True))
# span_overhead_matrix(aux_data)

# share_of_progress_graph(full_data,rel_speedup_seq_data,possible_n=[10**3,10**6,10**9])
# print(share_of_progress_problem_data(full_data,rel_speedup_seq_data,problem=13.1,n=10**6))

# span_comparison_best_vs_work_efficient(aux_data)
# new_parallelism_graph(aux_data)
# yearly_impr_rate_histo_rt(full_data, g_buckets, n=10**3,p=512)
#decade_progress(full_data,rel_speedup_seq_data,g_decades,n=10**3,p=64)
# pareto_frontier_graph(full_data,rel_speedup_seq_data,g_decades)
# aggregated_relative_speedup(full_data,rel_speedup_seq_data,n=10**6)
# work_span_improvement_heatmap(full_data)
# print(pareto_frontier_current_fractions(full_data,rel_speedup_seq_data,g_decades)

# compound_growth_rate_distribution_graph(full_data,rel_speedup_seq_data, g_buckets,n=10**9,p=2**3)

# print(average_improvement_over_decade_data(full_data,rel_speedup_seq_data,g_decades))
# average_improvement_over_decade_graph(full_data,rel_speedup_seq_data,g_decades)

# problem_work_vs_span_pareto_frontier(full_data,rel_speedup_seq_data,14.1)

# names:
# bs_mst_algo_name = "14.1-11-Johnson, Metaxas (1992)"
# we_mst_algo_name = "14.1-13-Deo and Yoo (1981)" #"14.1-10-Chin et al. (1982)"
# strong_scaling_comparison(full_data,bs_mst_algo_name,we_mst_algo_name)
# weak_scaling_comparison_graph(full_data,bs_mst_algo_name,we_mst_algo_name)
# varying_scaling_comparison_graph(full_data,bs_mst_algo_name,we_mst_algo_name)


# new_aggregated_relative_speedup_graph(full_data,rel_speedup_seq_data,n=10**6)
# debug(full_data,rel_speedup_seq_data,n=10**6)
# print(new_data_for_speedup_for_available_processors(full_data,rel_speedup_seq_data,problem=13.1))
# print(problem_relative_speedup_data(full_data,rel_speedup_seq_data,problem=13.1,n=10**6,p=1))
# print(problem_relative_speedup_data(full_data,rel_speedup_seq_data,problem=13.1,n=10**6,p=128))
# print(problem_relative_speedup_data(full_data,rel_speedup_seq_data,problem=13.1,n=10**6,p=10**6))

# print(share_of_progress_problem_data(full_data,rel_speedup_seq_data,problem=13.1,n=10**6))
# share_of_progress_graph(full_data,rel_speedup_seq_data,possible_n=[10**3,10**6,10**9])


# {'k Nearest Neighbors Search', 'undirected SSSP', 'Polygon Clipping with Arbitrary Clipping Polygon', 
# 'Non-comparison Sorting', 'Bipartite Graph MCM', 'kth Order Statistic', '2-dimensional space', 
# 'Single String Search', '2-Dimensional Delaunay Triangulation', 'Max Flow', 'DFA Minimization', 
# '2-D Polynomial Interpolation', 'General Linear Programming', 'APSP', 'General Graph MCM', 
# 'General Linear System', 'CC', 'Matrix Chain Scheduling Problem', 'Matrix Multiplication', 
# 'Greatest Common Divisor', 'General Maximum-Weight Matching', 'SCCs', 'Intersection detection', 
# 'Boolean Matrix Multiplication', 'Constructing Suffix Trees', 'directed SSSP', 'Variance Calculations', 
# 'Line Drawing', '2-Player', '2-dimensional', 'undirected nonneg SSSP', 'Approximate MCOP', 
# 'k-dimensional space', 'Reporting intersection points', '2D Maximum Subarray', 'directed MST; MST', 
# 'CC; SCCs', 'Point-in-Polygon', 'Multiplication', '1D Maximum Subarray', 'MST', 'Matrix LU Decomposition', 
# 'Topological Sorting', 'Comparison Sorting', '3-dimensional', 'General Permutations', 'LCS', 'OBST', 
# 'Constructing Eulerian Trails in a Graph', 'Lossless Compression', 'General Root Computation', 
# 'Constuct Voronoi Diagram', 'Edit Distance, constant-size alphabet', 
# 'Transitive Reduction Problem of Directed Graphs', 'directed nonneg SSSP', 'Discrete Fourier Transform'}


# {'Matrix Multiplication', 'k Nearest Neighbors Search', 'directed nonneg SSSP', 
# 'directed MST', 'Topological Sorting', 'MST', 'Enumerating Maximal Cliques', 'Multiplication', 
# 'Boolean Matrix Multiplication', 'APSP', 'Matrix LU Decomposition', 'Bipartite Graph MCM', 
# 'General Permutations', 'Determinant of Matrices with Integer Entries', '2D Maximum Subarray', 
# 'General Linear System', 'Intersection detection', 'General Root Computation', 
# 'Exact Laplacian Solver', 'Maximum Cut', 'undirected SSSP', 'Comparison Sorting', 
# 'Constructing Eulerian Trails in a Graph', 'Transitive Reduction Problem of Directed Graphs', 
# 'All Nearest Neighbors', 'Bipartite Maximum-Weight Matching', '2-dimensional Convex Hull', 
# 'Constructing Suffix Trees', 'Point-in-Polygon', 'Non-comparison Sorting', 
# 'General Maximum-Weight Matching', 'Polygon Clipping with Arbitrary Clipping Polygon', 
# 'Single String Search', 'Variance Calculations', 'Subset Sum', '3-dimensional Convex Hull', 
# '2-Dimensional Delaunay Triangulation', '2-D Polynomial Interpolation', 'CFG Parsing', 
# '2-Dimensional Poisson Problem', 'k-dimensional space Closest Pair Problem', 
# '2-Player Nash Equilibria', 'Max Flow', 'Line Drawing', '1D Maximum Subarray', 'DFA Minimization', 
# 'All Permutations', 'Transitive Closure', 'directed SSSP', 'Stable Marriage Problem', 
# 'Edit Distance, constant-size alphabet', 'General Graph MCM', 'OBST', 'directed APSP', 
# 'Lossless Compression', 'LCS', 'Reporting intersection points', 'Discrete Fourier Transform', 
# 'CC', '3-Dimensional Poisson Problem', 'kth Order Statistic', 
# 'Transitive Closure of a symmetric Boolean matrix', 'undirected nonneg SSSP', 
# 'Constuct Voronoi Diagram', 'Matrix Chain Scheduling Problem', 'SCCs', 'MCOP', 
# '2-dimensional space Closest Pair Problem', 'Greatest Common Divisor', 'General Linear Programming'}


# nice problems:
# - 'Topological Sorting' - 2 steps, 3 par points, but only 1 model (?)
# - 'LCS' - 1 step, but lots of non-boring points
# - 'Bipartite Graph MCM' - 2 steps (2 par points)
# - 'MST' - 1 step, too many par points
# - 'Comparison Sorting' - same; also check 1988 MIMD-TC algo - span is higher than bseq
# - 'General Permutations' - same
# - 'APSP' - 1 step, quite boring
# - 'SCCs' - 1 step, 1 par algo
# - 'Variance Calculations' - 1 step, 1 par algo
# - '2-dimensional' - 1 step, quite a few par points
# - 'Point-in-Polygon' - 1 step, 1 par point
# - 'directed nonneg SSSP' - 1 step, 1 par algo

#check data correctness
with open("aux.json", "w") as json_file:
    json.dump(full_problem_data, json_file, indent=4)



print("running functions to make the actual graphs for the paper")

pset = get_problems(simulated_par_data)
#{"max": 0.001, "label": "0-0.1%"},
histo_buckets = [
            {"max": 0.03, "label": "0.1-3%"},
            {"max": 0.1, "label": "3-10%"},
            {"max": 0.3, "label": "10-30%"},
            {"max": 1, "label": "30-100%"},
            {"max": 3, "label": "100-300%"},
            {"max": 10, "label": "300-1000%"},
            {"max": math.inf, "label": ">1000%"},]

# print("figure 1.1: Algorithm Improvements over Time")
# #TODO: address the "thesis_weight" and whether its actually doing anything
# average_improvement_over_decade_graph(simulated_par_data,full_seq_data,DECADES)
# average_improvement_over_decade_graph(simulated_par_data,full_seq_data,DECADES,var_weights="thesis_weight")


# print("figure ??: Number of Parallel Processors Over Time")
# available_processors(top_processor_data,pc_processor_data)
# print("figure ??: Parallel Performance for All Pairs Shortest Paths Problem using processors available at the time")
# speedup_for_available_processors(simulated_par_data,full_seq_data,'APSP', top_processor_data,pc_processor_data,n=10**6,seq=True)

# print("figure 1.2: Algorithm Problem Average Yearly Improvement Rate (Sequantial and Parallel)")
# #TODO: pick which one is needed and also what buckets
# # NEW_yearly_impr_rate_histo_grid(simulated_par_data, full_seq_data, histo_buckets,n_values=[10**3,10**6,10**9],
# #                                 p_values=[8,10**3,10**6], measure="rt",start_from="first_seq")
# # NEW_yearly_impr_rate_histo_grid(simulated_par_data, full_seq_data, histo_buckets,n_values=[10**3,10**6,10**9],
# #                                 p_values=[8,10**3,10**6], measure="rt",start_from="best_seq")
# # NEW_yearly_impr_rate_histo_grid(simulated_par_data, full_seq_data, histo_buckets,n_values=[10**3,10**6,10**9],
# #                                 p_values=[8,10**3,10**6], measure="rt",start_from="first_par")
# # NEW_yearly_impr_rate_histo_grid(simulated_par_data, full_seq_data, histo_buckets,n_values=[10**3,10**6,10**9],
# #                                 p_values=[8,10**3,10**6], measure="rt",start_from="stacked")

# #TODO: if best parallel work is better than best sq time, not accounting for that rn
# #need to take best work as best sequential

# EVERYTHING_yearly_impr_rate_histo_grid(full_data, histo_buckets,n_values=[10**3,10**6,10**9],
#                                 p_values=[8,10**3,10**6],measure="rt")
# # EVERYTHING_yearly_impr_rate_histo_grid(full_data, histo_buckets,n_values=[10**3,10**6,10**9],
# #                                 p_values=[8,10**3,10**6],measure="rt", par_data=simulated_par_data, seq_data=full_seq_data, variation="stacked")
# EVERYTHING_yearly_impr_rate_histo_grid(full_data, histo_buckets,n_values=[10**3,10**6,10**9], 
#                                        p_values=[8,10**3,10**6],measure="rt", par_data=simulated_par_data, seq_data=full_seq_data, variation="seq_plus_all")



# print("figure 1.3: Work - Span Tradeoff for Parallel Algorithms // Computational Length")
# span_vs_work_multiple_probs_pareto_frontier(simulated_par_data,full_seq_data, problems=['Topological Sorting','LCS','Bipartite Graph MCM'])
# print("figure 1.3: Work - Span Tradeoff for Parallel Algorithms // Speedup Relative to Sequantial Time")
# numerical_overhead_vs_span(simulated_par_data,full_seq_data, problems=['Topological Sorting','LCS','Bipartite Graph MCM'],n=10**6)
print("figure 1.3: Best Span vs Best Work-efficient Algorithm Span for all Problems")
#TODO: at some point also called with aux_data so what was that? and what is full_problem_data?
span_comparison_best_vs_work_efficient(full_problem_data)
NEW_span_comparison_best_vs_work_efficient(full_problem_data)

# print("figure 1.4: Speed of Parallel Bipartite Graph Maximum Cardinality Matching")
# problem_speedup_vs_proc(simulated_par_data,full_seq_data,"Bipartite Graph MCM",n_values=[10**3,10**6,10**9],max_p=10**7)
# print("figure 1.4: Work Overhead vs # of Processors for the Bipartite Graph MCM Problem")
# problem_overhead_vs_proc(simulated_par_data,full_seq_data,"Bipartite Graph MCM",n_values=[10**3,10**6,10**9], allowed_models=set(model_dict.keys()))
# print("figure 1.4: Work Efficiency of the Fastest Algorithm for n=10^6")
# problems_work_efficiency_by_processors_graph(simulated_par_data,full_seq_data,pset, n = 10**6, max_p=10**9,allowed_models=set(model_dict.keys()))

print("figure 1.5: Work Overhead for the fastest algorithm")
# #THIS ONE IS THE OLD VERSION
# # work_overhead_histogram_graph_multiple_p(simulated_par_data,full_seq_data,pset,p_values=[8,10**3,10**6],n_values=[10**3,10**6,10**9],
# #                             upper_bounds=[0,10,100,1000,10000,math.inf],
# #                             max_p=10**9,allowed_models=set(model_dict.keys()))

#USE THIS ONE:
NEW_work_overhead_histogram_graph_multiple_p(simulated_par_data,full_seq_data,pset,p_values=[8,10**3,10**6],n_values=[10**3,10**6,10**9],
                            upper_bounds=[0,10,100,1000,10000,math.inf],
                            max_p=10**9,allowed_models=set(model_dict.keys()))


# # probs=get_problems(full_data)
# # probs_seq=get_problems(full_seq_data)
# # probs_par=get_problems(simulated_par_data)
# # with open("problems.csv", mode="w", newline="") as file:
# #     writer = csv.writer(file)
    
# #     # Writing header
# #     writer.writerow(["Problem", "In sequential", "In Parallel"])
    
# #     # Writing data rows
# #     for item in sorted(probs):  # Sorting to maintain order
# #         writer.writerow([
# #             item,
# #             1 if item in probs_seq else 0,
# #             1 if item in probs_par else 0
# #         ])



sankey_style_graph(full_data,simulated_par_data)

print("finished main")
