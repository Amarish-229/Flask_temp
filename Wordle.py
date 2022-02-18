import string
import enchant
dictionary = enchant.Dict("en-US")
from itertools import permutations, combinations

alphabet = string.ascii_lowercase
print(alphabet)
exclude = "cranjuibvhus"
contains = "u"
second = "o"
last = "e"
to_combined = [let for let in alphabet if let not in exclude]
print(to_combined)

perms = permutations(to_combined, 2)
combinations_to_check = []
for letter in to_combined:
    for perm in perms:
        str_ = letter + second + "".join(perm) + last
        combinations_to_check.append(str_)
# print("The Whole Perms", perms)
# final_ = ["".join(item) for item in perms if contains in item if dictionary.check("".join(item)) if item[1] != contains]
final_ = [item for item in combinations_to_check if dictionary.check(item)]
print(final_)
