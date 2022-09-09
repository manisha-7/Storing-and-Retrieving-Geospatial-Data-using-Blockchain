import random

def generate():
    num_letters = random.randint(5,9)
    num_symbols = random.randint(2,5)
    num_numb = random.randint(5,7)

    # l_let = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

    l_let = [chr(i) for i in range(65, 91)] + [chr(j) for j in range(97, 123)]

    l_num = [str(i) for i in range(0, 10)]

    l_sym = ['!', '@', '#', '$', '%', '*']

    password = []

    for let in range(num_letters):
        password.append(random.choice(l_let))

    for sym in range(num_symbols):
        password.append(random.choice(l_sym)) 

    for num in range(num_numb):
        password.append(random.choice(l_num))    

    random.shuffle(password)
    str1 = ''
    return str(str1.join(password))