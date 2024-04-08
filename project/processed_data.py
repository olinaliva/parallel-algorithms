# stores data that's relatively stable - e.g. TOP500 and commertcial processor data
# also includes old data (used for testing) - e.g. full_data, aux_data
# and functions + calls for reading data from json

from project.complexity_functions import *
from project.standard_codes import CODE_DIVISON
from project.helper_functions import create_aux_data
import json

VERSION = "_JAN23"


top_processor_data = {
    1925: (1, None), 
    # 1972: (64, 'ILLIAC IV'),
    # 1985: (65536, 'Thinking Machines Corporation CM-1'),
    1985: (2, 'Cray Inc. X-MP/22'), 
    1986: (4, 'Cray Inc. CRAY-2/4-256'),
    1987: (512, 'Thinking Machines Corporation CM-2'), 
    1989: (1024, 'Thinking Machines Corporation CM-200/32k'), 
    1990: (2048, 'MasPar MP-1216'), 
    1993: (3680, 'Intel XP/S140'), 
    1997: (9152, 'Intel ASCI Red'), 
    1999: (9632, 'Intel ASCI Red'), 
    2004: (32768, 'IBM BlueGene/L DD2 beta-System (0.7 GHz PowerPC 440)'),
    2005: (131072, 'IBM eServer Blue Gene Solution'), 
    2007: (212992, 'IBM eServer Blue Gene Solution'), 
    2009: (294912, 'IBM Blue Gene/P Solution'), 
    2011: (705024, 'Fujitsu K computer, SPARC64 VIIIfx 2.0GHz, Tofu interconnect'), 
    2012: (1572864, 'IBM BlueGene/Q, Power BQC 16C 1.60 GHz, Custom'), 
    2013: (3120000, 'NUDT TH-IVB-FEP Cluster, Intel Xeon E5-2692 12C 2.200GHz, TH Express-2, Intel Xeon Phi 31S1P'), 
    2016: (10649600, 'NRCPC Sunway MPP, Sunway SW26010 260C 1.45GHz, Sunway'), 
    2017: (19860000, 'ExaScaler ZettaScaler-2.2 HPC system, Xeon D-1571 16C 1.3GHz, Infiniband EDR, PEZY-SC2 700Mhz'),
    }

pc_processor_data = {
    1925: (1, ''), # actually 1951
    2005: (2, ''), 
    2006: (4, ''), 
    2010: (8, ''), 
    2017: (32, ''), 
    2019: (64, ''),
    # 2022: (128, ''), # Tachyum prodigy, not really a conventional CPU
}

aux_data = {
13.1: {"lower bound": 20, "best seq": 20, "bs span": 1, "bs work": 20, "bs par":19, "bs overhead": 0, "we exist": 1, "we span": 1, "we work": 20, "we par": 19},
14.1: {"lower bound": 20, "best seq": 20, "bs span": 1.5, "bs work": 21.5,"bs par":20,  "bs overhead": 1.5, "we exist": 1, "we span": 2, "we work": 20, "we par": 18},
17: {"lower bound": -1, "best seq": -1, "bs span": 0.1, "bs work": 29.7,"bs par":29.6,  "bs overhead": 7, "we exist": 0, "we span": 29.995, "we work": 29.995, "we par": 0},
33: {"lower bound": 10, "best seq": 10, "bs span": 0, "bs work": 15, "bs par":15, "bs overhead": 5, "we exist": 1, "we span": 0.001, "we work": 10, "we par": 9.999},
}

rel_speedup_seq_data = {
"1": {"problem": 14.1, "year": 1926, "auth": "Borůvka", "time": 21, "span fn":bo26, "const span fn": bo26_const},
"2": {"problem": 14.1, "year": 1975, "auth": "Yao", "time": 20.1, "span fn":yao75, "const span fn": yao75_const},
"3": {"problem": 14.1, "year": 1976, "auth": "Cheriton, Tarjan", "time": 20, "span fn":ct76, "const span fn": ct76_const},
"4": {"problem": 17, "year": 1953, "auth": "Shimbel", "time": 40, "span fn": sh53, "const span fn": sh53_const},
"5": {"problem": 17, "year": 1962, "auth": "Floyd, Warshall", "time": 30, "span fn": fw62, "const span fn": fw62_const},
"6": {"problem": 17, "year": 1976, "auth": "Fredman", "time": 29.9985, "span fn": fr76, "const span fn": fr76_const},
"7": {"problem": 17, "year": 1992, "auth": "Takaoka", "time": 29.998, "span fn": ta92, "const span fn": ta92_const},
"8": {"problem": 17, "year": 2004, "auth": "Takaoka", "time": 29.997, "span fn": ta04, "const span fn": ta04_const},
"9": {"problem": 17, "year": 2009, "auth": "Chan", "time": 29.996, "span fn": ch09, "const span fn": ch09_const},
"10": {"problem": 17, "year": 2014, "auth": "Williams", "time": 29.1, "span fn": wi14, "const span fn": wi14_const},
}

full_data = {
"13.1-20-Reif (1985)": {"year": 1985, "problem": 13.1, "span": 1, "span fn": comp_fn_1_0000, "work": 20, "work eff": 0, "sim": 0, "par": 19, "model": 135},
"13.1-21-Gazit (1986)": {"year": 1986, "problem": 13.1, "span": 1, "span fn": comp_fn_1_0000, "work": 20, "work eff": 0, "sim": 0, "par": 19, "model": 135},
"13.1-06-Chin et al. (1982)": {"year": 1982, "problem": 13.1, "span": 2, "span fn": comp_fn_2_0000, "work": 20, "work eff": 0, "sim": 0, "par": 18, "model": 210},
"13.1-10-Vishkin (1982)": {"year": 1982, "problem": 13.1, "span": 2, "span fn": comp_fn_2_0000, "work": 20, "work eff": 0, "sim": 0, "par": 18, "model": 130},
"13.1-16-Han, Wagner (1990)": {"year": 1990, "problem": 13.1, "span": 2, "span fn": comp_fn_2_0000, "work": 20, "work eff": 0, "sim": 0, "par": 18, "model": 120},
"13.1-11-Das, Deo, Prasad (1990)": {"year": 1990, "problem": 13.1, "span": 11, "span fn": comp_fn_11_0000, "work": 20, "work eff": 0, "sim": 0, "par": 9, "model": 300},
"13.1-01-Shiloach and Vishkin (1982)": {"year": 1982, "problem": 13.1, "span": 1, "span fn": comp_fn_1_0000, "work": 21, "work eff": 1, "sim": 0, "par": 20, "model": 220},
"13.1-13-Koubek, Kršňáková (1985)": {"year": 1985, "problem": 13.1, "span": 1, "span fn": comp_fn_1_0000, "work": 21, "work eff": 1, "sim": 0, "par": 20, "model": 130},
"13.1-12-Awerbuch, Shiloach (1987)": {"year": 1987, "problem": 13.1, "span": 1, "span fn": comp_fn_1_0000, "work": 21, "work eff": 1, "sim": 0, "par": 20, "model": 130},
"13.1-14-Cole, Vishkin (1991)": {"year": 1991, "problem": 13.1, "span": 1, "span fn": comp_fn_1_0000, "work": 21, "work eff": 1, "sim": 0, "par": 20, "model": 130},
"13.1-22-Hirschberg, Chandra, Sarwate (1979)": {"year": 1979, "problem": 13.1, "span": 2, "span fn": comp_fn_2_0000, "work": 21, "work eff": 1, "sim": 0, "par": 19, "model": 210},
"13.1-19-Nath and Maheshwari (1982)": {"year": 1982, "problem": 13.1, "span": 2, "span fn": comp_fn_2_0000, "work": 21, "work eff": 1, "sim": 0, "par": 19, "model": 200},
"13.1-17-Koubek, Kršňáková (1985)": {"year": 1985, "problem": 13.1, "span": 2, "span fn": comp_fn_2_0000, "work": 21, "work eff": 1, "sim": 0, "par": 19, "model": 120},
"13.1-18-Koubek, Kršňáková (1985)": {"year": 1985, "problem": 13.1, "span": 2, "span fn": comp_fn_2_0000, "work": 21, "work eff": 1, "sim": 0, "par": 19, "model": 110},
"13.1-15-Cole, Vishkin (1987)": {"year": 1987, "problem": 13.1, "span": 2, "span fn": comp_fn_2_0000, "work": 21, "work eff": 1, "sim": 0, "par": 19, "model": 120},
"13.1-03-Hirschberg (1976)": {"year": 1976, "problem": 13.1, "span": 2, "span fn": comp_fn_2_0000, "work": 22, "work eff": 2, "sim": 0, "par": 20, "model": 210},
"13.1-05-Hirschberg et al. (1979)": {"year": 1979, "problem": 13.1, "span": 2, "span fn": comp_fn_2_0000, "work": 22, "work eff": 2, "sim": 0, "par": 20, "model": 210},
"13.1-09-Wyllie (1979)": {"year": 1979, "problem": 13.1, "span": 2, "span fn": comp_fn_2_0000, "work": 22, "work eff": 2, "sim": 0, "par": 20, "model": 300},
"13.1-08-Chandra (1976)": {"year": 1976, "problem": 13.1, "span": 2, "span fn": comp_fn_2_0000, "work": 28, "work eff": 8, "sim": 0, "par": 27, "model": 210},
"13.1-07-Hirschberg (1976)": {"year": 1976, "problem": 13.1, "span": 2, "span fn": comp_fn_2_0000, "work": 32, "work eff": 12, "sim": 0, "par": 30, "model": 210},
"13.1-04-Reghbati (Arjomandi) and Corneil (1978)": {"year": 1978, "problem": 13.1, "span": 2, "span fn": comp_fn_2_0000, "work": 32, "work eff": 12, "sim": 0, "par": 30, "model": 210},
"13.1-02-Kucera (1982)": {"year": 1982, "problem": 13.1, "span": 1, "span fn": comp_fn_1_0000, "work": 41, "work eff": 21, "sim": 0, "par": 40, "model": 220},
"14.1-10-Chin et al. (1982)": {"year": 1982, "problem": 14.1, "span": 2, "span fn": comp_fn_2_0000, "work": 20, "work eff": 0, "sim": 0, "par": 18, "model": 120},
"14.1-06-Bentley (1980)": {"year": 1980, "problem": 14.1, "span": 11, "span fn": comp_fn_11_0000, "work": 20, "work eff": 0, "sim": 0, "par": 9, "model": 600},
"14.1-04-Levitt and Kautz  (1972)": {"year": 1972, "problem": 14.1, "span": 1, "span fn": comp_fn_1_0000, "work": 21, "work eff": 1, "sim": 0, "par": 20, "model": 600},
"14.1-05-Savage (1977)": {"year": 1977, "problem": 14.1, "span": 2, "span fn": comp_fn_2_0000, "work": 21, "work eff": 1, "sim": 0, "par": 19, "model": 120},
"14.1-08-Nath and Maheshwari (1982)": {"year": 1982, "problem": 14.1, "span": 2, "span fn": comp_fn_2_0000, "work": 21, "work eff": 1, "sim": 0, "par": 19, "model": 120},
"14.1-01-Bader & Cong Parallel Implementation  (2006)": {"year": 2006, "problem": 14.1, "span": 11, "span fn": comp_fn_11_0000, "work": 21, "work eff": 1, "sim": 0, "par": 10, "model": 600},
"14.1-11-Johnson, Metaxas (1992)": {"year": 1992, "problem": 14.1, "span": 1.5, "span fn": comp_fn_1_5000, "work": 21.5, "work eff": 1.5, "sim": 0, "par": 20, "model": 110},
"14.1-12-Johnson, Metaxas (1992)": {"year": 1992, "problem": 14.1, "span": 1.5, "span fn": comp_fn_1_5000, "work": 21.5, "work eff": 1.5, "sim": 1, "par": 20, "model": 120},
"14.1-07-Savage and Ja'Ja' (1981)": {"year": 1981, "problem": 14.1, "span": 2, "span fn": comp_fn_2_0000, "work": 22, "work eff": 2, "sim": 0, "par": 20, "model": 120},
"14.1-09-Nath and Maheshwari (1982)": {"year": 1982, "problem": 14.1, "span": 3, "span fn": comp_fn_3_0000, "work": 22, "work eff": 2, "sim": 0, "par": 19, "model": 110},
"14.1-02-Levitt and Kautz  (1972)": {"year": 1972, "problem": 14.1, "span": 10, "span fn": comp_fn_10_0000, "work": 30, "work eff": 10, "sim": 0, "par": 20, "model": 600},
"14.1-03-Levitt and Kautz  (1972)": {"year": 1972, "problem": 14.1, "span": 20, "span fn": comp_fn_20_0000, "work": 40, "work eff": 20, "sim": 0, "par": 20, "model": 600},
"14.1-13-Deo and Yoo (1981)": {"year": 1981, "problem": 14.1, "span": 16, "span fn": comp_fn_1_5000, "work": 20, "work eff": 0, "sim": 0, "par": 6, "model": 300},
# "14.1-14-Hirschberg (1982)": {"year": 1982, "problem": 14.1, "span": 1, "span fn": comp_fn_1_0000, "work": 31, "work eff": 11, "sim": 0, "par": 30, "model": 220},
# "14.1-15-Cole, Klein, Tarjan (1996)": {"year": 1996, "problem": 14.1, "span": 1, "span fn": comp_fn_1_0000, "work": 20, "work eff": 0, "sim": 0, "par": 19, "model": 130},
# "17.1-10-Zhang, Wu, Wei & Wang (2011)": {"year": 2011, "problem": 17, "span": 2, "span fn": comp_fn_2_0000, "work": 22, "work eff": -1, "sim": 0, "par": 20, "model": 600},
"17.1-09-Takaoka (2004)": {"year": 2004, "problem": 17, "span": 0.1, "span fn": comp_fn_0_1000, "work": 29.7, "work eff": -1, "sim": 0, "par": 29.6, "model": 110},
"17.1-08-Takaoka (1998)": {"year": 1998, "problem": 17, "span": 2, "span fn": comp_fn_2_0000, "work": 29.8, "work eff": -1, "sim": 0, "par": 29.2, "model": 110},
"17.1-07-Han, Pan & Reif (1992)": {"year": 1992, "problem": 17, "span": 1.1, "span fn": comp_fn_1_1000, "work": 29.999, "work eff": -1, "sim": 0, "par": 29.45, "model": 130},
"17.1-06-Han, Pan & Reif (1992)": {"year": 1992, "problem": 17, "span": 2, "span fn": comp_fn_2_0000, "work": 29.999, "work eff": -1, "sim": 0, "par": 29.3, "model": 110},
"17.1-11-Han, Pan & Reif (1992)": {"year": 1992, "problem": 17, "span": 1, "span fn": comp_fn_1_0000, "work": 30, "work eff": -1, "sim": 0, "par": 29.5, "model": 135},
"17.1-01-Levitt and Kautz (1972)": {"year": 1972, "problem": 17, "span": 10, "span fn": comp_fn_10_0000, "work": 30, "work eff": -1, "sim": 0, "par": 20, "model": 600},
"17.1-05-Takaoka (1992)": {"year": 1992, "problem": 17, "span": 2, "span fn": comp_fn_2_0000, "work": 30.6, "work eff": -1, "sim": 0, "par": 29.4, "model": 110},
"17.1-02-Savage (1977)": {"year": 1977, "problem": 17, "span": 2, "span fn": comp_fn_2_0000, "work": 31, "work eff": -1, "sim": 0, "par": 29.5, "model": 120},
"17.1-03-Dekel; Nassimi & Sahni (1981)": {"year": 1981, "problem": 17, "span": 2, "span fn": comp_fn_2_0000, "work": 32, "work eff": -1, "sim": 0, "par": 30, "model": 600},
"17.1-04-Kucera (1982)": {"year": 1982, "problem": 17, "span": 1, "span fn": comp_fn_1_0000, "work": 41, "work eff": -1, "sim": 0, "par": 40, "model": 130},
"33.1-06-Hagerup (1991)": {"year": 1991, "problem": 33, "span": 0.001, "span fn": comp_fn_0_0010, "work": 10, "work eff": 0, "sim": 0, "par": 9.999, "model": 130},
"33.1-12-Matias et al. (1991)": {"year": 1991, "problem": 33, "span": 0.001, "span fn": comp_fn_0_0010, "work": 10, "work eff": 0, "sim": 0, "par": 9.999, "model": 130},
"33.1-01-Reif (1985)": {"year": 1985, "problem": 33, "span": 1, "span fn": comp_fn_1_0000, "work": 10, "work eff": 0, "sim": 0, "par": 9, "model": 130},
"33.1-03-Czumaj et al. (1998)": {"year": 1998, "problem": 33, "span": 0.1, "span fn": comp_fn_0_1000, "work": 10.1, "work eff": 0.1, "sim": 0, "par": 10, "model": 120},
"33.1-02-Rajasekaran et al. (1989)": {"year": 1989, "problem": 33, "span": 0.9, "span fn": comp_fn_0_9000, "work": 11, "work eff": 1, "sim": 0, "par": 9.15, "model": 130},
"33.1-08-Hagerup (1991)": {"year": 1991, "problem": 33, "span": 1, "span fn": comp_fn_1_0000, "work": 11, "work eff": 1, "sim": 0, "par": 10, "model": 110},
"33.1-04-Czumaj et al. (1998)": {"year": 1998, "problem": 33, "span": 1, "span fn": comp_fn_1_0000, "work": 11, "work eff": 1, "sim": 0, "par": 10, "model": 110},
"33.1-09-Kruskal (1983)": {"year": 1983, "problem": 33, "span": 1.1, "span fn": comp_fn_1_1000, "work": 11, "work eff": 1, "sim": 0, "par": 9.1, "model": 120},
"33.1-10-Berkman et al. (1989)": {"year": 1989, "problem": 33, "span": 1.05, "span fn": comp_fn_1_0500, "work": 11, "work eff": 1, "sim": 0, "par": 9.2, "model": 120},
"33.1-07-Hagerup (1991)": {"year": 1991, "problem": 33, "span": 2, "span fn": comp_fn_2_0000, "work": 11, "work eff": 1, "sim": 0, "par": 9, "model": 110},
"33.1-11-Alonso et al. (1996)": {"year": 1996, "problem": 33, "span": 2, "span fn": comp_fn_2_0000, "work": 12, "work eff": 2, "sim": 0, "par": 10, "model": 100},
"33.1-05-Hagerup (1991)": {"year": 1991, "problem": 33, "span": 0, "span fn": comp_fn_0_0000, "work": 15, "work eff": 5, "sim": 0, "par": 15, "model": 130},
}


################################################################################
################################################################################


def parse_json(name):
    filename="./data/"+name+".json"
    jsonFile = open(filename, 'r')
    values = json.load(jsonFile)

    dict_to_be_returned = {}
    for val in values:
        dict_to_be_returned[val["name"]] = val
        assert "year" in val
    
    return dict_to_be_returned


original_par_data = parse_json("par_algos_original"+VERSION)
simulated_par_data = parse_json("par_algos_simulated"+VERSION)
full_seq_data = parse_json("seq_data"+VERSION)
full_problem_data = create_aux_data(simulated_par_data,full_seq_data)
# print(full_problem_data)

# for prob in full_problem_data:
#     if full_problem_data[prob]["bs work"] != full_problem_data[prob]["best seq"]:
#         print(prob)

# print(full_problem_data['Matrix Multiplication'])
# for alg in simulated_par_data:
#     if simulated_par_data[alg]["problem"] == 'APSP':
#         print(simulated_par_data[alg])
# for alg in full_seq_data:
#     if full_seq_data[alg]["problem"] == 'APSP':
#         print(alg)



# problem_data = {
# "Comparison Sorting": {'best seq': 2.1, 'bs name': '125Haggkvist and Hell (1981)', 'bs span': 0.0, 'bs work': 16.1, 'bs par': 16.1, 'bs overhead': 15.94, 'we name': '1235Kasani (2) (2022)', 'we span': 0.1, 'we par': 20.0, 'we exist': True},
# "Non-comparison Sorting": {'best seq': 10.0, 'bs name': '1169Jang, Kim (1997)', 'bs span': 0.0, 'bs work': 10.0, 'bs par': 10.0, 'bs overhead': 0.0, 'we name': '1122Hagerup, Raman (ints in range) (1992)', 'we span': 0.0, 'we par': 10.0, 'we exist': True},
# "kth Order Statistic": {'best seq': 10.0, 'bs name': '2240Cole, Vishkin (1986)', 'bs span': 1.001, 'bs work': 10.0, 'bs par': 8.95, 'bs overhead': 10.0, 'we name': '2240Cole, Vishkin (1986)', 'we span': 1.001, 'we par': 8.95, 'we exist': True},
# "Approximate MCOP": {'best seq': 12.0, 'bs name': '3242Valiant, Skyum, Berkowitz, Rackoff [implicit] (1983)', 'bs span': 2.0, 'bs work': 92.0, 'bs par': 90.0, 'bs overhead': 92.0, 'we name': '3250Bradford, Rawlins, Shannon (1998)', 'we span': 2.0, 'we par': 10.0, 'we exist': True},
# "Matrix Chain Scheduling Problem": {'best seq': 20.0, 'bs name': '3251Czumaj (1993)', 'bs span': 3.0, 'bs work': 20.0, 'bs par': 17.9, 'bs overhead': 20.0, 'we name': '3251Czumaj (1993)', 'we span': 3.0, 'we par': 17.9, 'we exist': True},
# "LCS": {'best seq': 20.0, 'bs name': '4256Babu, Saxena (1997)', 'bs span': 1.0, 'bs work': 21.0, 'bs par': 20.0, 'bs overhead': 21.0, 'we name': '4257Babu, Saxena (1997)', 'we span': 2.0, 'we par': 18.0, 'we exist': True},
# "Max Flow": {'best seq': 16.1, 'bs name': '5287Peretz, Fischler (2022)', 'bs span': 6.1, 'bs work': 16.1, 'bs par': 10.0, 'bs overhead': 16.1, 'we name': '5287Peretz, Fischler (2022)', 'we span': 6.1, 'we par': 10.0, 'we exist': True},
# "Matrix Multiplication": {'best seq': 15.11, 'bs name': '6288Chandra (1976)', 'bs span': 1.0, 'bs work': 15.5, 'bs par': 15.49, 'bs overhead': 15.5, 'we name': '6312Gazit, Miller (parallel Coppersmith & Winograd 1987) (1988)', 'we span': 1.0, 'we par': 15.109, 'we exist': True},
# "Boolean Matrix Multiplication": {'best seq': 15.999, 'bs name': '6290Agerwala, Lint (1978)', 'bs span': 1.0, 'bs work': 15.999, 'bs par': 15.94, 'bs overhead': 15.999, 'we name': '6290Agerwala, Lint (1978)', 'we span': 1.0, 'we par': 15.94, 'we exist': True},
# "General Linear System": {'best seq': 16.0, 'bs name': '9367Cosnard, Robert, Trystram (Huard method) (1987)', 'bs span': 10.0, 'bs work': 16.0, 'bs par': 6.0, 'bs overhead': 16.0, 'we name': '9365Bader, Gehrke (1991)', 'we span': 10.0, 'we par': 6.0, 'we exist': True},
# "General Linear Programming": {'best seq': 40.0, 'bs name': '10375Alon & Megiddo (1990)', 'bs span': 22.0, 'bs work': 40.0, 'bs par': 18.0, 'bs overhead': 40.0, 'we name': '10375Alon & Megiddo (1990)', 'we span': 22.0, 'we par': 18.0, 'we exist': True},
# "Reporting intersection points": {'best seq': 20.0, 'bs name': '11377Reif, Sen (implicit) (1992)', 'bs span': 0.0, 'bs work': 20.0, 'bs par': 20.0, 'bs overhead': 20.0, 'we name': '11377Reif, Sen (implicit) (1992)', 'we span': 0.0, 'we par': 20.0, 'we exist': True},
# "Intersection detection": {'best seq': 11.0, 'bs name': "11379Aggarwal, Chazelle, Guibas, Ó'Dúnlaing, Yap (1988)", 'bs span': 1.0, 'bs work': 12.0, 'bs par': 11.0, 'bs overhead': 12.0, 'we name': '11382Atallah, Cole, Goodrich (1989)', 'we span': 1.0, 'we par': 10.0, 'we exist': True},
# "2-dimensional": {'best seq': 11.0, 'bs name': '12386Akl (1982)', 'bs span': 0.0, 'bs work': 30.0, 'bs par': 30.0, 'bs overhead': 30.0, 'we name': '12388Atallah, Goodrich (1986)', 'we span': 1.0, 'we par': 10.0, 'we exist': True},  
# "3-dimensional": {'best seq': 11.0, 'bs name': '12409Amato, Goodrich, Ramos [randomized] (1994)', 'bs span': 1.0, 'bs work': 11.0, 'bs par': 10.0, 'bs overhead': 11.0, 'we name': '12405Reif, Sen (1992)', 'we span': 1.0, 'we par': 10.0, 'we exist': True},
# "CC": {'best seq': 10.0, 'bs name': '13433Awerbuch, Shiloach (1987)', 'bs span': 1.0, 'bs work': 11.0, 'bs par': 10.0, 'bs overhead': 11.0, 'we name': '13429Reif (1985)', 'we span': 1.0, 'we par': 9.0, 'we exist': True},
# "SCCs": {'best seq': 10.0, 'bs name': '13414Hirschberg (1976)', 'bs span': 2.0, 'bs work': 16.2, 'bs par': 16.0, 'bs overhead': 16.2, 'we name': None, 'we span': None, 'we par': None, 'we exist': False},
# "CC; SCCs": {'best seq': 10.0, 'bs name': '13417Reghbati (Arjomandi) and Corneil (1978)', 'bs span': 2.0, 'bs work': 16.2, 'bs par': 16.0, 'bs overhead': 16.2, 'we name': '13422Chin et al. (1982)', 'we span': 2.0, 'we par': 18.0, 'we exist': True},
# "MST": {'best seq': 6.1, 'bs name': '14483Adler, Dittrich, Juurlink, Kutylowski, Rieping (1998)', 'bs span': 0.0, 'bs work': 10.0, 'bs par': 10.0, 'bs overhead': 10.0, 'we name': '14492Chong, Han, Lam (2001)', 'we span': 1.0, 'we par': 6.0, 'we exist': True},
# "directed MST; MST": {'best seq': 11.0, 'bs name': '14463Tsin, Chin (1984)', 'bs span': 2.0, 'bs work': 11.0, 'bs par': 9.0, 'bs overhead': 11.0, 'we name': '14463Tsin, Chin (1984)', 'we span': 2.0, 'we par': 9.0, 'we exist': True},
# "2-dimensional space": {'best seq': 10.0, 'bs name': '15500MacKenzie, Stout (1991)', 'bs span': 0.0, 'bs work': 10.0, 'bs par': 10.0, 'bs overhead': 10.0, 'we name': '15500MacKenzie, Stout (1991)', 'we span': 0.0, 'we par': 10.0, 'we exist': True},
# "k-dimensional space": {'best seq': 10.0, 'bs name': '15502Blelloch, Gu, Shun, Sun (2016)', 'bs span': 2.001, 'bs work': 10.0, 'bs par': 8.895, 'bs overhead': 10.0, 'we name': '15502Blelloch, Gu, Shun, Sun (2016)', 'we span': 2.001, 'we par': 8.895, 'we exist': True},
# "undirected nonneg SSSP": {'best seq': 10.0, 'bs name': '16504Driscoll, Gabow, Shrairman, Tarjan (1987)', 'bs span': 6.1, 'bs work': 10.0, 'bs par': 5.9, 'bs overhead': 10.0, 'we name': '16504Driscoll, Gabow, Shrairman, Tarjan (1987)', 'we span': 6.1, 'we par': 5.9, 'we exist': True},
# "directed nonneg SSSP": {'best seq': 10.0, 'bs name': '16510Brodal, Traff, Zaroliagis (1997)', 'bs span': 6.0, 'bs work': 11.0, 'bs par': 5.9, 'bs overhead': 11.0, 'we name': None, 'we span': None, 'we par': None, 'we exist': False},
# "undirected SSSP": {'best seq': 16.1, 'bs name': '16517Spencer (1991)', 'bs span': 10.0, 'bs work': 16.1, 'bs par': 6.1, 'bs overhead': 16.1, 'we name': '16517Spencer (1991)', 'we span': 10.0, 'we par': 6.1, 'we exist': True},      
# "directed SSSP": {'best seq': 16.0, 'bs name': '16518Garg (2018)', 'bs span': 6.01, 'bs work': 16.0, 'bs par': 9.1, 'bs overhead': 16.0, 'we name': '16518Garg (2018)', 'we span': 6.01, 'we par': 9.1, 'we exist': True},
# "APSP": {'best seq': 15.92, 'bs name': '17531Takaoka (2004)', 'bs span': 0.1, 'bs work': 15.97, 'bs par': 15.96, 'bs overhead': 15.97, 'we name': None, 'we span': None, 'we par': None, 'we exist': False},
# "Matrix LU Decomposition": {'best seq': 15.25, 'bs name': '20555Solomonik, Demmel (Classical 2.5D) (2011)', 'bs span': 6.1, 'bs work': 16.0, 'bs par': 9.0, 'bs overhead': 16.0, 'we name': '20550van de Vorst (grids) (1988)', 'we span': 15.25, 'we par': 0.0, 'we exist': True},
# "Single String Search": {'best seq': 10.0, 'bs name': '22557Galil (1995)', 'bs span': 0.0, 'bs work': 10.0, 'bs par': 10.0, 'bs overhead': 10.0, 'we name': '22557Galil (1995)', 'we span': 0.0, 'we par': 10.0, 'we exist': True},     
# "Edit Distance, constant-size alphabet": {'best seq': 20.0, 'bs name': '23572Apostolico et al. (1990)', 'bs span': 1.15, 'bs work': 21.0, 'bs par': 19.9, 'bs overhead': 21.0, 'we name': None, 'we span': None, 'we par': None, 'we exist': False},
# "Multiplication": {'best seq': 11.0, 'bs name': '27584Sinha, Srimani (1988)', 'bs span': 1.0, 'bs work': 21.0, 'bs par': 20.0, 'bs overhead': 21.0, 'we name': None, 'we span': None, 'we par': None, 'we exist': False},
# "Bipartite Graph MCM": {'best seq': 16.0, 'bs name': '28593Kim, Chwa (1987)', 'bs span': 6.11, 'bs work': 20.1, 'bs par': 15.95, 'bs overhead': 20.1, 'we name': None, 'we span': None, 'we par': None, 'we exist': False},
# "General Graph MCM": {'best seq': 6.1, 'bs name': '28597Andrews et al. (1995)', 'bs span': 3.0, 'bs work': 6.1, 'bs par': 5.8, 'bs overhead': 6.1, 'we name': '28597Andrews et al. (1995)', 'we span': 3.0, 'we par': 5.8, 'we exist': True},
# "General Permutations": {'best seq': 10.0, 'bs name': '33606Hagerup (1991)', 'bs span': 0.0, 'bs work': 15.0, 'bs par': 15.0, 'bs overhead': 15.0, 'we name': '33607Hagerup (1991)', 'we span': 0.001, 'we par': 9.999, 'we exist': True},
# "OBST": {'best seq': 20.0, 'bs name': '38628Tchendji, Zeutouo (2019)', 'bs span': 7.2, 'bs work': 20.0, 'bs par': 15.4, 'bs overhead': 20.0, 'we name': '38625Myoupo, Tchendji (2014)', 'we span': 7.2, 'we par': 15.4, 'we exist': True},
# "2-Player": {'best seq': 951.5, 'bs name': '39630Parallel Support Enumeration (2008)', 'bs span': 16.0, 'bs work': 951.5, 'bs par': 950.0, 'bs overhead': 951.5, 'we name': '39630Parallel Support Enumeration (2008)', 'we span': 16.0, 'we par': 950.0, 'we exist': True},
# "General Maximum-Weight Matching": {'best seq': 16.0, 'bs name': '40634Osiakwan, Akl (1990)', 'bs span': 11.0, 'bs work': 16.0, 'bs par': 9.0, 'bs overhead': 16.0, 'we name': '40634Osiakwan, Akl (1990)', 'we span': 11.0, 'we par': 9.0, 'we exist': True},
# "Constructing Eulerian Trails in a Graph": {'best seq': 10.0, 'bs name': '41639Park, Ryu (1999)', 'bs span': 1.0, 'bs work': 11.0, 'bs par': 10.0, 'bs overhead': 11.0, 'we name': '41641Caceres, Nasu (2003)', 'we span': 1.0, 'we par': 9.0, 'we exist': True},
# "Discrete Fourier Transform": {'best seq': 11.0, 'bs name': '42648Cui-xiang, Guo-qiang, Ming-he (2005)', 'bs span': 1.0, 'bs work': 11.0, 'bs par': 10.0, 'bs overhead': 11.0, 'we name': '42645Edelman, McCorquodale, Toledo [Algorithm 1] (1998)', 'we span': 1.0, 'we par': 10.0, 'we exist': True},
# "Line Drawing": {'best seq': 10.0, 'bs name': '43651Graham, Iyengar, Zheng (1992)', 'bs span': 0.0, 'bs work': 10.0, 'bs par': 10.0, 'bs overhead': 10.0, 'we name': '43649Pang (1990)', 'we span': 0.0, 'we par': 10.0, 'we exist': True},
# "Polygon Clipping with Arbitrary Clipping Polygon": {'best seq': 10.0, 'bs name': '44657Narayanaswami (1996)', 'bs span': 0.0, 'bs work': 10.0, 'bs par': 10.0, 'bs overhead': 10.0, 'we name': '44657Narayanaswami (1996)', 'we span': 0.0, 'we par': 10.0, 'we exist': True},
# "General Root Computation": {'best seq': 10.0, 'bs name': "48670parallel Graeffe's method - Rice, Jamieson (1989)", 'bs span': 0.0, 'bs work': 10.0, 'bs par': 10.0, 'bs overhead': 10.0, 'we name': "48670parallel Graeffe's method - Rice, Jamieson (1989)", 'we span': 0.0, 'we par': 10.0, 'we exist': True},
# "k Nearest Neighbors Search": {'best seq': 10.0, 'bs name': '49680Schieber, Vishkin (1990)', 'bs span': 0.1, 'bs work': 10.0, 'bs par': 9.1, 'bs overhead': 10.0, 'we name': '49680Schieber, Vishkin (1990)', 'we span': 0.1, 'we par': 9.1, 'we exist': True},
# "Constuct Voronoi Diagram": {'best seq': 11.0, 'bs name': '54709Reif, Sen (1989)', 'bs span': 1.0, 'bs work': 11.0, 'bs par': 10.0, 'bs overhead': 11.0, 'we name': '54703Xin et al. (2013)', 'we span': 1.0, 'we par': 10.0, 'we exist': True},
# "Variance Calculations": {'best seq': 10.0, 'bs name': "55710Chan's algorithm Parallel Implementation (1979)", 'bs span': 1.0, 'bs work': 11.0, 'bs par': 10.0, 'bs overhead': 11.0, 'we name': None, 'we span': None, 'we par': None, 'we exist': False},
# "Topological Sorting": {'best seq': 10.0, 'bs name': '56717Chaudhuri (1992)', 'bs span': 1.0, 'bs work': 16.1, 'bs par': 16.0, 'bs overhead': 16.1, 'we name': None, 'we span': None, 'we par': None, 'we exist': False},
# "DFA Minimization": {'best seq': 11.0, 'bs name': '57721Cho, Huynh (1992)', 'bs span': 2.0, 'bs work': 60.0, 'bs par': 58.0, 'bs overhead': 60.0, 'we name': None, 'we span': None, 'we par': None, 'we exist': False},
# "2-Dimensional Delaunay Triangulation": {'best seq': 10.0, 'bs name': "64774Aggarwal, Chazelle, Guibas, Ó'Dúnlaing, Yap (1988)", 'bs span': 2.0, 'bs work': 12.0, 'bs par': 10.0, 'bs overhead': 12.0, 'we name': None, 'we span': None, 'we par': None, 'we exist': False},
# "Lossless Compression": {'best seq': 10.0, 'bs name': '75852Nagumo, Lu, Watson (1) (1995)', 'bs span': 1.0, 'bs work': 11.0, 'bs par': 10.0, 'bs overhead': 11.0, 'we name': '75850Edwards, Vishkin (2014)', 'we span': 2.0, 'we par': 8.9, 'we exist': True},
# "1D Maximum Subarray": {'best seq': 10.0, 'bs name': '80874Wen (1995)', 'bs span': 1.0, 'bs work': 10.0, 'bs par': 9.0, 'bs overhead': 10.0, 'we name': '80873Perumalla and Deo (1995)', 'we span': 1.0, 'we par': 9.0, 'we exist': True},
# "2D Maximum Subarray": {'best seq': 30.0, 'bs name': '80878Qiu, Akl (1999)', 'bs span': 1.0, 'bs work': 30.0, 'bs par': 29.5, 'bs overhead': 30.0, 'we name': '80876KALYAN PERUMALLA and NARSINGH DEO (1995)', 'we span': 1.0, 'we par': 29.5, 'we exist': True},
# "Constructing Suffix Trees": {'best seq': 10.0, 'bs name': '81885Landau, Vishkin (1986)', 'bs span': 1.0, 'bs work': 20.0, 'bs par': 19.0, 'bs overhead': 20.0, 'we name': '81891Farach (1997)', 'we span': 1.0, 'we par': 9.0, 'we exist': True},
# "Point-in-Polygon": {'best seq': 10.0, 'bs name': '107932Chen, Davis, Kruskal (1993)', 'bs span': 1.0, 'bs work': 11.0, 'bs par': 10.0, 'bs overhead': 11.0, 'we name': None, 'we span': None, 'we par': None, 'we exist': False},
# "Transitive Reduction Problem of Directed Graphs": {'best seq': 16.0, 'bs name': '129949Gibbons et al. (1988)', 'bs span': 4.0, 'bs work': 16.24, 'bs par': 16.0, 'bs overhead': 16.24, 'we name': '129950Chang, Henschen (1990)', 'we span': 6.0, 'we par': 10.0, 'we exist': True},
# "2-D Polynomial Interpolation": {'best seq': 20.0, 'bs name': '142963Egecioglu, Gallopoulos, Koc (1990)', 'bs span': 1.0, 'bs work': 20.0, 'bs par': 19.0, 'bs overhead': 20.0, 'we name': '142963Egecioglu, Gallopoulos, Koc (1990)', 'we span': 1.0, 'we par': 19.0, 'we exist': True},
# "Greatest Common Divisor": {'best seq': 20.0, 'bs name': '143970Sedjelmaci (2001)', 'bs span': 990.0, 'bs work': 2090.5, 'bs par': 1000.5, 'bs overhead': 2090.5, 'we name': None, 'we span': None, 'we par': None, 'we exist': False},
# }

