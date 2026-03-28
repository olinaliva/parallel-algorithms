#from header import *
import json
import csv
import copy
#aaaaaaah
#import sys
#import os
#header_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#sys.path.append(header_dir)
#from header import *

#put these here to not deal w/ the commented out header
#VERSION="_JAN26"
#VERSION="_FEB18"
# VERSION="_MAR9"
VERSION="_MAR21"
import warnings


PARALLEL_ALGO_FIELDS={
        "Old Family #": "family",
        "Looked at?": "looked at", 
        "Subproblem": "problem",
        "Variation": "vars", 
        "Algo ID": "id", 
        "Algorithm Name": "auth", 
        "Year": "year", 
        "Span Encoding (T_1)": "span",
        "Work Encoding (T_inf)": "work", 
        "Model Encoding": "model", 
        "Randomized?": "randomized", 
        "Approximate?": "approximate", 
        "Heuristic-based?": "heuristic", 
        "Parallel?": "parallel", 
        "# of Proc Encoding": "par", 
        "Quantum?": "quantum", 
        "GPU-based?": "gpu", 
        "Domains": "domains"
    }

SEQUENTIAL_ALGO_FIELDS={
        "Family Name": "family",  # was "Old Family #" — Sheet1 no longer has that column
        "Looked at?": "looked at",
        "Subproblem (currently only for Parallel Algos)": "problem",
        "Variation": "vars",
        "Algo ID": "id",
        "Algorithm Name": "auth",
        "Year": "year",
        "Time Encoding": "time",
        "Randomized?": "randomized",
        "Approximate?": "approximate",
        "Heuristic-based?": "heuristic",
        "Parallel?": "parallel",
        "Quantum?": "quantum",
        "GPU-based?": "gpu",
        "Domains": "domains"
    }

PARALLEL_DISCARABLE_FIELD_VALUES = {
        "problem": ("","#N/A"),
        "auth": "",
        "year": "",
        "span": ("","xxxx","xxx","yy"," "),
        "work": ("","xxxx","xxx","yy"," "),
        "model": (""," "),
        "approximate": "1",
        "heuristic": "1",
        "parallel": ("0",""," "),
        "par": "",
        "quantum": "1",
        "gpu": "1",
        "looked at": ("0", "0.001"),
    }

SEQUENTIAL_DISCARABLE_FIELD_VALUES = {
        # "problem" removed: seq entries have empty Subproblem (it's only filled for parallel algos)
        "auth": "",
        "year": ("",'-'),
        "time": "",
        "approximate": "1",
        "heuristic": "1",
        "parallel": "1",
        "quantum": "1",
        "gpu": "1",
        "looked at": ("0", "0.001"),
    }

PARALLEL_ALLOWABLE_MODELS = {100, 110, 120, 130, 131, 132, 133, 135, 200, 210, 
                             220, 300, 310, 320, 330, 400, 500, 510, 520}


def log_underreviewed_entries(values, dataset_label, version):
    """
    Save entries with 'looked at' in ("0", "0.001") to data/underreviewed_entries_VERSION.json
    for future data review. Reads any existing file and appends, so calling for seq then par
    produces a single combined list.
    """
    flagged = []
    for entry in values:
        if entry.get("looked at", "") in ("0", "0.001"):
            record = {"dataset": dataset_label}
            for k in ("family", "id", "auth", "year", "problem", "vars", "domains", "looked at"):
                if k in entry:
                    record[k] = entry[k]
            flagged.append(record)
    output_path = f'./data/underreviewed_entries{version}.json'
    existing = []
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    existing.extend(flagged)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=4)
    print(f"Logged {len(flagged)} underreviewed {dataset_label} entries ({len(existing)} total) to {output_path}")


def create_all_datasets():
    '''
    Creates the parallel dataset, sequential dataset (out of 2 sheets), and the
    auxiliary dataset (with one entry per problem)
    '''
    pass


def create_seq_data(name1,name2):
    values = []
    for name in [name1,name2]:
        csvFilePath = r'./'+name+r'.csv'
        with open(csvFilePath, encoding='utf-8') as csvf: 
            csvReader = csv.DictReader(csvf)
            for row in csvReader: 
                values.append(row)

    # jsonFilePath = r'./'+name1+r'_raw.json'
    # with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
    #     jsonString = json.dumps(values, indent=4)
    #     jsonf.write(jsonString)

    print(values[0].keys())
    print(values[-1].keys())

    print(len(values))
    wanted_fields_only_values = filter_unwanted_fields_json(values, 
                        wanted_fields=SEQUENTIAL_ALGO_FIELDS)
    print(len(wanted_fields_only_values))
    print(wanted_fields_only_values[0].keys())
    print(wanted_fields_only_values[-1].keys())

    log_underreviewed_entries(wanted_fields_only_values, "seq", VERSION)
    discarded_bad_algos_values = filter_unwanted_algos(wanted_fields_only_values,
                        unwanted_values=SEQUENTIAL_DISCARABLE_FIELD_VALUES)
    print(len(discarded_bad_algos_values))
    algos_with_subproblems = consolidate_subproblems(discarded_bad_algos_values)
    print(len(algos_with_subproblems))
    algos_with_names = add_name_field(algos_with_subproblems)
    final_values = type_cast_data(algos_with_names)

    # Fallback: seq entries leave "Subproblem" blank (parallel-only field), so problem=="".
    # Try vars first, then family (for problems with no subproblems, e.g. Cardinality Estimation).
    for entry in final_values:
        if entry.get("problem", "") == "":
            if entry.get("vars", "") != "":
                entry["problem"] = entry["vars"]
            elif entry.get("family", "") != "":
                entry["problem"] = entry["family"]

    print(str(len(final_values))+" algorithms in the sequential dataset")
    newJsonFilePath = r'./data/seq_data'+VERSION+r'.json'
    with open(newJsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(final_values, indent=4)
        jsonf.write(jsonString)


    pass

def create_par_data(name):
    convert_csv_to_json(name)
    apply_various_operations_to_change_the_json_file_so_its_usable(name,
                    wanted_fields=PARALLEL_ALGO_FIELDS,
                    unwanted_values=PARALLEL_DISCARABLE_FIELD_VALUES,
                    allowed_model_list=PARALLEL_ALLOWABLE_MODELS)
    

def convert_csv_to_json(name):
    jsonArray = []
    csvFilePath = r'./'+name+r'.csv'
    jsonFilePath = r'./'+name+r'_raw.json'
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf)
        for row in csvReader: 
            jsonArray.append(row)
            # if "Cole & Gooddrich" in row['Algorithm Name']:
            #     print("======================================")
            #     print(row)
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)
    print("Successfuly wrote "+str(len(jsonArray))+" items")

def apply_various_operations_to_change_the_json_file_so_its_usable(name,wanted_fields,unwanted_values,allowed_model_list):
    '''
    Creates the datasets in their analyzable form
    '''
    jsonFilePath = r'./'+name+r'_raw.json'
    jsonFile = open(jsonFilePath, 'r')
    values = json.load(jsonFile)

    wanted_fields_only_values = filter_unwanted_fields_json(values, wanted_fields)
    print("FILTER UNDWANTED FIELDS ONLY VALUES DONE")

    log_underreviewed_entries(wanted_fields_only_values, "par", VERSION)
    discarded_bad_algos_values = filter_unwanted_algos(wanted_fields_only_values, unwanted_values)
    print("FILTER UNDWANTED ALGOS DONE")

    # one_var_per_algo_values, vars = separate_variations(discarded_bad_algos_values)
    algos_with_final_subproblems = consolidate_subproblems(discarded_bad_algos_values)
    print("ALGOS WITH FINAL SUBPROBLEMS DONE")
    
    final_values = type_cast_data(algos_with_final_subproblems)
    print("TYPE CAST DATA DONE")

    # make the "original" dataset with only meaningful models (no other or distributed memory)
    meaningful_models_values = remove_nonspecific_models(final_values,allowed_model_list)
    print(str(len(meaningful_models_values))+" algorithms in the original dataset")
    newJsonFilePath = './data/par_algos_original'+VERSION+'.json'
    print("file path: ",newJsonFilePath)
    with open(newJsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(meaningful_models_values, indent=4)
        jsonf.write(jsonString)

    # make the "simulated" dataset with all algorithms simulated onto the main model
    simulated_algorithms_values = simulate_models(final_values)
    print(str(len(simulated_algorithms_values))+" algorithms in the simulated dataset")
    newJsonFilePath = './data/par_algos_simulated'+VERSION+'.json'
    with open(newJsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(simulated_algorithms_values, indent=4)
        jsonf.write(jsonString)


def filter_unwanted_fields_json(values, wanted_fields):
    '''
    discards any field not in wanted_fields, and renames the fields according
    to the their value

    name: name of the csv file
    wanted_fields: dictionary mapping wanted fields to their preferred name
    '''
    # jsonFilePath = r'./'+name+r'_raw.json'
    # jsonFile = open(jsonFilePath, 'r')
    # values = json.load(jsonFile)
    new_values = []
    for element in values:
        # if element["Algo ID"]=='9':
        #     print(element)
        new_element = {}
        for key in element:
            if key in wanted_fields:
                new_element[wanted_fields[key]] = element[key]
        new_values.append(new_element)

    return new_values
    # newJsonFilePath = r'./fields_'+name+r'.json'
    # with open(newJsonFilePath, 'w', encoding='utf-8') as jsonf: 
    #     jsonString = json.dumps(new_values, indent=4)
    #     jsonf.write(jsonString)

def filter_unwanted_algos(values, unwanted_values):
    '''
    discards any algorithm with one or more unvalid fields (as specified by the
    unwanted_values input dictionary)
    '''
    # jsonFilePath = r'./fields_'+name+r'.json'
    # jsonFile = open(jsonFilePath, 'r')
    # values = json.load(jsonFile)

    new_values = copy.deepcopy(values)

    removed_stats = {}
    for field in unwanted_values:
        removed_stats[field] = 0
    for i in reversed(range(len(values))):
        element = values[i]
        for field in unwanted_values:
            print("element ",element)
            #its taking "values" as just the name of the csv :(
            print("unwanted values ", unwanted_values)
            print("field", field)
            
            if element[field] in unwanted_values[field]:
                new_values.pop(i)
                removed_stats[field] += 1

            # if element[field] == unwanted_values[field]:
            #     new_values.pop(i)
            #     removed_stats[field] += 1
            # #deal w/ xxx xxxx and yy (and also an error where they are "")
            # elif (element["span"] == "xxxx" or element["span"] == "xxx" or element["span"] == "yy" or element["span"] == "" or element["span"] == " "):
            #     new_values.pop(i)
            #     removed_stats["span"] += 1
            # elif (element["work"] == "xxxx" or element["work"] == "xxx" or element["work"] == "yy"):
            #     new_values.pop(i)
            #     removed_stats["work"] += 1
            # #checking if these will fix an error im getting :(
            # elif (element["model"] == "" or element["model"] == " "):
            #     new_values.pop(i)
            #     removed_stats["model"] += 1
            # elif (element["par"] == "" or element["par"] == " "):
            #     new_values.pop(i)
            #     removed_stats["par"] += 1
            # #removing double encoded models for now
            # elif (";" in element["model"]): 
            #     new_values.pop(i)
            #     removed_stats["model"] += 1
            # elif (element["problem"]=="#N/A"):
            #     new_values.pop(i)
            #     removed_stats["problem"] += 1
                break
    
    return new_values

def consolidate_subproblems(values):
    '''
    TODO
    '''
    warnings.warn("Warning...........Subproblems not consolidated!") #what was the thought process here?
    problem_set = set()
    for val in values:
        problem_set.add(val["problem"])
    # print("LIST OF CURRENT PROBLEMS ("+str(len(values))+")")
    # for prob in problem_set:
    #     print(prob)
    return values



def separate_variations(values):
    '''
    For each problem, chooses the most frequent variation as its canonical one
    Discards algorithms not solving their canonical variation, sets "vars" to it 
    '''
    # jsonFilePath = r'./analyzable_'+name+r'.json'
    # jsonFile = open(jsonFilePath, 'r')
    # values = json.load(jsonFile)
    new_values = []

    problems = {}
    for element in values:
        problems[element["problem"]] = None

    for problem in problems:
        # getting the most frequent variation
        var_dict = {}
        for element in values:
            if element["problem"] == problem:
                # get the variations and update counts
                vars = element["vars"].replace(" ", "").split(";")
                for var in set(vars):
                    if var in var_dict:
                        var_dict[var] += 1
                    else:
                        var_dict[var] = 1
        freq_var = max(var_dict, key=var_dict.get)
        problems[element["problem"]] = freq_var

        # including algorithms for the most frequent variation
        for element in values:
            if element["problem"] == problem and freq_var in element["vars"]:
                new_values.append(copy.deepcopy(element))
                new_values[-1]["vars"] = freq_var

    return new_values, problems

def type_cast_data(values):
    '''
    type casting should be the last operation performed during data cleanup
    '''
    new_values = copy.deepcopy(values)
    # print(type(new_values))
    # print(len(new_values))
    # print(new_values[1])
    # print(new_values[0][0])

    for i in reversed(range(len(new_values))):
        element = new_values[i]
        deleted=False
        for field in ["year","model"]:
            if field in element:
                # print("field in element")
                if element[field] == '-':
                    # print("dash")
                    del new_values[i]
                    deleted=True
                    break
                else:
                    print("element[field] ",element[field])
                    print("field: ",field)
                    #tripping over model="" which is weird since it should be filtered out i think??
                    #seems ti be fixed by specifically filtering out models that are "" and " " ??
                    element[field] = int(element[field])
        if deleted==True: break
        for field in ["span","work","par","time"]:
            if field in element:
                if element[field] == '-':
                    # print("dash")
                    del new_values[i]
                    break
                print("element[field] ",element[field])
                print("field: ",field)
                #same issues of "" values :( (did specific filtering above)
                #also oh no there are models with value; value. need to fix
                element[field] = float(element[field])
    
    return new_values

def add_name_field(values):
    new_values = []
    for element in values:
        new_values.append(copy.deepcopy(element))
        # if "family" not in element:
        #     print(element)
        new_name = element["family"]+element["id"]+element["auth"]+" ("+str(element["year"])+")"
        new_values[-1]["name"] = new_name
    return new_values


def remove_nonspecific_models(values,allowed_model_list):
    '''
    removes models we don't care about, and creates the "name" field
    '''
    new_values = []
    for element in values:
        if element["model"] in allowed_model_list:
            new_values.append(copy.deepcopy(element))
            print(element)
            #print(element["family"])
            #there isn't a key "family", going to go with "problem" and see if it fucks stuff over later
            #yes it did fuck stuff over later but its unfucked now
            #new_name = element["problem"]+element["id"]+element["auth"]+" ("+str(element["year"])+")"
            new_name = element["family"]+element["id"]+element["auth"]+" ("+str(element["year"])+")"
            new_values[-1]["name"] = new_name
    return new_values

def simulate_models(values):
    new_allowable_models = PARALLEL_ALLOWABLE_MODELS.copy()
    new_allowable_models.add(700)
    return remove_nonspecific_models(values,new_allowable_models)

    return
    SIM_TABLE = {
    100: "PRAM",
    110: "PRAM-EREW",
    120: "PRAM-CREW",
    130: "PRAM-CRCW",
    131: "PRAM-CRCW-ARBITRARY",
    132: "PRAM-CRCW-COMMON",
    133: "PRAM-CRCW-PRIORITY",
    135: "Probabilistic PRAM-CRCW",
    200: "SIMD-SM",
    210: "SIMD-SM-R",
    220: "SIMD-SM-RW",
    300: "MIMD-TC",
    310: "MIMD-TC EREW",
    320: "MIMD-TC CREW",
    330: "MIMD-TC CRCW",
    400: "BSP",
    500: "Comparator Circuits",
    510: "Sorting Network",
    520: "Hardware Sorter",
    700: "Distributed Memory"
    } # this should be in the header doc, along with MAIN_MODEL

    # message passing

    new_values = []
    for element in values:
        if element["model"] == MAIN_MODEL:
            new_values.append(copy.deepcopy(element))
            new_values[-1]["sim"] = 0
            new_name = element["vars"]+element["id"]+element["auth"]+" ("+str(element["year"])+")"
            new_values[-1]["name"] = new_name
        else:
            old_model = element["model"]
            if old_model in SIM_TABLE:
                new_values.append(copy.deepcopy(element))
                
                new_values[-1]["span"] = element["span"]
                new_values[-1]["work"] = element["work"]
                new_values[-1]["par"] = element["par"]

                # new_values[-1]["span"] = SIM_TABLE[old_model]["span"](element["span"])
                # new_values[-1]["work"] = SIM_TABLE[old_model]["work"](element["work"])
                # new_values[-1]["par"] = SIM_TABLE[old_model]["par"](element["par"])
                
                new_values[-1]["sim"] = 1
                new_values[-1]["model"] = MAIN_MODEL
                new_name = element["vars"]+element["id"]+element["auth"]+" ("+str(element["year"])+")"
                new_values[-1]["name"] = new_name

    return new_values



def make_full_dataset(parallel_data_name, sequential_data):
    jsonFilePath = r'./'+parallel_data_name+r'_raw.json'
    jsonFile = open(jsonFilePath, 'r')
    values = json.load(jsonFile)
    new_values=copy.deepcopy(values)

    


    newJsonFilePath = './data/full_algos_(simulated)'+VERSION+'.json'
    with open(newJsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(new_values, indent=4)
        jsonf.write(jsonString)
    pass


MODEL_NAMES = {
    100: "PRAM (unspecified)", 110: "PRAM-EREW", 120: "PRAM-CREW",
    130: "PRAM-CRCW", 131: "PRAM-CRCW-ARB", 132: "PRAM-CRCW-COM",
    133: "PRAM-CRCW-PRI", 135: "Prob. PRAM-CRCW",
    200: "SIMD-SM", 210: "SIMD-SM-R", 220: "SIMD-SM-RW",
    300: "MIMD-TC", 310: "MIMD-TC EREW", 320: "MIMD-TC CREW", 330: "MIMD-TC CRCW",
    400: "BSP",
    500: "Comparator Circuits", 510: "Sorting Network", 520: "Hardware Sorter",
    600: "Other", 610: "External Memory",
    700: "Distributed Memory", 800: "Word RAM (Sequential)",
}

EXCLUSION_LABELS = {
    "looked at":  "not fully reviewed (looked_at=0/0.001)",
    "problem":    "no subproblem specified",
    "auth":       "no author",
    "year":       "no year",
    "span":       "no span encoding",
    "work":       "no work encoding",
    "model":      "no model encoding",
    "approximate":"approximate algorithm",
    "heuristic":  "heuristic-based algorithm",
    "parallel":   "not a parallel algorithm",
    "par":        "no processor count encoding",
    "quantum":    "quantum algorithm",
    "gpu":        "GPU-based algorithm",
    "time":       "no time encoding",
}


def _classify_exclusions(field_filtered_values, discard_rules):
    """
    Walk every entry in field_filtered_values and classify it against
    discard_rules (same format as PARALLEL/SEQUENTIAL_DISCARABLE_FIELD_VALUES).
    Returns (kept, excluded) where excluded entries have an extra 'reason' key.
    Uses first-failing-field logic, matching filter_unwanted_algos behaviour.
    """
    kept = []
    excluded = []
    for entry in field_filtered_values:
        first_reason = None
        for field, bad_vals in discard_rules.items():
            val = entry.get(field, "")
            if isinstance(bad_vals, str):
                bad_vals = (bad_vals,)
            if val in bad_vals:
                first_reason = field
                break
        if first_reason:
            rec = dict(entry)
            rec["reason"] = first_reason
            excluded.append(rec)
        else:
            kept.append(entry)
    return kept, excluded


def _count_typecast_drops(values):
    """
    Count how many entries type_cast_data would drop (those with '-' in
    year/model/span/work/par/time).  Does not mutate values.
    """
    drops = 0
    for entry in values:
        for field in ("year", "model", "span", "work", "par", "time"):
            if field in entry and entry[field] == "-":
                drops += 1
                break
    return drops


def generate_pipeline_report(par_csv_name, seq_csv_name1, seq_csv_name2,
                              version, output_dir=None):
    """
    Run the full conversion pipeline with detailed instrumentation at every
    stage and write a text report + JSON report + matplotlib figures.

    par_csv_name      e.g. "data/Parallel_Algos_MAR21"  (no .csv suffix)
    seq_csv_name1/2   e.g. "data/Sheet1_MAR21", "data/Sheet1_New_Entries_MAR21"
    version           e.g. "_MAR21"
    output_dir        where to save outputs (default: ./data/pipeline_report<version>/)
    """
    import os
    import datetime

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        HAS_MPL = True
    except ImportError:
        HAS_MPL = False
        print("Warning: matplotlib not available — skipping visualizations")

    if output_dir is None:
        output_dir = f"./data/pipeline_report{version}/"
    os.makedirs(output_dir, exist_ok=True)

    report = {
        "version": version,
        "generated": datetime.datetime.now().isoformat(),
        "par": {},
        "seq": {},
        "combined": {},
    }
    lines = []

    def hdr(title, char="="):
        lines.append("")
        lines.append(char * 64)
        lines.append(f"  {title}")
        lines.append(char * 64)

    def sub(title):
        lines.append(f"\n  -- {title} --")

    def ln(text="", indent=4):
        lines.append(" " * indent + text)

    # =========================================================
    # PARALLEL PIPELINE
    # =========================================================
    hdr(f"PARALLEL ALGORITHMS PIPELINE  [{version}]")

    # Stage 0: raw CSV
    with open(f"./{par_csv_name}.csv", encoding="utf-8") as f:
        par_raw = list(csv.DictReader(f))
    ln(f"Stage 0  Raw CSV rows:                          {len(par_raw):>5}")
    report["par"]["s0_raw"] = len(par_raw)

    # Stage 1: field selection (rename only)
    par_fields = filter_unwanted_fields_json(par_raw, PARALLEL_ALGO_FIELDS)
    ln(f"Stage 1  After field selection (rename only):   {len(par_fields):>5}")
    report["par"]["s1_after_field_select"] = len(par_fields)

    # Stage 2: classify exclusions
    par_kept, par_excl = _classify_exclusions(par_fields, PARALLEL_DISCARABLE_FIELD_VALUES)

    par_excl_counts = {}
    for e in par_excl:
        r = e["reason"]
        par_excl_counts[r] = par_excl_counts.get(r, 0) + 1

    sub("Stage 2  Exclusion breakdown")
    ln(f"Total excluded:                                 {len(par_excl):>5}", 6)
    for field, bad_vals in PARALLEL_DISCARABLE_FIELD_VALUES.items():
        n = par_excl_counts.get(field, 0)
        if n:
            label = EXCLUSION_LABELS.get(field, field)
            ln(f"  {label+':':55s} {n:>4}", 6)
    ln(f"Entries passing all filters:                    {len(par_kept):>5}", 6)
    report["par"]["s2_excluded"] = len(par_excl)
    report["par"]["s2_excluded_by_reason"] = par_excl_counts
    report["par"]["s2_kept"] = len(par_kept)

    # Stage 3: type cast drops
    tc_drops_par = _count_typecast_drops(par_kept)
    par_after_tc = len(par_kept) - tc_drops_par
    ln(f"Stage 3  After type casting (drops '-' values): {par_after_tc:>5}"
       f"  ({tc_drops_par} dropped)")
    report["par"]["s3_after_typecast"] = par_after_tc
    report["par"]["s3_typecast_drops"] = tc_drops_par

    # Stage 4: model filter
    # (We work from par_kept since type_cast only adds int/float conversion;
    #  we parse model as int manually for comparison.)
    def _model_int(e):
        try:
            return int(e.get("model", -1))
        except (ValueError, TypeError):
            return -1

    model_counts_raw = {}
    for e in par_kept:
        m = _model_int(e)
        model_counts_raw[m] = model_counts_raw.get(m, 0) + 1

    allowable     = PARALLEL_ALLOWABLE_MODELS
    sim_allowable = PARALLEL_ALLOWABLE_MODELS | {700}

    par_original  = [e for e in par_kept if _model_int(e) in allowable]
    par_simulated = [e for e in par_kept if _model_int(e) in sim_allowable]
    par_excluded_model = [e for e in par_kept if _model_int(e) not in sim_allowable]

    sub("Stage 4  Model distribution (entries passing filters)")
    for m, cnt in sorted(model_counts_raw.items(), key=lambda x: -x[1]):
        name = MODEL_NAMES.get(m, f"Unknown code {m}")
        if m in allowable:
            tag = "original + simulated"
        elif m in sim_allowable:
            tag = "simulated only"
        else:
            tag = "EXCLUDED from both datasets"
        ln(f"  {name} [{m}]:  {cnt:>4}   ({tag})", 6)
    ln(f"Stage 4a Original dataset  (known PRAM/MIMD/BSP/Circuit): {len(par_original):>4}")
    ln(f"Stage 4b Simulated dataset (+Distributed Memory):          {len(par_simulated):>4}")
    ln(f"         Excluded by model filter:                         {len(par_excluded_model):>4}")
    report["par"]["s4_original"]         = len(par_original)
    report["par"]["s4_simulated"]        = len(par_simulated)
    report["par"]["s4_excluded_by_model"]= len(par_excluded_model)
    report["par"]["s4_model_counts"]     = {MODEL_NAMES.get(m, str(m)): v
                                             for m, v in model_counts_raw.items()}
    report["par"]["s4_model_excluded_entries"] = [
        {k: e.get(k, "") for k in ("family", "id", "auth", "year", "problem", "model")}
        for e in par_excluded_model
    ]

    # Problem coverage (simulated dataset)
    par_problems = {}
    for e in par_simulated:
        p = e.get("problem", "")
        par_problems[p] = par_problems.get(p, 0) + 1

    sub(f"Problem coverage in simulated dataset: {len(par_problems)} unique problems")
    for p, cnt in sorted(par_problems.items(), key=lambda x: -x[1]):
        ln(f"  {p+':':55s} {cnt:>3}", 6)
    report["par"]["problem_count"]   = len(par_problems)
    report["par"]["problems"]        = par_problems

    # =========================================================
    # SEQUENTIAL PIPELINE
    # =========================================================
    hdr(f"SEQUENTIAL ALGORITHMS PIPELINE  [{version}]")

    seq_raw = []
    for name in [seq_csv_name1, seq_csv_name2]:
        with open(f"./{name}.csv", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            ln(f"  {name}.csv:  {len(rows)} rows", 2)
            seq_raw.extend(rows)
    ln(f"Stage 0  Raw CSV rows (both sheets combined):   {len(seq_raw):>5}")
    report["seq"]["s0_raw"] = len(seq_raw)

    seq_fields = filter_unwanted_fields_json(seq_raw, SEQUENTIAL_ALGO_FIELDS)
    ln(f"Stage 1  After field selection:                 {len(seq_fields):>5}")
    report["seq"]["s1_after_field_select"] = len(seq_fields)

    seq_kept, seq_excl = _classify_exclusions(seq_fields, SEQUENTIAL_DISCARABLE_FIELD_VALUES)

    seq_excl_counts = {}
    for e in seq_excl:
        r = e["reason"]
        seq_excl_counts[r] = seq_excl_counts.get(r, 0) + 1

    sub("Stage 2  Exclusion breakdown")
    ln(f"Total excluded:                                 {len(seq_excl):>5}", 6)
    for field, bad_vals in SEQUENTIAL_DISCARABLE_FIELD_VALUES.items():
        n = seq_excl_counts.get(field, 0)
        if n:
            label = EXCLUSION_LABELS.get(field, field)
            ln(f"  {label+':':55s} {n:>4}", 6)
    ln(f"Entries passing all filters:                    {len(seq_kept):>5}", 6)
    report["seq"]["s2_excluded"]           = len(seq_excl)
    report["seq"]["s2_excluded_by_reason"] = seq_excl_counts
    report["seq"]["s2_kept"]               = len(seq_kept)

    tc_drops_seq = _count_typecast_drops(seq_kept)
    seq_after_tc = len(seq_kept) - tc_drops_seq
    ln(f"Stage 3  After type casting:                    {seq_after_tc:>5}"
       f"  ({tc_drops_seq} dropped)")
    report["seq"]["s3_after_typecast"] = seq_after_tc

    # Problem fallback (problem → vars → family)
    no_problem_before = sum(1 for e in seq_kept if not e.get("problem", "").strip())
    fixed_by_vars     = sum(1 for e in seq_kept
                            if not e.get("problem","").strip() and e.get("vars","").strip())
    fixed_by_family   = sum(1 for e in seq_kept
                            if not e.get("problem","").strip()
                            and not e.get("vars","").strip()
                            and e.get("family","").strip())
    still_empty       = no_problem_before - fixed_by_vars - fixed_by_family

    ln(f"Stage 4  Problem name fallback")
    ln(f"  Entries with blank problem before fallback:   {no_problem_before:>5}", 6)
    ln(f"  Fixed by vars field:                          {fixed_by_vars:>5}", 6)
    ln(f"  Fixed by family field:                        {fixed_by_family:>5}", 6)
    ln(f"  Still missing problem after fallback:         {still_empty:>5}", 6)
    report["seq"]["s4_no_problem_before_fallback"] = no_problem_before
    report["seq"]["s4_fixed_by_vars"]   = fixed_by_vars
    report["seq"]["s4_fixed_by_family"] = fixed_by_family
    report["seq"]["s4_still_empty"]     = still_empty
    report["seq"]["s4_final_count"]     = seq_after_tc

    seq_problems = {}
    for e in seq_kept:
        p = e.get("problem", "") or e.get("vars", "") or e.get("family", "")
        seq_problems[p] = seq_problems.get(p, 0) + 1

    sub(f"Problem coverage: {len(seq_problems)} unique problems")
    for p, cnt in sorted(seq_problems.items(), key=lambda x: -x[1]):
        ln(f"  {p+':':55s} {cnt:>3}", 6)
    report["seq"]["problem_count"] = len(seq_problems)
    report["seq"]["problems"]      = seq_problems

    # =========================================================
    # COMBINED SUMMARY
    # =========================================================
    hdr("COMBINED SUMMARY")

    all_par_probs = set(par_problems)
    all_seq_probs = set(seq_problems)
    both  = all_par_probs & all_seq_probs
    p_only = all_par_probs - all_seq_probs
    s_only = all_seq_probs - all_par_probs

    ln(f"Problems with parallel algorithms:              {len(all_par_probs):>5}")
    ln(f"Problems with sequential algorithms:            {len(all_seq_probs):>5}")
    ln(f"Problems with BOTH par and seq data:            {len(both):>5}")
    ln(f"Problems with parallel data only:               {len(p_only):>5}")
    ln(f"Problems with sequential data only:             {len(s_only):>5}")
    if p_only:
        sub("Par-only problems")
        for p in sorted(p_only):
            ln(f"  {p}", 6)
    if s_only:
        sub("Seq-only problems")
        for p in sorted(s_only):
            ln(f"  {p}", 6)

    report["combined"] = {
        "par_problems": len(all_par_probs),
        "seq_problems": len(all_seq_probs),
        "problems_with_both": len(both),
        "par_only_problems": sorted(p_only),
        "seq_only_problems": sorted(s_only),
    }

    # =========================================================
    # EXCLUDED ENTRIES LIST  (non-underreviewed only)
    # =========================================================
    hdr("EXCLUDED ENTRIES  (all reasons except looked_at < 1)")

    par_excl_nla = [e for e in par_excl  if e["reason"] != "looked at"]
    seq_excl_nla = [e for e in seq_excl  if e["reason"] != "looked at"]

    ln(f"Parallel entries excluded (non-looked_at): {len(par_excl_nla)}")
    ln(f"Sequential entries excluded (non-looked_at): {len(seq_excl_nla)}")

    sub("Parallel excluded — sorted by family then year")
    for e in sorted(par_excl_nla, key=lambda x: (x.get("family",""), x.get("year",""))):
        label = EXCLUSION_LABELS.get(e["reason"], e["reason"])
        ln(f"  [{label}]", 6)
        ln(f"    family={e.get('family','')}  id={e.get('id','')}  "
           f"auth={e.get('auth','')}  year={e.get('year','')}", 6)

    sub("Sequential excluded — sorted by family then year")
    for e in sorted(seq_excl_nla, key=lambda x: (x.get("family",""), x.get("year",""))):
        label = EXCLUSION_LABELS.get(e["reason"], e["reason"])
        ln(f"  [{label}]", 6)
        ln(f"    family={e.get('family','')}  id={e.get('id','')}  "
           f"auth={e.get('auth','')}  year={e.get('year','')}", 6)

    report["par"]["excluded_non_lookedat"] = [
        {k: e.get(k,"") for k in ("reason","family","id","auth","year","problem","vars","model")}
        for e in par_excl_nla
    ]
    report["seq"]["excluded_non_lookedat"] = [
        {k: e.get(k,"") for k in ("reason","family","id","auth","year","problem","vars")}
        for e in seq_excl_nla
    ]

    # =========================================================
    # WRITE TEXT + JSON REPORTS
    # =========================================================
    text_path = os.path.join(output_dir, f"pipeline_report{version}.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(f"DATA PIPELINE REPORT — version {version}\n")
        f.write(f"Generated: {report['generated']}\n")
        f.write("\n".join(lines))
    print(f"Wrote text report → {text_path}")

    json_path = os.path.join(output_dir, f"pipeline_report{version}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
    print(f"Wrote JSON report → {json_path}")

    # =========================================================
    # VISUALIZATIONS
    # =========================================================
    # Collect year lists for histogram (entries that passed all filters)
    def _years(entry_list):
        years = []
        for e in entry_list:
            try:
                years.append(int(e.get("year", 0)))
            except (ValueError, TypeError):
                pass
        return [y for y in years if y > 1900]

    par_years = _years(par_simulated)
    seq_years = _years(seq_kept)

    if HAS_MPL:
        _plot_pipeline_report(
            report, par_excl_counts, seq_excl_counts,
            model_counts_raw, par_problems, seq_problems,
            par_years, seq_years,
            version, output_dir,
        )

    return report


def _plot_pipeline_report(report, par_excl_counts, seq_excl_counts,
                           model_counts_raw, par_problems, seq_problems,
                           par_years, seq_years,
                           version, output_dir):
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import os

    COLORS = {
        "kept":    "#4C9BE8",
        "excl":    "#E87C4C",
        "neutral": "#7DBF7D",
        "par":     "#4C9BE8",
        "seq":     "#E8C44C",
        "both":    "#9B59B6",
    }

    # ----------------------------------------------------------
    # Fig 1: Pipeline stage waterfall (par + seq side by side)
    # ----------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f"Data Pipeline — Entry Counts at Each Stage  [{version}]",
                 fontsize=13, fontweight="bold")

    for ax, dataset, label, color in [
        (axes[0], report["par"], "Parallel", COLORS["par"]),
        (axes[1], report["seq"], "Sequential", COLORS["seq"]),
    ]:
        if dataset == report["par"]:
            stages = [
                ("Raw CSV",            dataset["s0_raw"]),
                ("After field select", dataset["s1_after_field_select"]),
                ("Pass filters",       dataset["s2_kept"]),
                ("After type cast",    dataset["s3_after_typecast"]),
                ("Original dataset",   dataset["s4_original"]),
                ("Simulated dataset",  dataset["s4_simulated"]),
            ]
        else:
            stages = [
                ("Raw CSV",            dataset["s0_raw"]),
                ("After field select", dataset["s1_after_field_select"]),
                ("Pass filters",       dataset["s2_kept"]),
                ("After type cast",    dataset["s3_after_typecast"]),
                ("Final seq dataset",  dataset["s4_final_count"]),
            ]
        names  = [s[0] for s in stages]
        counts = [s[1] for s in stages]
        bars = ax.barh(names, counts, color=color, alpha=0.8, edgecolor="white")
        for bar, cnt in zip(bars, counts):
            ax.text(bar.get_width() + max(counts) * 0.01, bar.get_y() + bar.get_height() / 2,
                    str(cnt), va="center", fontsize=10)
        ax.set_xlabel("Number of entries")
        ax.set_title(f"{label} Pipeline")
        ax.invert_yaxis()
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.set_xlim(0, max(counts) * 1.15)

    plt.tight_layout()
    path = os.path.join(output_dir, f"pipeline_stages{version}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved → {path}")

    # ----------------------------------------------------------
    # Fig 2: Exclusion reasons — par and seq stacked bar
    # ----------------------------------------------------------
    all_reasons = list(dict.fromkeys(
        list(PARALLEL_DISCARABLE_FIELD_VALUES) +
        list(SEQUENTIAL_DISCARABLE_FIELD_VALUES)
    ))
    par_vals = [par_excl_counts.get(r, 0) for r in all_reasons]
    seq_vals = [seq_excl_counts.get(r, 0) for r in all_reasons]
    labels   = [EXCLUSION_LABELS.get(r, r) for r in all_reasons]

    # Only show reasons that actually excluded something
    nonzero = [(i, r) for i, r in enumerate(all_reasons)
               if par_vals[i] > 0 or seq_vals[i] > 0]
    idx    = [i for i, _ in nonzero]
    labels = [labels[i] for i in idx]
    pv     = [par_vals[i] for i in idx]
    sv     = [seq_vals[i] for i in idx]

    x = range(len(labels))
    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.35
    b1 = ax.bar([i - width/2 for i in x], pv, width, label="Parallel",
                color=COLORS["par"], alpha=0.8)
    b2 = ax.bar([i + width/2 for i in x], sv, width, label="Sequential",
                color=COLORS["seq"], alpha=0.8)
    for bar in list(b1) + list(b2):
        if bar.get_height() > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    str(int(bar.get_height())), ha="center", va="bottom", fontsize=8)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=9)
    ax.set_ylabel("Entries excluded")
    ax.set_title(f"Exclusion Reasons by Dataset  [{version}]")
    ax.legend()
    plt.tight_layout()
    path = os.path.join(output_dir, f"pipeline_exclusion_reasons{version}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved → {path}")

    # ----------------------------------------------------------
    # Fig 3: Parallel model distribution (all models in CSV)
    # ----------------------------------------------------------
    model_items = sorted(model_counts_raw.items(), key=lambda x: -x[1])
    m_names  = [MODEL_NAMES.get(m, f"Code {m}") for m, _ in model_items]
    m_counts = [c for _, c in model_items]
    allowable     = PARALLEL_ALLOWABLE_MODELS
    sim_allowable = PARALLEL_ALLOWABLE_MODELS | {700}
    bar_colors = []
    for m, _ in model_items:
        if m in allowable:
            bar_colors.append(COLORS["par"])
        elif m in sim_allowable:
            bar_colors.append(COLORS["both"])
        else:
            bar_colors.append(COLORS["excl"])

    fig, ax = plt.subplots(figsize=(12, 5))
    x_pos = range(len(m_names))
    bars = ax.bar(x_pos, m_counts, color=bar_colors, edgecolor="white")
    for bar, cnt in zip(bars, m_counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                str(cnt), ha="center", va="bottom", fontsize=8)
    ax.set_xticks(list(x_pos))
    ax.set_xticklabels(m_names, rotation=40, ha="right", fontsize=9)
    ax.set_ylabel("Number of parallel algorithms")
    ax.set_title(f"Parallel Algorithm Model Distribution  [{version}]")
    import matplotlib.patches as mpatches
    legend_handles = [
        mpatches.Patch(color=COLORS["par"],  label="In original + simulated datasets"),
        mpatches.Patch(color=COLORS["both"], label="Simulated dataset only"),
        mpatches.Patch(color=COLORS["excl"], label="Excluded from both"),
    ]
    ax.legend(handles=legend_handles)
    plt.tight_layout()
    path = os.path.join(output_dir, f"pipeline_model_distribution{version}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved → {path}")

    # ----------------------------------------------------------
    # Fig 4: Problem coverage — algorithms per problem (par + seq)
    # ----------------------------------------------------------
    all_probs = sorted(set(par_problems) | set(seq_problems))
    par_by_prob = [par_problems.get(p, 0) for p in all_probs]
    seq_by_prob = [seq_problems.get(p, 0) for p in all_probs]
    # Sort by total descending, keep top 40
    combined_sort = sorted(
        zip(all_probs, par_by_prob, seq_by_prob),
        key=lambda x: -(x[1] + x[2])
    )[:40]
    probs_s  = [x[0] for x in combined_sort]
    par_s    = [x[1] for x in combined_sort]
    seq_s    = [x[2] for x in combined_sort]

    fig, ax = plt.subplots(figsize=(16, 7))
    x = range(len(probs_s))
    ax.bar(x, par_s, label="Parallel algos",   color=COLORS["par"],  alpha=0.85)
    ax.bar(x, seq_s, bottom=par_s, label="Sequential algos", color=COLORS["seq"], alpha=0.85)
    ax.set_xticks(list(x))
    ax.set_xticklabels(probs_s, rotation=55, ha="right", fontsize=7)
    ax.set_ylabel("Number of algorithms")
    ax.set_title(f"Algorithms per Problem (top 40 by total)  [{version}]")
    ax.legend()
    plt.tight_layout()
    path = os.path.join(output_dir, f"pipeline_problem_coverage{version}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved → {path}")

    # ----------------------------------------------------------
    # Fig 5: Year distribution of accepted entries
    # ----------------------------------------------------------
    import numpy as np
    decade_bins = list(range(1950, 2035, 5))  # 5-year buckets from 1950

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=False)
    fig.suptitle(f"Year Distribution of Accepted Algorithms  [{version}]",
                 fontsize=12, fontweight="bold")

    for ax, years, label, color in [
        (axes[0], par_years, f"Parallel (simulated, n={len(par_years)})", COLORS["par"]),
        (axes[1], seq_years, f"Sequential (n={len(seq_years)})",          COLORS["seq"]),
    ]:
        clipped = [y for y in years if decade_bins[0] <= y <= decade_bins[-1]]
        pre = sum(1 for y in years if y < decade_bins[0])
        ax.hist(clipped, bins=decade_bins, color=color, alpha=0.8, edgecolor="white")
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of algorithms")
        ax.set_title(label)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
        plt.setp(ax.get_xticklabels(), rotation=40, ha="right")
        if pre:
            ax.text(0.02, 0.97, f"+ {pre} entries before {decade_bins[0]}",
                    transform=ax.transAxes, va="top", fontsize=8, color="gray")

    plt.tight_layout()
    path = os.path.join(output_dir, f"pipeline_year_distribution{version}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved → {path}")

    print("Pipeline report visualizations complete.")


if __name__ == '__main__':
    # convert_csv_to_json("Parallel_Algos_MAY1")
    # filter_unwanted_fields_json("Parallel_Algos_MAY1",PARALLEL_ALGO_FIELDS)
    # filter_unwanted_algos("Parallel_Algos_MAY1",PARALLEL_DISCARABLE_FIELD_VALUES)

    #wut?^^^^

    create_par_data("Parallel_Algos_MAY1")
    print("DONE WITH PARALLEL")
    #technically should probably use this one but im just copying the old ones and changing the version name
    create_seq_data("Sheet1_MAY1","Sheet1_New_Entries_MAY1")

    pass