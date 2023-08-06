
# from https://pypi.org/project/TinyMath/#modal-close

from math import sqrt

class Basicmath:

    def add(self, a, b):
        return a+b

    def sub(self, a, b):
        return a-b
        
    def isPrime(self, num):
        if num<=1:
            return False
        for i in range(2,int(sqrt(num))+1):
            if num%i==0:
                return False
        return True