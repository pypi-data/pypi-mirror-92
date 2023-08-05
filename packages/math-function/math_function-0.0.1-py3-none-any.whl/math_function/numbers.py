from math import sqrt

class Numbers:
    def isPrime(self,num):
        if num<=1:
            return False
        for i in range(2,int(sqrt(num)+1)):
            if num%i==0:
                return False
        return True

        