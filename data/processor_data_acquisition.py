from header import *
import json
import csv
import copy
import os
import datetime


def find_proc_increase_commercial():
    proc_num_for_year = find_best_top_every_year(name="cpu_short")
    
    years = sorted(proc_num_for_year.keys())
    proc_increase = {}
    best_so_far = 0
    for y in years:
        if proc_num_for_year[y][0] > best_so_far:
            proc_increase[y] = proc_num_for_year[y]
            best_so_far = proc_num_for_year[y][0]

    return proc_increase

def find_proc_increase_supercomputer():
    starting_proc = {
        1925: (1, None),
        1972: (64, "ILLIAC IV"),
        # 1985: (65536, "Thinking Machines Corporation CM-1"), - not accurate (no FPUs)
        1987: (512, "Thinking Machines Corporation CM-2"), # 2048 32-bit FPUs
    }
    proc_pre_2008 = find_best_top_every_year(name="top500_pre_2008")
    proc_post_2008 = find_best_top_every_year(name="top500_post_2008")

    all_yearly_proc = {} #{**starting_proc, **proc_pre_2008, **proc_post_2008}
    for dataset in [starting_proc, proc_pre_2008, proc_post_2008]:
        for elem in dataset:
            if elem in all_yearly_proc:
                if dataset[elem][0] > all_yearly_proc[elem][0]:
                    all_yearly_proc[elem] = dataset[elem]
            else:
                all_yearly_proc[elem] = dataset[elem]

    years = sorted(all_yearly_proc.keys())
    proc_increase = {}
    best_so_far = 0
    for y in years:
        if all_yearly_proc[y][0] > best_so_far:
            proc_increase[y] = all_yearly_proc[y]
            best_so_far = all_yearly_proc[y][0]

    return proc_increase

def find_best_top_every_year(name):
    csvFilePath = r'data/past_data/'+name+r'.csv'
    proc_num_for_year = {}
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            comp_name = ""
            if name=="top500_post_2008":
                y = int(row["Year"])
                proc = int(row["Cores"]) if row["Cores"]!="" else int(row["Total Cores"])
                comp_name = row["Manufacturer"]+" "+row["Computer"]
            elif name=="top500_pre_2008":
                y = int(row["Year"])
                proc = int(row["Processors"])
                comp_name = row["Manufacturer"]+" "+row["Computer"]
            elif name=="cpu_short":
                y = row["Launched"]
                y = int(datetime.datetime.strptime(y, "%m/%d/%y").date().year)
                proc = 1 if row["Cores"]=='NA' else int(row["Cores"])
            else:
                raise ValueError("This only works on 3 specific files")
            if y in proc_num_for_year and proc_num_for_year[y][0]<proc:
                proc_num_for_year[y] = (proc,comp_name)
            elif y not in proc_num_for_year:
                proc_num_for_year[y] = (proc,comp_name)
    return proc_num_for_year