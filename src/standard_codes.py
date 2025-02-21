
"""
Dictionaries mapping codes to data interpreting (dictionaries mapping data numbers to what they mean)
"""

# models
model_dict = {
    100: "PRAM (unspecified)",
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
    600: "Other",
    610: "External Memory",
    700: "Distributed Memory",
    800: "Word RAM (Sequential)"
}

# complexity classes
# the number assignments are (I hope) logical; often it's i: n^{i//10}*log^{i%10}(n)
TIME_CODES = {
    0: "$O(1)$",
    0.001: "$O(\log^*{n})$",
    0.1: "$O(\log{\log{n}})$",
    0.2: "$O(\log^2 {\log{n}})$",
    0.84: "$O(\log{n}^{1/2} / \log{\log{n}}^{3/2})$",
    0.85: "$O(\log{n}^{1/2} / \log{\log{n}}^{1/2})$",
    0.9: "$O(\log{n}/\log{\log{n}})$",
    1: "$O(\log{n})$",
    1.001: "$O(\log{n} \log^*{n})$",
    1.05: "$O(\log{n} \log{\log{\log{n}}})$",
    1.1: "$O(\log{n} \log{\log{n}})$",
    1.101: "$O(\log{n} \log{\log{n}} 2^{\log^*{n}})$",
    1.15: "$O(\log{n} \log^2{\log{n}})$",
    1.29: "$O(\log{n}^{4/3} / \log{\log{n}}^{1/3})$",
    1.5: "$O(\log^{3/2}{n})$",
    2: "$O(\log^2{n})$",
    2.001: "$O(\log^2{n} \log^*{n})$",
    2.07: "$O(\log^2{n} \log{\log{n}}^3)$",
    2.1: "$O(\log^2{n} \log{\log{n}})$",
    3: "$O(\log^3{n})$",
    4: "$O(\log^4{n})$",
    5: "$O(\log^c{n})$",
    5.009: "$O(2^{\log{n}^{0.5}})$",
    5.01: "$O(2^{\log{n}^{0.5}} \log{n} / \log{\log{n}}^2)$",
    5.02: "$O(n^\epsilon)$",
    5.021: "$O(n^\epsilon \log{n})$",
    5.024: "$O(n^{0.00025} \log{n})$",
    5.025: "$O(n^{(\log{7}-\log{143640}/\log{70})/2})$",
    5.03: "$O(n^{0.062})$",
    5.5: "$O(n^{0.25})$",
    5.51: "$O(n^{1/4} \log{n})$",
    5.53: "$O(n^{0.312})$",
    5.54: "$O(n^{0.3135} \log^4{n})$",
    5.545: "$O(n^{0.314} \log^4{n})$",
    5.55: "$O(n^{0.3145} \log^4{n})$",
    5.6: "$O(n^{1/3})$",
    5.61: "$O(n^{1/3 + \epsilon})$",
    5.8: "$O(n^{1/2}/ \log^2{n})$",
    5.9: "$O(n^{1/2}/ \log{n})$",
    6: "$O(n^{1/2})$",
    6.01: "$O(n^{1/2} \log{\log{n}})$",
    6.1: "$O(n^{1/2} \log{n})$",
    6.11: "$O(n^{1/2} \log{n} \log{\log{n}})$",
    6.129: "$O(n^{1/2} \log{n}^{4/3} / \log{\log{n}}^{1/3})$",
    6.2: "$O(n^{1/2} \log^2{n})$",
    6.23: "$O(n^{1/2} \log^3{n})$",
    6.27: "$O(n^{\log{3}-1})$",
    6.5: "$O(n^{0.6})$",
    7: "$O(n^{0.627} \log^2{\log{n}}/\log^2{n})$",
    7.15: "$O(n^{2/3-\epsilon} \log^c{n})$",
    7.2: "$O(n^{2/3})$",
    7.31: "$O(n^{0.69356805} \log{n})$",
    7.5: "$O(n^{0.75})$",
    7.501: "$O(n^{0.75} \log{\log{n}})$",
    7.51: "$O(n^{0.75} \log{n})$",
    8: "$O(n^{\log{7}-2} \log{n})$",
    8.1: "$O(n^{0.9})$",
    8.3: "$O(n^{1-\epsilon})$",
    8.301: "$O(n^{1-\epsilon} \log^*{n})$",
    8.31: "$O(n^{1-\epsilon} \log{n})$",
    8.5: "$O(n/\log^c{n})$",
    8.7: "$O(n/\log^4{n})$",
    8.8: "$O(n/\log^3{n})$",
    8.895: "$O(n / (\log^2{n} \log^*{n}})$",
    8.9: "$O(n/\log^2{n})$",
    8.9005: "$O(n \alpha(n) /\log^2{n})$",
    8.94: "$O(n / (\log{n} \log{\log{n}} 2^{\log^*{n}}))$",
    8.95: "$O(n / (\log{n} \log{\log{n}}))$",
    8.99: "$O(n / (\log{n} \log^*{n}})$",
    9: "$O(n/\log{n})$",
    9.0005: "$O(n \alpha(n) /\log{n})$",
    9.05: "$O(n \log{\log{n}} / \log{n})$",
    9.06: "$O(n \log^2{\log{n}} / \log{n})$",
    9.08: "$O(n / \log^{1/2}{n})$",
    9.09: "$O(n / \log^2{\log{n}})$",
    9.1: "$O(n/\log{\log{n}})$",
    9.2: "$O(n/\log{\log{\log{n}}})$",
    9.999: "$O(n/\log^*{n})$",
    10: "$O(n)$",
    10.0005: "$O(n \alpha(n))$",
    10.001: "$O(n \log^*{n})$",
    10.1: "$O(n \log{\log{n}})$",
    10.2: "$O(n \log^2{\log{n}})$",
    10.4: "$O(n \log^\epsilon{n})$",
    10.5: "$O(n \log^{1/2}{n})$",
    10.9: "$O(n \log{n} / \log{\log{n}})$",
    10.95: "$O(n \log{n} \log{\log{\log{n}}} / \log{\log{n}})$",
    11: "$O(n \log{n})$",
    11.09: "$O(n \log{n} \log{\log{n}} / \log{\log{\log{n}}})$",
    11.1: "$O(n \log{n} \log{\log{n}})$",
    11.2: "$O(n \log{n} \log{\log{n}}^2)$",
    11.3: "$O(n \log{n} \log{\log{n}}^3)$",
    11.41: "$O(n \log^{1+\epsilon}{n} / \log{\log{n}})$",
    11.5: "$O(n \log^{3/2}{n})$",
    11.585: "$O(n \log^{1.585}{n})$",
    12: "$O(n \log^2{n})$",
    12.001: "$O(n \log^2{n} \log^*{n})$",
    13: "$O(n \log^3{n})$",
    13.1: "$O(n \log^3{n} \log{\log{n}})$",
    14: "$O(n \log^4{n})$",
    15: "$O(n \log^c{n})$",
    15.011: "$O(n^{1+1/\log{n}} \log{n})$",
    15.012: "$O(n^{1+1/\log{n}} \log^2{n})$",
    15.019: "$O(n^{1+3\epsilon} / \log{n})$",
    15.097: "$O(n^{1.1855})$",
    15.099: "$O(n^{1.186})$",
    15.101: "$O(n^{1.18643195})$",
    15.103: "$O(n^{1.1864365})$",
    15.104: "$O(n^{1.1865})$",
    15.105: "$O(n^{1.1865} \log{n})$",
    15.107: "$O(n^{1.18775})$",
    15.109: "$O(n^{1.188})$",
    15.11: "$O(n^{1.188} \log{n})$",
    15.23: "$O(n^{\log{54}/(2 \log{5})})$",
    15.236: "$O(n^{1.24})$",
    15.238: "$O(n^{1.2475})$",
    15.24: "$O(n^{1.247774})$",
    15.25: "$O(n^{1.25})$",
    15.26: "$O(n^{1.258325})$",
    15.262: "$O(n^{1.259})$",
    15.264: "$O(n^{1.26})$",
    15.28: "$O(n^{1.305})$",
    15.4: "$O(n^{4/3})$",
    15.41: "$O(n^{4/3} \log{n})$",
    15.46: "$O(n^{1.39})$",
    15.47: "$O(n^{\log{143640}/(2 \log{70})})$",
    15.48: "$O(n^{1.4})$",
    15.481: "$O(n^{1.4035})$",
    15.49: "$O(n^{\log{7}/2} / \log{n})$",
    15.5: "$O(n^{\log{7}/2})$",
    15.6: "$O(n^{\log{7}/2} \log{n})$",
    15.602: "$O(n^{\log{7}/2} \log^3{n})$",
    15.603: "$O(n^{\log{7}/2+0.25})$",
    15.605: "$O(n^{\log{7}/2+0.25} \log^2{n})$",
    15.61: "$O(n^{1.4255})$",
    15.612: "$O(n^{1.4255} \log^2{n})$",
    15.614: "$O(n^{10/7} \log^c{n})$",
    15.7: "$O(n^{1.46})$",
    15.92: "$O(n^{1.5} /2^{(\log n)^{0.5}})$",
    15.925: "$O(n^{1.5} \log{\log{n}}^{3/2}/\log{n}^{5/2})$",
    15.93: "$O(n^{1.5}/\log^2{n})$",
    15.94: "$O(n^{1.5}/ (\log{n} \log{\log{n}}))$",
    15.95: "$O(n^{1.5}/\log{n})$",
    15.96: "$O(n^{1.5} \log{\log{n}}/\log{n})$",
    15.97: "$O(n^{1.5} \log{\log{n}}^2/\log{n})$",
    15.98: "$O(n^{1.5} \log{\log{n}}^{3/2}/\log{n}^{1/2})$",
    15.992: "$O(n^{1.5} \log{\log{n}}^3 / \log{n}^2)$",
    15.994: "$O(n^{1.5} \log{\log{n}}^{1/2} / \log{n}^{3/2})$",
    15.996: "$O(n^{1.5} \log{\log{n}}^{1/2} / \log{n}^{1/2})$",
    15.998: "$O(n^{1.5} \log{\log{n}}^{1/3} / \log{n}^{1/3})$",
    15.999: "$O(n^{1.5} / \log{\log{n}})$",
    15.9995: "$o(n^{1.5})$",
    16: "$O(n^{1.5})$",
    16.01: "$O(n^{1.5} \log{\log{n}})$",
    16.06: "$O(n^{1.5} \log{n}^{1/2} \log{\log{n}}^{1/2})$",
    16.07: "$O(n^{1.5} \log{n} / \log{\log{n}})$",
    16.1: "$O(n^{1.5} \log{n})$",
    16.2: "$O(n^{1.5} \log^2{n})$",
    16.23: "$O(n^{1.5} \log^3{n})$",
    16.24: "$O(n^{1.5} \log^4{n})$",
    16.27: "$O(n^{\log{3}})$",
    16.4: "$O(n^{1.6})$",
    16.5: "$O(n^{5/3})$",
    16.9: "$O(n^{11/6} \log{n})$",
    17.9: "$O(n^2/\log^3{n})$",
    17.99: "$O(n^2/ (\log^2{n}\log{\log{n}}))$",
    18: "$O(n^2/\log^2{n})$",
    19: "$O(n^2/\log{n})$",
    19.9: "$O(n^2/\log{\log{n}})$",
    20: "$O(n^2)$",
    20.1: "$O(n^2 \log{\log{n}})$",
    21: "$O(n^2 \log{n})$",
    21.1: "$O(n^2 \log{n} \log{\log{n}})$",
    21.5: "$O(n^2 \log^{3/2}{n})$",
    22: "$O(n^2 \log^2{n})$",
    23: "$O(n^2 \log^3{n})$",
    25: "$O(n^2 \log^c{n})$",
    25.02: "$O(n^{2 + 2\epsilon})$",
    26.1: "$O(n^{2.373} \log n)$",
    26.11: "$O(n^{2.376} \log n)$",
    26.5: "$O(n^{5/2})$",
    26.6: "$O(n^{5/2} \log{n})$",
    26.7: "$O(n^{1+\log{3}})$",
    27: "$O(n^{\log{7}}/\log{n})$",
    27.5: "$O(n^{\log{7}})$",
    28: "$O(n^{\log{7}} \log{n})$",
    29.2: "$O(n^3 \log{\log{n}}^{3/2}/\log{n}^{5/2})$",
    29.3: "$O(n^3/\log{n}^2)$",
    29.4: "$O(n^3 \log{\log{n}}^{1/2}/\log{n}^{3/2})$",
    29.45: "$O(n^3/(\log{n} \log{\log{n}}))$",
    29.5: "$O(n^3/\log{n})$",
    29.6: "$O(n^3 \log{\log{n}}/\log{n})$",
    29.7: "$O(n^3 \log{\log{n}}^2/\log{n})$",
    29.8: "$O(n^3 \log{\log{n}}^{3/2}/\log{n}^{1/2})$",
    29.999: "$o(n^3)$",
    30: "$O(n^3)$",
    30.1: "$O(n^3 \log{\log{n}})$",
    30.6: "$O(n^3 \log{n}^{1/2} \log{\log{n}}^{1/2})$",
    31: "$O(n^3 \log{n})$",
    32: "$O(n^3 \log^2{n})$",
    33: "$O(n^3 \log^3{n})$",
    33.7: "$O(n^{1.5+\log{3}})$",
    35: "$O(n^{3.25})$",
    35.3: "$O(n^{3.25} \log^3{n})$",
    36.5: "$O(n^{7/2})$",
    40: "$O(n^4)$",
    40.1: "$O(n^4 \log{\log{n}})$",
    41: "$O(n^4 \log{n})$",
    43: "$O(n^4 \log^3{n})$",
    44.8: "$O(n^{4.5} \log^3{n})$",
    46: "$O(n^5/ \log^4{n})$",
    49: "$O(n^5 / \log{n})$",
    51: "$O(n^5 \log{n})$",
    55.4: "$O(n^6/ \log^6{n})$",
    55.5: "$O(n^6/ \log^5{n})$",
    56: "$O(n^6/ \log^4{n})$",
    57: "$O(n^6/ \log^3{n})$",
    58: "$O(n^6/ \log^2{n})$",
    59: "$O(n^6/ \log{n})$",
    60: "$O(n^6)$",
    61: "$O(n^6 \log{n})$",
    62: "$O(n^6 \log^2{n})$",
    65.3: "$O(n^{6.5} \log^3{n})$",
    70: "$O(n^7)$",
    80: "$O(n^8)$",
    90: "$O(n^9)$",
    92: "$O(n^9 \log^2{n})$",
    937.9: "$O(2^{\sqrt{n} \log{3}/3} / (\sqrt{n} \log{n}))$",
    938: "$O(2^{\sqrt{n} \log{3}/3})$",
    938.1: "$O(2^{\sqrt{n} \log{3}/3} n)$",
    940: "$O(2^{\sqrt{n}})$",
    941.5: "$O(2^{\sqrt{n}} n^{1.5})$",
    942: "$O(2^{\sqrt{n}} n^2)$",
    944: "$O(2^{\sqrt{n}} n^c)$",
    950: "$O(4^{\sqrt{n}})$",
    951.5: "$O(n^{1.5} 4^{\sqrt{n}})$",
    960: "$2^{O(\sqrt{n})}$",
    974: "$O(2^{\epsilon n}/n)$",
    984: "$O(2^{n/8})$",
    986: "$O(2^{n/4})$",
    986.1: "$O(2^{n/4} n)$",
    986.9: "$O(2^{\log{1.2852}n})$",
    987: "$O(2^{3n/8})$",
    987.8: "$O(2^{n/2} / n^2)$",
    987.9: "$O(2^{n/2} / n)$",
    988: "$O(2^{n/2})$",
    988.1: "$O(2^{n/2} n)$",
    988.2: "$O(2^{n/2} n^2)$",
    990: "$O(2^n / n)$",
    991: "$O(2^n \log{n} / n)$",
    1000: "$O(2^n)$",
    1000.5: "-",
    1010: "$O(2^n n)$",
    1020: "$O(2^n n^2)$",
    1045: "$O(2^n n^c)$",
    1099: "$O(2^{n+\epsilon})$",
    1515: "$O(2^{1.5n} n^{1.5})$",
    1984: "$O(2^{2n} / n^{1.5})$",
    2000: "$O(2^{2n})$",
    2020: "$O(2^{2n} n^2)$",
    2021: "$O(2^{2n} n^2 \log{n})$",
    2070.5: "$O(2^{n(2+\epsilon)}/n^3)$",
    2090.5: "$O(2^{n(2+\epsilon)}/n)$",
    2091.5: "$O(2^{n(2+\epsilon)} \log{n} / n)$",
    3011: "$O(2^{3n} n \log{n})$",
    6000.5: "$O(2^{n(6+\epsilon)})$",
    7091.5: "$O(2^{n(7+\epsilon)} \log{n} / n)$",
    8000: "$O(\log^n{\log{n}})$",
    8001: "$O(\log{n} \log^{n-1}{\log{n}})$",
    8010: "$O(n \log^n{\log{n}})$",
    8011: "$O(n \log{n} \log^{n-1}{\log{n}})$",
    9000: "$O(n!)$",
    9001: "$O(n n!)$",
    9122: "$O(2^n n^{2n + 2})$",
    9200: "$O(2^{2n^2})$",
    9305: "$O(2^{\log{5} n^3})$",
}

def multiply_by_log(code):
    # TODO: map new_code to old codes
    if code in {0,2,3}:
        new_code = code+1
    assert new_code in TIME_CODES
    return new_code

problem_dict = {
    13.1: "Strongly Connected Components",
    14.1: "Minimum Spanning Tree",
    17: "All Pairs Shortest Paths",
    33: "Generating Random Permutations",
    'APSP': "All Pairs Shortest Paths",
    #adding \n so it splits into two lines in graphs
    'LCS': "Longest Common\nSubsequence",
    '2-Dimensional Delaunay Triangulation':'2-Dimensional Delaunay Triangulation',
    '1D Maximum Subarray': '1D Maximum Subarray',
    '2-Player': '2-Player Nash Equilibria',
    'MST': "Minimum Spanning Tree",
    'General Graph MCM': 'General Graph MCM',
    'General Root Computation': 'General Root Computation',
    'directed APSP': 'Directed All Pairs Shortest Paths',
    'Bipartite Graph MCM': 'Bipartite Graph Maximum\nCardinality Matching',
    'Topological Sorting': 'Topological Sorting'
}

var_weight_dict = {
    "Comparison Sorting": {"family": "Sorting", "number": 1, "thesis_weight": 1, "equal_weight": 0.5},
    "Non-comparison Sorting": {"family": "Sorting", "number": 1, "thesis_weight": 1, "equal_weight": 0.5},
    "kth Order Statistic": {"family": "kth Order Statistic", "number": 2, "thesis_weight": 1, "equal_weight": 1},
    "MCOP": {"family": "Matrix Chain Multiplication", "number": 3, "thesis_weight": 1, "equal_weight": 0.5},
    "Matrix Chain Scheduling Problem": {"family": "Matrix Chain Multiplication", "number": 3, "thesis_weight": 1, "equal_weight": 0.5},
    "LCS": {"family": "Longest Common Subsequence", "number": 4, "thesis_weight": 1, "equal_weight": 1},
    "Max Flow": {"family": "Maximum Flow", "number": 5, "thesis_weight": 1, "equal_weight": 1},
    "Matrix Multiplication": {"family": "Matrix Product", "number": 6, "thesis_weight": 1, "equal_weight": 0.5},
    "Boolean Matrix Multiplication": {"family": "Matrix Product", "number": 6, "thesis_weight": 1, "equal_weight": 0.5},
    "k-Graph Coloring": {"family": "Graph Coloring", "number": 7.5, "thesis_weight": 1, "equal_weight": 1},
    "General Linear System": {"family": "Linear System", "number": 9, "thesis_weight": 1, "equal_weight": 1},
    "General Linear Programming": {"family": "Linear Programming", "number": 10, "thesis_weight": 1, "equal_weight": 1},
    "Reporting intersection points": {"family": "Line segment intersection", "number": 11, "thesis_weight": 1, "equal_weight": 0.5},
    "Intersection detection": {"family": "Line segment intersection", "number": 11, "thesis_weight": 1, "equal_weight": 0.5},
    "2-dimensional Convex Hull": {"family": "Convex Hull", "number": 12, "thesis_weight": 1, "equal_weight": 0.5},
    "3-dimensional Convex Hull": {"family": "Convex Hull", "number": 12, "thesis_weight": 1, "equal_weight": 0.5},
    "CC": {"family": "Strongly Connected Components", "number": 13, "thesis_weight": 1, "equal_weight": 0.25},
    "Transitive Closure": {"family": "Strongly Connected Components", "number": 13, "thesis_weight": 1, "equal_weight": 0.25},
    "SCCs": {"family": "Strongly Connected Components", "number": 13, "thesis_weight": 1, "equal_weight": 0.25},
    "Transitive Closure of a symmetric Boolean matrix": {"family": "Strongly Connected Components", "number": 13, "thesis_weight": 1, "equal_weight": 0.25},
    "MST": {"family": "Minimum Spanning Tree (MST)", "number": 14, "thesis_weight": 1, "equal_weight": 0.5},
    "directed MST": {"family": "Minimum Spanning Tree (MST)", "number": 14, "thesis_weight": 1, "equal_weight": 0.5},
    "2-dimensional space Closest Pair Problem": {"family": "Closest Pair Problem", "number": 15, "thesis_weight": 1, "equal_weight": 0.5},
    "k-dimensional space Closest Pair Problem": {"family": "Closest Pair Problem", "number": 15, "thesis_weight": 1, "equal_weight": 0.5},
    "undirected nonneg SSSP": {"family": "Shortest Path (Directed Graphs)", "number": 16, "thesis_weight": 1, "equal_weight": 0.25},
    "directed nonneg SSSP": {"family": "Shortest Path (Directed Graphs)", "number": 16, "thesis_weight": 1, "equal_weight": 0.25},
    "directed SSSP": {"family": "Shortest Path (Directed Graphs)", "number": 16, "thesis_weight": 1, "equal_weight": 0.25},
    "undirected SSSP": {"family": "Shortest Path (Directed Graphs)", "number": 16, "thesis_weight": 1, "equal_weight": 0.25},
    "directed APSP": {"family": "All-Pairs Shortest Paths (APSP)", "number": 17, "thesis_weight": 1, "equal_weight": 0.5},
    "APSP": {"family": "All-Pairs Shortest Paths (APSP)", "number": 17, "thesis_weight": 1, "equal_weight": 0.5},
    "Integer Factoring": {"family": "Integer Factoring", "number": 18, "thesis_weight": 1, "equal_weight": 1},
    "Matrix LU Decomposition": {"family": "LU Decomposition", "number": 20, "thesis_weight": 1, "equal_weight": 1},
    "Single String Search": {"family": "String Search", "number": 22, "thesis_weight": 1, "equal_weight": 1},
    "Edit Distance, constant-size alphabet": {"family": "Sequence Alignment", "number": 23, "thesis_weight": 1, "equal_weight": 1},
    "Convex Polygonal Window": {"family": "Line Clipping", "number": 25, "thesis_weight": 1, "equal_weight": 1},
    "Multiplication": {"family": "Multiplication", "number": 27, "thesis_weight": 1, "equal_weight": 1},
    "Bipartite Graph MCM": {"family": "Maximum Cardinality Matching", "number": 28, "thesis_weight": 1, "equal_weight": 0.5},
    "General Graph MCM": {"family": "Maximum Cardinality Matching", "number": 28, "thesis_weight": 1, "equal_weight": 0.5},
    "Exact Laplacian Solver": {"family": "SDD Systems Solver", "number": 31, "thesis_weight": 1, "equal_weight": 1},
    "General Permutations": {"family": "Generating Random Permutations", "number": 33, "thesis_weight": 1, "equal_weight": 1},
    "Convex Optimization (Non-linear)": {"family": "Convex Optimization (Non-linear)", "number": 34, "thesis_weight": 1, "equal_weight": 1},
    "All Permutations": {"family": "All Permutations", "number": 37, "thesis_weight": 1, "equal_weight": 1},
    "OBST": {"family": "Optimal Binary Search Trees", "number": 38, "thesis_weight": 1, "equal_weight": 1},
    "2-Player Nash Equilibria": {"family": "Nash Equilibria", "number": 39, "thesis_weight": 1, "equal_weight": 1},
    "n-Player Nash Equilibria": {"family": "Nash Equilibria", "number": 39, "thesis_weight": 1, "equal_weight": 0},
    "Bipartite Maximum-Weight Matching": {"family": "Maximum-Weight Matching", "number": 40, "thesis_weight": 1, "equal_weight": 0.5},
    "General Maximum-Weight Matching": {"family": "Maximum-Weight Matching", "number": 40, "thesis_weight": 1, "equal_weight": 0.5},
    "Constructing Eulerian Trails in a Graph": {"family": "Constructing Eulerian Trails in a Graph", "number": 41, "thesis_weight": 1, "equal_weight": 1},
    "Discrete Fourier Transform": {"family": "Discrete Fourier Transform", "number": 42, "thesis_weight": 1, "equal_weight": 1},
    "Line Drawing": {"family": "Line Drawing", "number": 43, "thesis_weight": 1, "equal_weight": 1},
    "Polygon Clipping with Arbitrary Clipping Polygon": {"family": "Polygon Clipping", "number": 44, "thesis_weight": 1, "equal_weight": 1},
    "General Root Computation": {"family": "Root Computation", "number": 48, "thesis_weight": 1, "equal_weight": 1},
    "k Nearest Neighbors Search": {"family": "Nearest Neighbor Search", "number": 49, "thesis_weight": 1, "equal_weight": 0.5},
    "All Nearest Neighbors": {"family": "Nearest Neighbor Search", "number": 49, "thesis_weight": 1, "equal_weight": 0.5},
    "Coset Enumeration": {"family": "Coset Enumeration", "number": 50, "thesis_weight": 1, "equal_weight": 1},
    "Maximum Likelihood Parameters": {"family": "Maximum Likelihood Parameters", "number": 51, "thesis_weight": 1, "equal_weight": 1},
    "Constuct Voronoi Diagram": {"family": "Voronoi Diagrams", "number": 54, "thesis_weight": 1, "equal_weight": 1},
    "Variance Calculations": {"family": "Variance Calculations", "number": 55, "thesis_weight": 1, "equal_weight": 1},
    "Topological Sorting": {"family": "Topological Sorting", "number": 56, "thesis_weight": 1, "equal_weight": 1},
    "DFA Minimization": {"family": "DFA Minimization", "number": 57, "thesis_weight": 1, "equal_weight": 1},
    "Lowest Common Ancestor": {"family": "Lowest Common Ancestor", "number": 58, "thesis_weight": 1, "equal_weight": 1},
    "Exact GED": {"family": "Graph Edit Distance Computation", "number": 59, "thesis_weight": 1, "equal_weight": 1},
    "Enumerating Maximal Cliques": {"family": "Clique Problems", "number": 60, "thesis_weight": 1, "equal_weight": 0.5},
    "k-Clique": {"family": "Clique Problems", "number": 60.4, "thesis_weight": 1, "equal_weight": 0.5},
    "The Traveling-Salesman Problem": {"family": "The Traveling-Salesman Problem", "number": 61, "thesis_weight": 1, "equal_weight": 1},
    "2-Dimensional Poisson Problem": {"family": "Poisson Problem", "number": 62, "thesis_weight": 1, "equal_weight": 0.5},
    "3-Dimensional Poisson Problem": {"family": "Poisson Problem", "number": 63, "thesis_weight": 1, "equal_weight": 0.5},
    "2-Dimensional Delaunay Triangulation": {"family": "Delaunay Triangulation", "number": 64, "thesis_weight": 1, "equal_weight": 0.5},
    "3-Dimensional Delaunay Triangulation": {"family": "Delaunay Triangulation", "number": 64, "thesis_weight": 1, "equal_weight": 0.5},
    "De Novo Genome Assembly": {"family": "De Novo Genome Assembly", "number": 65, "thesis_weight": 1, "equal_weight": 1},
    "Subset Sum": {"family": "The Subset-Sum Problem", "number": 66, "thesis_weight": 1, "equal_weight": 1},
    "Disk Scheduling": {"family": "Disk Scheduling", "number": 71, "thesis_weight": 1, "equal_weight": 1},
    "The Vertex Cover Problem": {"family": "The Vertex Cover Problem", "number": 72, "thesis_weight": 1, "equal_weight": 1},
    "CFG Parsing": {"family": "CFG Problems", "number": 73, "thesis_weight": 1, "equal_weight": 1},
    "Finding Frequent Itemsets": {"family": "Finding Frequent Itemsets", "number": 74, "thesis_weight": 1, "equal_weight": 1},
    "Lossless Compression": {"family": "Data Compression", "number": 75, "thesis_weight": 1, "equal_weight": 1},
    "Stable Marriage Problem": {"family": "Stable Matching Problem", "number": 78, "thesis_weight": 1, "equal_weight": 1},
    "Longest Path on Interval Graphs": {"family": "Longest Path", "number": 79, "thesis_weight": 1, "equal_weight": 1},
    "1D Maximum Subarray": {"family": "Maximum Subarray Problem", "number": 80, "thesis_weight": 1, "equal_weight": 0.5},
    "2D Maximum Subarray": {"family": "Maximum Subarray Problem", "number": 80, "thesis_weight": 1, "equal_weight": 0.5},
    "Constructing Suffix Trees": {"family": "Constructing Suffix Trees", "number": 81, "thesis_weight": 1, "equal_weight": 1},
    "Entity Resolution": {"family": "Entity Resolution", "number": 83, "thesis_weight": 1, "equal_weight": 1},
    "Graph Isomorphism, General Graphs": {"family": "Graph Isomorphism Problem", "number": 86, "thesis_weight": 1, "equal_weight": 1},
    "Collaborative Filtering": {"family": "Collaborative Filtering", "number": 92, "thesis_weight": 1, "equal_weight": 1},
    "Optimal Policies for MDPs": {"family": "Optimal Policies for MDPs", "number": 97, "thesis_weight": 1, "equal_weight": 1},
    "Motif Search": {"family": "Motif Search", "number": 99, "thesis_weight": 1, "equal_weight": 1},
    "Link Analysis": {"family": "Link Analysis", "number": 153, "thesis_weight": 1, "equal_weight": 1},
    "Point-in-Polygon": {"family": "Point-in-Polygon", "number": 107, "thesis_weight": 1, "equal_weight": 1},
    "Maximum Cut": {"family": "Maximum Cut", "number": 117, "thesis_weight": 1, "equal_weight": 1},
    "Determinant of Matrices with Integer Entries": {"family": "Determinants", "number": 119, "thesis_weight": 1, "equal_weight": 1},
    "Integer Relation": {"family": "Integer Relation", "number": 120, "thesis_weight": 1, "equal_weight": 1},
    "Transitive Reduction Problem of Directed Graphs": {"family": "Transitive Reduction Problem", "number": 129, "thesis_weight": 1, "equal_weight": 1},
    "Volterra-Abel Equations": {"family": "Integral Equations", "number": 137, "thesis_weight": 1, "equal_weight": 0.5},
    "Fredholm Equations": {"family": "Integral Equations", "number": 137, "thesis_weight": 1, "equal_weight": 0.5},
    "Solutions to Nonlinear Equations": {"family": "Solutions to Nonlinear Equations", "number": 140, "thesis_weight": 1, "equal_weight": 1},
    "2-D Polynomial Interpolation": {"family": "Polynomial Interpolation", "number": 142, "thesis_weight": 1, "equal_weight": 1},
    "Greatest Common Divisor": {"family": "Greatest Common Divisor", "number": 143, "thesis_weight": 1, "equal_weight": 1},
}

def check_family_weight_sum(weight_dict,weight_type):
    '''
    Checks that all the variation weights of every family sum up to one
    weight_dict: dictionary mapping variations to dict of "family" and weight_type
    weight_type: weighting scheme to use (e.g. "equal_weight")
    '''
    fams = {}
    for var in weight_dict:
        fams[weight_dict[var]["family"]] = 0 if (weight_dict[var]["family"] not 
                                in fams) else fams[weight_dict[var]["family"]]
        fams[weight_dict[var]["family"]] += weight_dict[var][weight_type]
    for fam in fams:
        assert fams[fam] == 1

check_family_weight_sum(var_weight_dict,"equal_weight")

CODE_DIVISON = {
    (16.1,2.1): 15.94,
    (92.0, 12.0): 80.0,
    (21.0, 20.0): 1.0,
    (15.5, 15.11): 5.51, # TODO: not actually, but it's the closest
    (12.0, 11.0): 1.0,
    (30.0, 11.0): 19.0,
    (11.0, 10.0): 1.0,
    (16.2, 10.0): 6.2,
    (10.0, 6.1): 5.9,
    (15.97, 15.92): 5.01,
    (16.0, 15.25): 5.5,
    (21.0, 20.0): 1.0,
    (21.0, 11.0): 10.0,
    (20.1, 16.0): 6.01,
    (15.0, 10.0): 5.0,
    (16.1, 10.0): 6.1,
    (60.0, 11.0): 49.0,
    (12.0, 10.0): 2.0,
    (20.0, 10.0): 10.0,
    (16.24, 16.0): 4.0,
    (2090.5, 20.0): 2070.5,
    (12.0, 2.1): 9.1,
    (2090.5, 2000.0): 974.0,
    (11.0, 2.1): 8.95,
    (16.0, 10.0): 6.0,
    (16.1, 15.998): 1.29,
    (13.0, 11.0): 2.0,
    (16.1, 11.0): 6.0,
    (21.1, 20.0): 1.1,
    (10.1, 10.0): 0.1,
    (21.0, 15.998): 6.129,
    (21.0, 11.1): 9.1,
    (16.0, 15.996): 0.85,
    (11.0, 10.1): 0.9,
    (16.1, 15.95): 2,
    (15.11, 15.101): 7.31,
    (16.0, 15.109): 5.53,
    (21.0, 19.0): 2,
    (20.1, 15.25): 7.501,
    (30.0, 20.0): 10,
    (16.24, 15.104): 5.54,
    (16.24, 15.097): 5.55,
    (16.0, 15.92): 5.009,
    (15.5, 15.47): 5.025,
    (57.0, 11.0): 46,
    (15.11, 15.107): 5.024,
    (15.25, 15.109): 5.03,
    (1010.0, 988.0): 988.1,
    (16.24, 15.099): 5.545,
    (20.0, 10.1): 19.9,
    (16.0, 15.98): 0.84,
    (25.02, 20.0): 5.02,
    (988.1, 988.0): 10,
    (16.0, 15.992): 2.07,
    (44.8, 20.0): 26.7, # TODO
}

CODE_MULTIPLICATION = {
    (10.0,2.0): 12.0,
    (15.6,2.0): 15.602,
}

# TODO: change format (e.g. dict with all options)
# complexity categories separating complexities near O(1)
# good for spans
def get_category_1_list():
    return ["constant", "log log", "logarithmic", "$log^2$", "polylogarithmic", 
            "sublinear", "linear", "$n \log n$", "$n \log^2 n$", "quadratic", 
            "cubic","exponential"]

def complexity_category_1(num):
    if num <= 0.001:
        return "constant"
    # elif num <= 0.1:
    #     return "log log"
    elif num <=1:
        return "logarithmic"
    # elif num <=2:
    #     return "$\log^2$"
    elif num <=5:
        return "polylog"
    elif num <=9.998:
        return "sublinear"
    elif num <=10:
        return "linear"
    # elif num <=11:
    #     return "$n \log n$"
    # elif num <=12:
    #     return "$n \log^2 n$"
    elif num <=20:
        return "quadratic"
    elif num <= 30:
        return "cubic"
    else:
        return "supracubic/\nexponential"
    
# complexity categories separating complexities near O(n)
def complexity_category_n(num):
    if num <= 10.001:
        return "linear"
    # elif num <= 10.1:
    #     return "n log log"
    elif num <=11:
        return "$n \log n$"
    # elif num <=12:
    #     return "$n \log^2$"
    elif num <=15:
        return "n$\cdot$polylogarithmic"
    elif num <=19.998:
        return "sub-quadratic"
    elif num <=20:
        return "quadratic"
    elif num <=21:
        return "$n^2 \log n$"
    elif num <=22:
        return "$n^2 \log^2 n$"
    elif num <=30:
        return "cubic"
    elif num <= 40:
        return "$n^4$"
    else:
        return "more than $n^4$"
    
# complexity categories separating complexities near O(n^2)
def complexity_category_n2(num):
    raise NotImplementedError

# TODO
def work_category(num):
    return TIME_CODES[num]


DECADES = [{"max": 1950, "label": "40s"}, 
            {"max": 1960, "label": "50s"}, 
            {"max": 1970, "label": "60s"}, 
            {"max": 1980, "label": "70s"}, 
            {"max": 1990, "label": "80s"}, 
            {"max": 2000, "label": "90s"}, 
            {"max": 2010, "label": "00s"}, 
            {"max": 2020, "label": "10s"}, 
            {"max": 2030, "label": "20s"},]

DECADE_LIST = ["pre-1900s", "1900s", "1910s", "1920s", "1930s", "1940s", "1950s", 
               "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
# given a year gives the decade
def get_decade(year):
    if year <= 1900:
        return "pre-1900s"
    elif year <= 1910:
        return "1900s"
    elif year <= 1920:
        return "1910s"
    elif year <= 1930:
        return "1920s"
    elif year <= 1940:
        return "1930s"
    elif year <= 1950:
        return "1940s"
    elif year <= 1960:
        return "1950s"
    elif year <= 1970:
        return "1960s"
    elif year <= 1980:
        return "1970s"
    elif year <= 1990:
        return "1980s"
    elif year <= 2000:
        return "1990s"
    elif year <= 2010:
        return "2000s"
    elif year <= 2020:
        return "2010s"
    elif year <= 2030:
        return "2020s"
    else:
        raise ValueError("This was written in 2023, if you're from the future you need to update this function. Input: "+str(year))
