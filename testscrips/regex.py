"""
validate email addresses in Python, using Regular Expressions
Regular Expressions, often shortened as regex, 
- are a sequence of characters used to check whether a pattern exists in a given text (string) or not.
- are, for instance, used at the server side to validate the format of email addresses or passwords during 
registration
"""
#The re module contains classes and methods to represent and work with Regular Expressions in Python
import re

"""The re.compile() method compiles a regex pattern into a regex object
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+’))
but the above codeline not working"""

regex='^[a-z0-9]+[\._]?[\a-z0-9]+[@]\w+[. ]\w{2,3}$'

"""
explaining the above regular expressions: (refer to Unit 4 - class notes)
^ A caret: Matches a pattern at the start of the string
$ Dollar sign. Matches the end of the string.
? Question mark: Checks if the preceding character appears exactly zero or one time. 
And Specifies a non-greedy version of +, *
w Lowercase w: Matches any single letter, digit, or underscore.
\ backslash: If the character following the backslash is a recognized escape character, then the special meaning of the term is taken.
∙ Else the backslash () is treated like any other character and passed through.
∙ It can be used in front of all the metacharacters to remove their special meaning
"""

"""
define a function to validate email
pass the regular expressionand the string into the fullmatch() method
"""
def isValid(email):
    if re.fullmatch(regex, email): 
        print("Valid email") 
    else: 
        print("Invalid email")

# Driver Code
if __name__ == '__main__':

	# Enter the email
	email = "goodmorning1@gmail.com"
	# calling run function
	isValid(email)

	email = "my.email@hotmail-go.org"
	isValid(email)

	email = "goodmorning622022.com"
	isValid(email)



"""
Sources:
GeeksforGeeks (August 8, 2021) "Check if email address valid or not in Python". Available from: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
Gupta, R. (February 7, 2021) "How To Validate An Email Address In Python". Available from: https://www.c-sharpcorner.com/article/how-to-validate-an-email-address-in-python/
Jaiswal, S. (2020) Python Regular Expression Tutorial. Available from: https://www.datacamp.com/community/tutorials/python-regular-expression-tutorial
Peoples, C. (2021), Lecture Notes, Secure Software Development SSDCS_PCOM7E, University of Essex Online, delivered November 2021

"""