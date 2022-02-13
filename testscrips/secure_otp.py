"""
Generate a secure secret code 
Instead of random, use secrets module

"""

import secrets
# Getting systemRandom class instance out of secrets module

username = input("Enter Username: ")

otp = secrets.token_hex(16)
print("Hello " + username + "!" + " Your OTP is " + otp)

password=input("Enter the OTP:")
if password==otp:
    print("OTP is correct.")
else:
    print("OTP is incorrect.")



