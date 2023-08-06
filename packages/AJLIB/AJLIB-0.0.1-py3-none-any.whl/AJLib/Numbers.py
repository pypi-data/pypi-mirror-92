# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 16:00:00 2021

@author: AsheeshJanda
"""

class Numbers:
    def isPrime(self,num):
        is_Prime = True
        if(num<=1):
            return False
        elif(num==2):
            return True
        else:
            for i in int(num/2):
                if(i!=1):
                    if(num%i==0):
                        is_Prime=False
                        break
    return(is_Prime)
                
    def isArmstrong(self,num):
        res,n = 0,num
        while(num>0):
            rem = num%10
            res = res + (rem*rem*rem)
            num = num //10
        return(n==res)
        