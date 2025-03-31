# parallel-algorithms

This is the code for the improvements in parallel algorithms project. It generates plots and other information to analyze parallel algorithms.

The **Plots** and **Preliminary Plots** folders house the generated plots. Newly-created plots get saved here by default. The specific folder location can be changed in **header.py**.  
The **data** folder has data files in various stages of being ready to use, as well as some code to process said data.  
The **project** folder contains the code to generate the plots. It also has the following:  
    - **complexity_functions.py**: all helper functions that compute asymptotic time  
    - **huge_num.py**: a class for handling very large numbers with not very large precision  
    - **processed_data.py**: stores complementary data (such as processor data) and function calls for reading the main algorithms data  
    - **standard_codes.py**: stores mappings of codes (used to interpret the data) to their meanings  
    - **helper_functions.py**: miscellanious helper functions


The main way to use this is to comment/uncomment calls to functions in the **main.py** file. Most parameters (such as colors, the main parallel model, or the location of saved plots) can be changed in **header.py**. An exception is changing the version of the data to be generated, which can be done in **src/processed_data.py**.

That's the overview. If you have any questions, feel free to email me at dtontici@mit.edu.

# Branch updates
For for thesis code see original github and dtontici@mit.edu
The branch is for code for paper data and figures
Once it's finalized I will make it pretty-er, easier to navigate and update this README, in the meantime contact lolina@mit.edu with questions
