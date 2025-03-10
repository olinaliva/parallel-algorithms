import math
import decimal
from .huge_num import Huge

EPS = 0.01
POLY_EXP = 6
OFFSET = 0.5
BIG_O_CONST = 5

def log_star(n, b): 
    '''
    log star function
    '''
    def _log(x, base):     
        return (int)(math.log(x) / math.log(base))
    if(n > 1.0):
        return 1.0 + log_star(_log(n, b), b)
    else:
        return 0

def alpha(n):
    '''
    inverse Ackermann function
    given A(m,m) returns m
    '''
    if n <= 3:
        return 1
    elif n <= 7:
        return 2
    elif n <= 61:
        return 3
    # elif n <= 2**(2**(2**65533))-3: # computing this takes way too long
    #     return 4
    return 4 # return 5

def stirling(n):
    '''
    computes factorial approximation, using Stirling's formula
    '''
    return (2*math.pi*n)**0.5 * Huge(n/math.e,n)


#############################################################################################


def bo26(n):
    return n**2*max(math.log(n,2),1)
def bo26_const(n):
    return 1.5*n**2*max(math.log(n,2),1) + 2*n**2 + 2*n*max(math.log(n,2),1)

def yao75(n):
    return n**2*max(math.log(max(math.log(n,2),1),2),1)
def yao75_const(n):
    return 3*n**2*max(math.log(max(math.log(n,2),1),2),1) + 2.5*n**2 + 2*n**2/max(math.log(n,2),1) + 2*n

def ct76(n):
    return n**2
def ct76_const(n):
    return 8*n**2+4*n

def sh53(n):
    return n**4
def sh53_const(n):
    return n**4

def fw62(n):
    return n**3
def fw62_const(n):
    return n**3

def fr76(n):
    return n**3 * (max(math.log(max(math.log(n,2),1),2),1) / max(math.log(n,2),1))**(1/3)
def fr76_const(n):
    return n**3 * (max(math.log(max(math.log(n,2),1),2),1) / max(math.log(n,2),1))**(1/3)

def ta92(n):
    return n**3 * (max(math.log(max(math.log(n,2),1),2),1) / max(math.log(n,2),1))**(1/2)
def ta92_const(n):
    return n**3 * (max(math.log(max(math.log(n,2),1),2),1) / max(math.log(n,2),1))**(1/2)

def ta04(n):
    return n**3 * (max(math.log(max(math.log(n,2),1),2),1))**2 / max(math.log(n,2),1)
def ta04_const(n):
    return n**3 * (max(math.log(max(math.log(n,2),1),2),1))**2 / max(math.log(n,2),1)

def ch09(n):
    return n**3 * (max(math.log(max(math.log(n,2),1),2),1))**3 / (max(math.log(n,2),1))**2
def ch09_const(n):
    return n**3 * (max(math.log(max(math.log(n,2),1),2),1))**3 / (max(math.log(n,2),1))**2

def wi14(n):
    return n**3 /2**((max(math.log(n,2),1))**0.5)
def wi14_const(n):
    return n**3 /2**((max(math.log(n,2),1))**0.5)


#############################################################################################


def comp_fn_0_0000(n):
    return 1
def comp_fn_0_0010(n):
    return max(log_star(n,2),1)
def comp_fn_0_1000(n):
    return max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_0_2000(n):
    return max(math.log(max(math.log(n,2),1),2),1)**2
def comp_fn_0_8500(n):
    return max(math.log(n,2),1)**0.5 / max(math.log(max(math.log(n,2),1),2),1)**0.5
def comp_fn_0_9000(n):
    return max(math.log(n,2),1) / max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_1_0000(n):
    return max(math.log(n,2),1)
def comp_fn_1_0010(n):
    return max(math.log(n,2),1) * log_star(n,2)
def comp_fn_1_0500(n):
    return max(math.log(n,2),1) * max(math.log(max(math.log(max(math.log(n,2),1),2),1),2),1)
def comp_fn_1_1000(n):
    return max(math.log(n,2),1) * max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_1_1010(n):
    return max(math.log(n,2),1) * max(math.log(max(math.log(n,2),1),2),1) * 2**(log_star(n,2))
def comp_fn_1_1500(n):
    return max(math.log(n,2),1) * max(math.log(max(math.log(n,2),1),2),1)**2
def comp_fn_1_2900(n):
    return max(math.log(n,2),1)**(4/3) * max(math.log(max(math.log(n,2),1),2),1)**(1/3)
def comp_fn_1_5000(n):
    return max(math.log(n,2),1)**1.5
def comp_fn_2_0000(n):
    return max(math.log(n,2),1)**2
def comp_fn_2_0010(n):
    return max(math.log(n,2),1)**2 * log_star(n,2)
def comp_fn_2_1000(n):
    return max(math.log(n,2),1)**2 * max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_3_0000(n):
    return max(math.log(n,2),1)**3
def comp_fn_4_0000(n):
    return max(math.log(n,2),1)**4
def comp_fn_5_0000(n):
    return max(math.log(n,2),1)**POLY_EXP


def comp_fn_5_1000(n):
    return 2**(max(math.log(n,2),1)**{0.5}) * max(math.log(n,2),1) / max(math.log(max(math.log(n,2),1),2),1)**2
def comp_fn_5_0200(n):
    return n**EPS
def comp_fn_5_0210(n):
    return n**EPS * max(math.log(n,2),1)
def comp_fn_5_5000(n):
    return n**0.25
def comp_fn_5_5100(n):
    return n**0.25 * max(math.log(n,2),1)
def comp_fn_5_5300(n):
    return n**0.312
def comp_fn_5_5400(n):
    return n**0.3135 * max(math.log(n,2),1)**4
def comp_fn_5_5500(n):
    return n**0.3145 * max(math.log(n,2),1)**4
def comp_fn_5_6000(n):
    return n**(1/3)
def comp_fn_5_6100(n):
    return n**(1/3+EPS)
def comp_fn_5_8000(n):
    return n**0.5 / max(math.log(n,2),1)**2
def comp_fn_5_9000(n):
    return n**0.5 / max(math.log(n,2),1)
def comp_fn_6_0000(n):
    return n**0.5
def comp_fn_6_0100(n):
    return n**0.5 * max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_6_1000(n):
    return n**0.5 * max(math.log(n,2),1)
def comp_fn_6_1100(n):
    return n**0.5 * max(math.log(n,2),1) * max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_6_1290(n):
    return n**0.5 * max(math.log(n,2),1)**(4/3) * max(math.log(max(math.log(n,2),1),2),1)**(1/3)
def comp_fn_6_2000(n):
    return n**0.5 * max(math.log(n,2),1)**2
def comp_fn_6_2300(n):
    return n**0.5 * max(math.log(n,2),1)**3
def comp_fn_6_2700(n):
    return n**(math.log(3,2)-1)
def comp_fn_6_5000(n):
    return n**0.6
def comp_fn_7_0000(n):
    return n**0.627 * max(math.log(max(math.log(n,2),1),2),1)**2 / max(math.log(n,2),1)**2
def comp_fn_7_1500(n):
    return n**(2/3-EPS) * max(math.log(n,2),1)**POLY_EXP
def comp_fn_7_2000(n):
    return n**(2/3)
def comp_fn_7_3100(n):
    return n**0.69356805 * max(math.log(n,2),1)
def comp_fn_7_5000(n):
    return n**0.75
def comp_fn_7_5010(n):
    return n**0.75 * max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_7_5100(n):
    return n**0.75 * max(math.log(n,2),1)
def comp_fn_8_0000(n):
    return n**(math.log(7,2)-2) * max(math.log(n,2),1)
def comp_fn_8_1000(n):
    return n**0.9
def comp_fn_8_3000(n):
    return n**(1-EPS)
def comp_fn_8_3010(n):
    return n**(1-EPS)*log_star(n,2)
def comp_fn_8_3100(n):
    return n**(1-EPS) * max(math.log(n,2),1)
def comp_fn_8_5000(n):
    return n / max(math.log(n,2),1)**POLY_EXP
def comp_fn_8_7000(n):
    return n / max(math.log(n,2),1)**4
def comp_fn_8_8000(n):
    return n / max(math.log(n,2),1)**3
def comp_fn_8_8950(n):
    return n / (max(math.log(n,2),1)**2 * log_star(n,2))
def comp_fn_8_9000(n):
    return n / max(math.log(n,2),1)**2
def comp_fn_8_9005(n):
    return n * alpha(n) / max(math.log(n,2),1)**2
def comp_fn_8_9400(n):
    return n / (max(math.log(n,2),1) * max(math.log(max(math.log(n,2),1),2),1) * 2**log_star*n,2)
def comp_fn_8_9500(n):
    return n / (max(math.log(n,2),1) * max(math.log(max(math.log(n,2),1),2),1))
def comp_fn_8_9900(n):
    return n / (max(math.log(n,2),1) * log_star*n,2)
def comp_fn_9_0000(n):
    return n / max(math.log(n,2),1)
def comp_fn_9_0005(n):
    return n * alpha(n) / max(math.log(n,2),1)
def comp_fn_9_0500(n):
    return n * max(math.log(max(math.log(n,2),1),2),1) / max(math.log(n,2),1)
def comp_fn_9_0600(n):
    return n * max(math.log(max(math.log(n,2),1),2),1)**2 / max(math.log(n,2),1)
def comp_fn_9_0800(n):
    return n / max(math.log(n,2),1)**0.5
def comp_fn_9_0900(n):
    return n / max(math.log(max(math.log(n,2),1),2),1)**2
def comp_fn_9_1000(n):
    return n / max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_9_2000(n):
    return n / max(math.log(max(math.log(max(math.log(n,2),1),2),1),2),1)
def comp_fn_9_9990(n):
    return n / max(log_star(n,2),1)
def comp_fn_10_0000(n):
    return n


def comp_fn_10_0005(n):
    return n * alpha(n)
def comp_fn_10_0010(n):
    return n * log_star(n,2)
def comp_fn_10_1000(n):
    return n * max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_10_2000(n):
    return n * max(math.log(max(math.log(n,2),1),2),1)**2
def comp_fn_10_4000(n):
    return n * max(math.log(n,2),1)**EPS
def comp_fn_10_5000(n):
    return n * max(math.log(n,2),1)**0.5
def comp_fn_10_9000(n):
    return n * max(math.log(n,2),1) / max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_10_9500(n):
    return n * max(math.log(n,2),1) * max(math.log(max(math.log(max(math.log(n,2),1),2),1),2),1) / max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_11_0000(n):
    return n * max(math.log(n,2),1)
def comp_fn_11_0900(n):
    return n * max(math.log(n,2),1) * max(math.log(max(math.log(n,2),1),2),1) / max(math.log(max(math.log(max(math.log(n,2),1),2),1),2),1)
def comp_fn_11_1000(n):
    return n * max(math.log(n,2),1) * max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_11_2000(n):
    return n * max(math.log(n,2),1) * max(math.log(max(math.log(n,2),1),2),1)**2
def comp_fn_11_3000(n):
    return n * max(math.log(n,2),1) * max(math.log(max(math.log(n,2),1),2),1)**3
def comp_fn_11_4100(n):
    return n * max(math.log(n,2),1)**(1+EPS) / max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_11_5000(n):
    return n * max(math.log(n,2),1)**1.5
def comp_fn_11_5850(n):
    return n * max(math.log(n,2),1)**1.585
def comp_fn_12_0000(n):
    return n * max(math.log(n,2),1)**2
def comp_fn_12_0010(n):
    return n * max(math.log(n,2),1)**2 * log_star(n,2)
def comp_fn_13_0000(n):
    return n * max(math.log(n,2),1)**3
def comp_fn_13_1000(n):
    return n * max(math.log(n,2),1)**3 * max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_14_0000(n):
    return n * max(math.log(n,2),1)**4
def comp_fn_15_0000(n):
    return n * max(math.log(n,2),1)**POLY_EXP


def comp_fn_15_0110(n):
    return n**(1+1/max(math.log(n,2),1)) * max(math.log(n,2),1)
def comp_fn_15_0120(n):
    return n**(1+1/max(math.log(n,2),1)) * max(math.log(n,2),1)**2
def comp_fn_15_0190(n):
    return n**(1+3*EPS) / max(math.log(n,2),1)
def comp_fn_15_0970(n):
    return n**1.1855
def comp_fn_15_0990(n):
    return n**1.186
def comp_fn_15_1010(n):
    return n**1.18643195
def comp_fn_15_1030(n):
    return n**1.1864365
def comp_fn_15_1040(n):
    return n**1.1865
def comp_fn_15_1050(n):
    return n**1.1865 * max(math.log(n,2),1)
def comp_fn_15_1070(n):
    return n**1.18775
def comp_fn_15_1090(n):
    return n**1.188
def comp_fn_15_1100(n):
    return n**1.188 * max(math.log(n,2),1)
def comp_fn_15_2300(n):
    return n**(math.log(54,5)/2)
def comp_fn_15_2360(n):
    return n**1.24
def comp_fn_15_2380(n):
    return n**1.2475
def comp_fn_15_2400(n):
    return n**1.247774
def comp_fn_15_2500(n):
    return n**1.25
def comp_fn_15_2600(n):
    return n**1.258325
def comp_fn_15_2620(n):
    return n**1.259
def comp_fn_15_2640(n):
    return n**1.26
def comp_fn_15_2800(n):
    return n**1.305
def comp_fn_15_4000(n):
    return n**(4/3)
def comp_fn_15_4100(n):
    return n**(4/3) * max(math.log(n,2),1)
def comp_fn_15_4600(n):
    return n**1.39
def comp_fn_15_4700(n):
    return n**(math.log(143640,70)/2)
def comp_fn_15_4800(n):
    return n**1.4
def comp_fn_15_4810(n):
    return n**1.4035
def comp_fn_15_4900(n):
    return n**(math.log(7,2)/2) / max(math.log(n,2),1)
def comp_fn_15_5000(n):
    return n**(math.log(7,2)/2)
def comp_fn_15_6000(n):
    return n**(math.log(7,2)/2) * max(math.log(n,2),1)
def comp_fn_15_6020(n):
    return n**(math.log(7,2)/2) * max(math.log(n,2),1)**3
def comp_fn_15_6030(n):
    return n**(math.log(7,2)/2+0.25)
def comp_fn_15_6050(n):
    return n**(math.log(7,2)/2+0.25) * max(math.log(n,2),1)**2
def comp_fn_15_6100(n):
    return n**1.4255
def comp_fn_15_6120(n):
    return n**1.4255 * max(math.log(n,2),1)**2
def comp_fn_15_6140(n):
    return n**(10/7) * max(math.log(n,2),1)**POLY_EXP
def comp_fn_15_7000(n):
    return n**1.46


def comp_fn_15_9200(n):
    return n**1.5 /2**((max(math.log(n,2),1))**0.5)
def comp_fn_15_9250(n):
    return n**1.5 * max(math.log(max(math.log(n,2),1),2),1)**1.5 / max(math.log(n,2),1)**2.5
def comp_fn_15_9300(n):
    return n**1.5 / max(math.log(n,2),1)**2
def comp_fn_15_9400(n):
    return n**1.5 / (max(math.log(n,2),1) * max(math.log(max(math.log(n,2),1),2),1))
def comp_fn_15_9500(n):
    return n**1.5 / max(math.log(n,2),1)
def comp_fn_15_9600(n):
    return n**1.5 * max(math.log(max(math.log(n,2),1),2),1) / max(math.log(n,2),1)
def comp_fn_15_9700(n):
    return n**1.5 * max(math.log(max(math.log(n,2),1),2),1)**2 / max(math.log(n,2),1)
def comp_fn_15_9800(n):
    return n**1.5 * max(math.log(max(math.log(n,2),1),2),1)**1.5 / max(math.log(n,2),1)**0.5


def comp_fn_15_9920(n):
    return n**1.5 * max(math.log(max(math.log(n,2),1),2),1)**3 / max(math.log(n,2),1)**2
def comp_fn_15_9940(n):
    return n**1.5 * max(math.log(max(math.log(n,2),1),2),1)**(1/2) / max(math.log(n,2),1)**(3/2)
def comp_fn_15_9960(n):
    return n**1.5 * (max(math.log(max(math.log(n,2),1),2),1) / max(math.log(n,2),1))**(1/2)
def comp_fn_15_9980(n):
    return n**1.5 * (max(math.log(max(math.log(n,2),1),2),1) / max(math.log(n,2),1))**(1/3)
def comp_fn_15_9990(n):
    return n**1.5 / max(math.log(max(math.log(n,2),1),2),1)


def comp_fn_15_9995(n):
    return n**1.5-OFFSET
def comp_fn_16_0000(n):
    return n**1.5
def comp_fn_16_0100(n):
    return n**1.5 * max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_16_0600(n):
    return n**1.5 * max(math.log(n,2),1)**0.5 * max(math.log(max(math.log(n,2),1),2),1)**0.5
def comp_fn_16_0700(n):
    return n**1.5 * max(math.log(n,2),1) / max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_16_1000(n):
    return n**1.5 * max(math.log(n,2),1)
def comp_fn_16_2000(n):
    return n**1.5 * max(math.log(n,2),1)**2
def comp_fn_16_2300(n):
    return n**1.5 * max(math.log(n,2),1)**3
def comp_fn_16_2400(n):
    return n**1.5 * max(math.log(n,2),1)**4
def comp_fn_16_2700(n):
    return n**math.log(3,2)
def comp_fn_16_4000(n):
    return n**1.6
def comp_fn_16_5000(n):
    return n**(5/3)
def comp_fn_16_9000(n):
    return n**(11/6) * max(math.log(n,2),1)
def comp_fn_17_9000(n):
    return n**2 * max(math.log(n,2),1)**3
def comp_fn_17_9900(n):
    return n**2 / (max(math.log(n,2),1)**2 * max(math.log(max(math.log(n,2),1),2),1))
def comp_fn_18_0000(n):
    return n**2 / max(math.log(n,2),1)**2
def comp_fn_19_0000(n):
    return n**2 / max(math.log(n,2),1)
def comp_fn_19_9000(n):
    return n**2 / max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_20_0000(n):
    return n**2
def comp_fn_20_1000(n):
    return n**2 * max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_21_0000(n):
    return n**2 * max(math.log(n,2),1)
def comp_fn_21_1000(n):
    return n**2 * max(math.log(n,2),1) * max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_21_5000(n):
    return n**2 * max(math.log(n,2),1)**1.5
def comp_fn_22_0000(n):
    return n**2 * max(math.log(n,2),1)**2
def comp_fn_23_0000(n):
    return n**2 * max(math.log(n,2),1)**3
def comp_fn_25_0000(n):
    return n**2 * max(math.log(n,2),1)**POLY_EXP
def comp_fn_25_0200(n):
    return n**(2+2*EPS)
def comp_fn_26_1000(n):
    return n**2.373 * max(math.log(n,2),1)
def comp_fn_26_1100(n):
    return n**2.376 * max(math.log(n,2),1)
def comp_fn_26_5000(n):
    return n**2.5
def comp_fn_26_6000(n):
    return n**2.5 * max(math.log(n,2),1)
def comp_fn_26_7000(n):
    return n**(1+math.log(3,2))
def comp_fn_27_0000(n):
    return n**math.log(7,2) / max(math.log(n,2),1)
def comp_fn_27_5000(n):
    return n**math.log(7,2)
def comp_fn_28_0000(n):
    return n**math.log(7,2) * max(math.log(n,2),1)


def comp_fn_29_2000(n):
    return n**3 * max(math.log(max(math.log(n,2),1),2),1)**1.5 / max(math.log(n,2),1)**2.5
def comp_fn_29_3000(n):
    return n**3 / max(math.log(n,2),1)**2
def comp_fn_29_4000(n):
    return n**3 * max(math.log(max(math.log(n,2),1),2),1)**0.5 / max(math.log(n,2),1)**1.5
def comp_fn_29_4500(n):
    return n**3 / (max(math.log(max(math.log(n,2),1),2),1) * max(math.log(n,2),1))
def comp_fn_29_5000(n):
    return n**3 / max(math.log(n,2),1)
def comp_fn_29_6000(n):
    return n**3 * max(math.log(max(math.log(n,2),1),2),1) / max(math.log(n,2),1)
def comp_fn_29_7000(n):
    return n**3 * max(math.log(max(math.log(n,2),1),2),1)**2 / max(math.log(n,2),1)
def comp_fn_29_8000(n):
    return n**3 * max(math.log(max(math.log(n,2),1),2),1)**1.5 / max(math.log(n,2),1)**0.5

def comp_fn_29_9950(n):
    return n**3 /2**((max(math.log(n,2),1))**0.5)
def comp_fn_29_9960(n):
    return n**3 * (max(math.log(max(math.log(n,2),1),2),1))**3 / (max(math.log(n,2),1))**2
def comp_fn_29_9970(n):
    return n**3 * (max(math.log(max(math.log(n,2),1),2),1))**2 / max(math.log(n,2),1)
def comp_fn_29_9980(n):
    return n**3 * (max(math.log(max(math.log(n,2),1),2),1) / max(math.log(n,2),1))**(1/2)
def comp_fn_29_9985(n):
    return n**3 * (max(math.log(max(math.log(n,2),1),2),1) / max(math.log(n,2),1))**(1/3)
def comp_fn_29_9990(n):
    return n**3-OFFSET
def comp_fn_30_0000(n):
    return n**3
def comp_fn_30_1000(n):
    return n**3 * max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_30_6000(n):
    return n**3 * max(math.log(n,2),1)**0.5 * max(math.log(max(math.log(n,2),1),2),1)**0.5
def comp_fn_31_0000(n):
    return n**3 * max(math.log(n,2),1)
def comp_fn_32_0000(n):
    return n**3 * max(math.log(n,2),1)**2
def comp_fn_33_0000(n):
    return n**3 * max(math.log(n,2),1)**3
def comp_fn_33_7000(n):
    return n**(1.5+math.log(3,2))
def comp_fn_35_0000(n):
    return n**3.25
def comp_fn_35_3000(n):
    return n**3.25 * max(math.log(n,2),1)**3
def comp_fn_36_5000(n):
    return n**3.5
def comp_fn_40_0000(n):
    return n**4


def comp_fn_40_1000(n):
    return n**4 * max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_41_0000(n):
    return n**4 * max(math.log(n,2),1)
#hopefully this one is correct
def comp_fn_41_1000(n):
    return n**4 * max(math.log(n,2),1) * max(math.log(max(math.log(n,2),1),2),1)
def comp_fn_43_0000(n):
    return n**4 * max(math.log(n,2),1)**3
def comp_fn_44_8000(n):
    return n**4.5 * max(math.log(n,2),1)**3
def comp_fn_49_0000(n):
    return n**5 / max(math.log(n,2),1)
def comp_fn_51_0000(n):
    return n**5 * max(math.log(n,2),1)
#added, hopefully correct
def comp_fn_52_0000(n):
    return n**5 * max(math.log(n,2),1)**2
def comp_fn_55_4000(n):
    return n**6 / max(math.log(n,2),1)**6
def comp_fn_55_5000(n):
    return n**6 / max(math.log(n,2),1)**5
def comp_fn_56_0000(n):
    return n**6 / max(math.log(n,2),1)**4
def comp_fn_57_0000(n):
    return n**6 / max(math.log(n,2),1)**3
def comp_fn_58_0000(n):
    return n**6 / max(math.log(n,2),1)**2
def comp_fn_59_0000(n):
    return n**6 / max(math.log(n,2),1)
def comp_fn_60_0000(n):
    return n**6
def comp_fn_61_0000(n):
    return n**6 * max(math.log(n,2),1)
def comp_fn_62_0000(n):
    return n**6 * max(math.log(n,2),1)**2
def comp_fn_65_3000(n):
    return n**6.5 * max(math.log(n,2),1)**3
def comp_fn_70_0000(n):
    return n**7
def comp_fn_80_0000(n):
    return n**8
def comp_fn_90_0000(n):
    return n**9
def comp_fn_92_0000(n):
    return n**9 * max(math.log(n,2),1)**2


#this is poly(n), coding as n^16 i guess?
def comp_fn_400_0000(n):
    return n**16
def comp_fn_937_9000(n):
    return Huge(2,math.sqrt(n)*math.log(3,2)/3) / (math.sqrt(n)*math.log(n,2))
def comp_fn_938_0000(n):
    return Huge(2,math.sqrt(n)*math.log(3,2)/3)
def comp_fn_938_1000(n):
    return Huge(2,math.sqrt(n)*math.log(3,2)/3) * n
def comp_fn_940_0000(n):
    return Huge(2,math.sqrt(n))
def comp_fn_941_5000(n):
    return Huge(2,math.sqrt(n)) * n**1.5
def comp_fn_942_0000(n):
    return Huge(2,math.sqrt(n)) * n**2
def comp_fn_944_0000(n):
    return Huge(2,math.sqrt(n)) * n**POLY_EXP
def comp_fn_950_0000(n):
    return Huge(4,n**0.5)
def comp_fn_951_5000(n):
    return Huge(4,n**0.5) * n**1.5
def comp_fn_960_0000(n):
    return Huge(2,BIG_O_CONST*n**0.5)
def comp_fn_974_0000(n):
    return Huge(2,EPS) / n
def comp_fn_984_0000(n):
    return Huge(2,n/8)
def comp_fn_986_0000(n):
    return Huge(2,n/4)
def comp_fn_986_1000(n):
    return Huge(2,n/4) * n
def comp_fn_986_9000(n):
    return Huge(2,n*math.log(1.2852,2)) * n
def comp_fn_987_0000(n):
    return Huge(2,3*n/8)
def comp_fn_987_8000(n):
    return Huge(2,n/2) / n**2
def comp_fn_987_9000(n):
    return Huge(2,n/2) / n
def comp_fn_988_0000(n):
    return Huge(2,n/2)
def comp_fn_988_1000(n):
    return Huge(2,n/2) * n
def comp_fn_988_2000(n):
    return Huge(2,n/2) * n**2
def comp_fn_990_0000(n):
    return Huge(2,n) / n
def comp_fn_991_0000(n):
    return Huge(2,n) * (max(math.log(n,2),1) / n)
def comp_fn_1000_0000(n):
    return Huge(2,n)
def comp_fn_1010_0000(n):
    return Huge(2,n) * n
def comp_fn_1020_0000(n):
    return Huge(2,n) * n**2
def comp_fn_1045_0000(n):
    return Huge(2,n) * n**POLY_EXP
def comp_fn_1099_0000(n):
    return Huge(2,n+EPS)
def comp_fn_1515_0000(n):
    return Huge(2,1.5*n) * n**1.5
def comp_fn_1984_0000(n):
    return Huge(2,2*n) / n**1.5
def comp_fn_2000_0000(n):
    return Huge(2,2*n)
def comp_fn_2020_0000(n):
    return Huge(2,2*n) * n**2
def comp_fn_2021_0000(n):
    return Huge(2,2*n) * (n**2 * max(math.log(n,2),1))
def comp_fn_2070_5000(n):
    return Huge(2,n*(2+EPS)) / n**3
def comp_fn_2090_5000(n):
    return Huge(2,n*(2+EPS)) / n
def comp_fn_2091_5000(n):
    return Huge(2,int(n*(2+EPS))) * (max(math.log(n,2),1) / n)
def comp_fn_3011_0000(n):
    return Huge(2,int(3*n)) * (n * max(math.log(n,2),1))
def comp_fn_6000_5000(n):
    return Huge(2,n*(6+EPS))
def comp_fn_7091_5000(n):
    return Huge(2,n*(7+EPS)) * (max(math.log(n,2),1) / n)
def comp_fn_8000_0000(n):
    return Huge(max(math.log(max(math.log(n,2),1),2),1) , n)
def comp_fn_8001_0000(n):
    huge_obj_1 = Huge(max(math.log(max(math.log(n,2),1),2),1) , n-1)
    return huge_obj_1 * max(math.log(n,2),1)
def comp_fn_8010_0000(n):
    huge_obj_1 = Huge(max(math.log(max(math.log(n,2),1),2),1) , n)
    return huge_obj_1 * n
def comp_fn_8011_0000(n):
    huge_obj_1 = Huge(max(math.log(max(math.log(n,2),1),2),1),int(n-1))
    return huge_obj_1 * (n * max(math.log(n,2),1))


def comp_fn_9000_0000(n):
    return stirling(n)
def comp_fn_9001_0000(n):
    return n*stirling(n)
def comp_fn_9122_0000(n):
    return Huge(2,n) * Huge(n,2*n+2)
def comp_fn_9200_0000(n):
    return Huge(2,2*n**2)
def comp_fn_9305_0000(n):
    return Huge(2,math.log(5,2)*n**3)



