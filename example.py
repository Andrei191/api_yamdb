ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)

def max_length_role(array):
    maxi = 0
    for elem in array:
        if len(elem[0]) > maxi:
            maxi = len(elem[0])
    return maxi

print(max_length_role(ROLES))
