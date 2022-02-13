# Python Program for simple OTP genertaor

"""
random is a module in Python that generates random numbers
However, being completely deterministic, it is not suitable for all purposes, 
and is completely unsuitable for cryptographic purposes.

The pseudo-random generators of this module should not be used for security purposes. 
For security or cryptographic uses, see the secrets module

"""
import random as r
# function for otp generation (otpgen)
def otpgen():
    otp=""
    for i in range(6):
        otp+=str(r.randint(1,9))
    print ("Your One Time Password is " + otp)
    
otpgen()

"""
Sources:
https://docs.python.org/3/library/random.html
"""