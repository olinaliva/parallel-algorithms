# class for handling very large numbers that need division
# no negative numbers
# basically just representing numbers as a base and exponent

import decimal
import math
import numbers

ERR = 0 #8 # 0.01
class Huge:

    def __init__(self, base, exp):
        assert isinstance(base,numbers.Real)
        assert isinstance(exp,numbers.Real)
        assert base > 0
        self.base = base
        self.exponent = exp

    def __eq__(self,other):
        if type(other) == Huge:
            return self.base == other.base and self.exponent == other.exponent
        elif other < 0:
            return False
        elif other == 0:
            return self.base == 0
        else:
            return abs(self.exponent - log(other,self.base)) <= ERR
        
    def __lt__(self,other):
        if type(other) == Huge:
            other_exp_with_self_base = other.exponent * log(other.base,self.base)   
        elif other <= 0:
            return False 
        else:
            other_exp_with_self_base = log(other,self.base)
        return self.exponent < other_exp_with_self_base
    
    def __gt__(self,other):
        if type(other) == Huge:
            other_exp_with_self_base = other.exponent * log(other.base,self.base)
        elif other < 0:
            return True 
        elif other == 0:
            return self.base > 0
        else:
            other_exp_with_self_base = log(other,self.base)
        return self.exponent > other_exp_with_self_base
    
    def __ge__(self,other):
        return self > other or self == other
    
    def __le__(self,other):
        return self < other or self == other
    
    def __str__(self):
        return str(self.base)+"^"+str(self.exponent)

    def __mul__(self,num):
        if type(num) == Huge:
            rebased_num = num.rebase(self.base)
            return Huge(self.base, self.exponent + rebased_num.exponent)
        elif isinstance(num,numbers.Real):
            return Huge(self.base, self.exponent + log(num,self.base))
        else:
            raise TypeError("Can only multiply a Huge object with a number, not with "+type(num))
        
    def __rmul__(self,num):
        return self * num
        
    def __truediv__(self,num):
        if isinstance(num,numbers.Real):
            return self * (1/num)
        elif type(num) == Huge:
            return self * Huge(num.base,-num.exponent)
        
    def __rtruediv__(self,num):
        return num * Huge(self.base,-self.exponent)
    
    def __sub__(self, other):
        """ self - other """  
        if self < other:
            raise ValueError("Can't substract from smaller value, no negative Huge numbers allowed")
        elif self == other:
            return 0
        ratio = float(Huge(self.base,-self.exponent) * other)
        assert ratio < 1
        return self * (1 - ratio)

    def __rsub__(self, other):
        """ other - self """
        if self > other:
            raise ValueError("Can't substract from smaller value, no negative Huge numbers allowed")
        elif self == other:
            return 0
        ratio = float(Huge(self.base,-self.exponent) * other)
        assert ratio > 1
        return other if ratio==math.inf else self * (ratio - 1)
    
    def __add__(self,num):
        if num < 0:
            return self - num
        elif num == 0:
            return self
        ratio = float(Huge(self.base,-self.exponent) * num)
        return num if ratio==math.inf else self * (ratio + 1)
    
    def __radd__(self,num):
        return self + num

    def __float__(self):
        return float(self.evaluate())
    
    def __int__(self):
        return int(self.evaluate())
    
    def __pow__(self,new_exp):
        return Huge(self.base,self.exponent*new_exp)
    
    def __round__(num):
        # print("using round!")
        if type(num) == Huge:
            return num
        else:
            return round(num)

    def get_base(self):
        return self.base
    
    def get_exponent(self):
        return self.exponent

    def rebase(self,new_base):
        new_exp = self.exponent * log(self.base,new_base)
        return Huge(new_base,new_exp)

    def evaluate(self):
        try:
            return self.base**self.exponent
        except OverflowError:
            try:
                return int(self.base)**int(self.exponent)
            except:
                return decimal.Decimal(self.base)**decimal.Decimal(self.exponent)

    def log(self,base=math.e):
        rebased_self = self.rebase(base)
        return rebased_self.exponent
    


def log(n,b=math.e):
    # print("type of n is "+str(type(n)))
    # print("type of b is "+str(type(b)))
    if type(b) == Huge:
        return log(n,b.base) / b.exponent
    elif type(b) == decimal.Decimal:
        log(n,10)/float(b.log10())
    elif isinstance(n,numbers.Real):
        return math.log(n,b)
    elif type(n)==decimal.Decimal:
        return float(n.log10())/math.log(b,10)
    elif type(n)==Huge:
        return n.log(b)
    else:
        raise TypeError("n is neither a number not a decimal nor huge")