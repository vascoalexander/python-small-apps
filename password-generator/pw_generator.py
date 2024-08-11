import string
from random import randint

def generate_pw(pw_length=8):
    """Function to generate a password out of a list of 92 chars. Takes one argument
    specifying the length of the password"""
    char_list = list(string.ascii_letters + string.digits + string.punctuation)
    pw = ''

    for i in range(0,pw_length):
        number = randint(0,len(char_list)-1)
        pw += char_list[number]
    return pw

if __name__ == "__main__":
    pw_length = int(input('How long should the password be (in characters)?: '))
    print(generate_pw(pw_length))
    