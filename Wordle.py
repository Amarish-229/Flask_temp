import string
import enchant
dictionary = enchant.Dict("en-US")
from itertools import permutations, combinations

alphabet = string.ascii_lowercase
print(alphabet)
exclude = "digthosbav"
contains = "u"
list_contains = 'roe'
first = "c"
second = "l"
third = 'o'
fourth = 'r'
last = "e"
to_combined = [let for let in alphabet if let not in exclude]
print(to_combined)

perms = permutations(to_combined, 4)
# combinations_to_check = ["".join(item) for item in perms if 'o' in item and 'l' in item and item[-1] == 'e']
combinations_to_check = ["".join(perm) + last for perm in perms if 'r' in perm and perm[2] != 'r' and perm[1] != 'r']
# print(combinations_to_check)
# for letter in to_combined:
#         for let in to_combined:
#             str_ = letter + second + third + let + last
#             print(str_)
#             combinations_to_check.append(str_)
# print("The Whole Perms", perms)
# # final_ = ["".join(item) for item in perms if contains in item if dictionary.check("".join(item)) if item[1] != contains]
final_ = [item for item in combinations_to_check if dictionary.check(item)]
# # final_ = [item for item in perms ]
print(final_)



