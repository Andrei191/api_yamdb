import random


def random_code(length=16):
    chars = 'AbraCadaBraFjhdLkdfjdkDDKFDJKF'
    code = ''
    for x in range(length):
        code += random.choice(chars)
    return code
