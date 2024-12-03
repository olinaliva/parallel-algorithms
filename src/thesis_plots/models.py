from header import *
import csv


# model_mapping: a dict mapping model codes to their less restrictive category
# model code
def make_model_plots(model_data_name,model_mapping):

    # jsonArray = []
    # csvFilePath = r'./data/'+model_data_name+r'.csv'
    # jsonFilePath = r'./data/'+model_data_name+r'_raw.json'
    # with open(csvFilePath, encoding='utf-8') as csvf: 
    #     csvReader = csv.DictReader(csvf)
    #     for row in csvReader: 
    #         jsonArray.append(row)

            
    jsonFilePath = r'./'+model_data_name+r'.json'
    jsonFile = open(jsonFilePath, 'r')
    jsonArray = json.load(jsonFile)

    complexity_model_codes = list(model_dict.keys()) # [100,110,120,130,131,132,...]
    complexity_models = [model_dict[x] for x in complexity_model_codes] # ["PRAM","PRAM-erew",...]

    all_used_model_code_indeces = {}

    data_old_format = {}
    print(len(jsonArray))
    for data_point in jsonArray: 
        model_code = model_mapping[int(data_point["model"])]
        model = complexity_model_codes.index(model_code)
        all_used_model_code_indeces[model] = 0
        year = int(data_point["year"])

        if (model,year) in data_old_format:
            # increase freq
            data_old_format[(model,year)]["freq"] += 1
        else:
            # add data point
            decade = DECADE_LIST.index(get_decade(year))
            data_old_format[(model,year)] = {
                "year": year,
                "model": model,
                "decade": decade,
                "freq": 1
            }

    new_codes = []
    new_models = []
    i=0
    for model_index in sorted(list(all_used_model_code_indeces.keys())):
        new_codes.append(complexity_model_codes[model_index])
        new_models.append(complexity_models[model_index])
        all_used_model_code_indeces[model_index] = i
        i += 1
    
    total_freqs = 0
    for datapoint in data_old_format:
        old_ind = data_old_format[datapoint]["model"]
        data_old_format[datapoint]["model"] = all_used_model_code_indeces[old_ind]
        total_freqs += data_old_format[datapoint]["freq"] 

    # print(data_old_format)

    old_make_model_plots(data_old_format,complexity_models=new_models,avail_decades=DECADE_LIST)


    pass




OLD_MODELS = ["", "PRAM-CRCW", "PRAM-CREW", "PRAM-EREW", "Other PRAMs", 
                         "SIMD", "MIMD", "Sort Models", "WordRAM", "Other models"]
OLD_DEC = ["","60s","70s","80s","90s","2000s","2010s","2020s"]
# old but remade a litle
def old_make_model_plots(data,complexity_models=OLD_MODELS,avail_decades=OLD_DEC):
    actual_colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', 
                '#00ffff', '#777777', '#7700ff', '#469990']
    # all_colors # list(mcolors.TABLEAU_COLORS.values()) + all_colors
    try:
        actual_colors.remove("")
    except:
        pass
    names = list(data.keys())
    names.sort(key= lambda name: (data[name]["year"], -1*data[name]["model"]))
    years = [data[name]["year"] for name in names]
    models = [data[name]["model"] for name in names]
    freqs = [data[name]["freq"] for name in names]
    decades = [data[name]["decade"] for name in names]
    colors = [actual_colors[data[name]["model"]] for name in names] # c=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    model_ranges = list(range(0,len(complexity_models)))

    decade_als = {}
    for dec in range(0,len(avail_decades)):
        for m in range(0,len(complexity_models)):
            total_freq = sum(v["freq"] for k, v in data.items() if v["decade"] == dec and v["model"]==m)
            if total_freq > 0:
                decade_als[str(dec)+str(m)] = {"model": m, "decade": dec, "freq": total_freq}
    dec_decades = [decade_als[name]["decade"] for name in decade_als.keys()]
    dec_models = [decade_als[name]["model"] for name in decade_als.keys()]
    # dec_colors = [actual_colors[decade_als[name]["model"]] for name in decade_als.keys()]
    dec_freqs = [decade_als[name]["freq"] for name in decade_als.keys()]
    dec_sizes = [decade_als[name]["freq"]**2 for name in decade_als.keys()]
    
    # 2 - SCATTER PLOT were dot sizes are based on frequency
    fig, ax = plt.subplots(1,1,figsize=(7.5,3.5),dpi=200,layout='tight')
    ax.grid(axis='y', alpha=0.4)
    sizes = [4*f**2 for f in freqs]
    ax.scatter(years, models, c=colors, s=sizes)
    ax.set_yticks(model_ranges)
    ax.set_yticklabels(complexity_models)
    ax.set_title("Computational Models Throughout Time")
    ax.set_ylabel("Computational Model")
    ax.set_xlabel("Year")
    ax.xaxis.get_major_locator().set_params(integer=True)
    # handles = []
    # for i in range(0,len(complexity_models)):
    #     new_patch = mpatches.Patch(color=str(actual_colors[i]), label=complexity_models[i])
    #     handles.append(new_patch)
    # ax.legend(handles=handles,loc='center left', bbox_to_anchor=(1, 0.5), title="Models")
    # plt.show()
    # plt.savefig(SAVE_LOC+'models2_new_colors.png')

    # 5 - STACKED BAR CHART
    print(decade_als)
    weight_counts = {}
    for m in range(len(complexity_models)):
        weight_counts[m] = [0]*len(avail_decades[7:]) # TODO: hardcoded
    for name in decade_als.keys():
        weight_counts[decade_als[name]["model"]][decade_als[name]["decade"]-7] = decade_als[name]["freq"]
    width = 0.5
    fig, ax = plt.subplots(1,1,figsize=(8.5,4.5),dpi=200,layout='tight')
    bottom = np.zeros(len(avail_decades)-7)
    for boolean, weight_count in weight_counts.items():
        p = ax.bar(avail_decades[7:], weight_count, width, label=complexity_models[boolean], bottom=bottom,color=actual_colors[boolean])
        bottom += weight_count
    ax.set_title("Computational Models Throughout Time")
    ax.set_ylabel("Number of Algoritms")
    ax.set_xlabel("Decade")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()
    # plt.savefig(SAVE_LOC+'models5_new_colors.png')





    