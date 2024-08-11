import string, time
from random import randint

#anzahl = int(input('Wieviele Passwörter sollen generiert werden?: '))

def generate_pw(pw_length=8):
    char_list = list(string.ascii_letters + string.digits + string.punctuation)
    pw = ''

    for i in range(0,pw_length):
        number = randint(0,len(char_list)-1)
        pw += char_list[number]
    return pw

#write_file = input('Passwörter in Datei speichern? (Y/N): ')
#if write_file == 'Y':
#    timestr = time.strftime("%y-%m-%d_%H%M%S")
#    file_path = 'PW_generator/ausgabe_PW_' + str(timestr) + '.txt'
#    file_save = open(file_path,'w')
#    for key, pw in pw_liste.items():
#        file_save.write('{}: {}\n'.format(key, pw))
#    file_save.close()

if __name__ == "__main__":
    pw_length = int(input('How long should the password be (in characters)?: '))
    print(generate_pw(pw_length))
    