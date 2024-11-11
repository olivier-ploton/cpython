"""
Some demos with 0-based and 1-based indicies, and closed slices.
"""

def PRINT(*args, **kwargs):
    hrule = '-' * 60
    print()
    print(hrule)
    print(*args, **kwargs)
    print(hrule)
    print()

########################################

PRINT("The a{i} notation work on every indexable object")

# Outside of a Computer Science context, items are often numbered starting from 1
a = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th"]

print(f"{a = }")
print()

print(f"{a[0] = }")
print(f"{a[1] = }")
print(f"{a[2] = }")
print()

print(f"{a{1} = }")
print(f"{a{2} = }")
print(f"{a{3} = }")
print()

print(f"{a[-1] = }")
print(f"{a[-2] = }")
print(f"{a[-3] = }")
print()

print(f"{a{-0} = }")
print(f"{a{-1} = }")
print(f"{a{-2} = }")
print()

PRINT("Slices, semi-open and closed")

print(f"{a[0::2] = }")
print(f"{a[1::2] = }")
print()

print(f"{a{1::2} = }")
print(f"{a{2::2} = }")
print()

print(f"{a[0:7:2] = }")
print(f"{a{1:8:2} = }")
print(f"{a{1:7::2}= }")
print()

print(f"{a[1:8:2] = }")
print(f"{a{2:9:2} = }")
print(f"{a{2:8::2}= }")
print()

print("From 4th to 8th element, inclusive")
print(f"{a[3:8]   = }")
print(f"{a{4:8::} = }")
print()

########################################

PRINT("Some swapping")

print(f"{a =}")

print("Let us swap the 4-th and the 8-th element:")
a[3], a[7] = a[7], a[3]
print(f"{a =}")

print("Let us swap the 4-th and the 8-th element, again:")
a{4}, a{8} = a{8}, a{4}
print(f"{a =}")
print()

print("Let us swap and reverse the 3 first and last elements:")
for i in range(3):
    a[i], a[-i-1] = a[-i-1], a[i]
print(f"{a =}")

print("Let us swap and reverse the 3 first and last elements, again:")
for i in range(3):
    a[i], a{-i} = a{-i}, a[i]
print(f"{a =}")

########################################

PRINT("Mixing 0-based and 1-based indices")

class Reveal:
    def __getitem__(self, arg):
        return arg

reveal = Reveal()

print("Indices for the 4th line and 8th column of a 2D array")
print(f"{reveal[3, 7]  = }")
print(f"{reveal{4, 8}  = }")
print(f"{reveal[3].{8} = }")
print(f"{reveal{4}.[7] = }")

########################################

# This part shows details of the proof-of-concept implementation:
# parse-time AST expansion of extended indices/slices into standard ones.
# Use only out of curiosity or for debugging.

def printexpansion(*args):
    """
    prints the AST expansion of fragments of code with extended indices
    Each argument is a string containing a fragment of code
    """
    import ast
    for code in args:
        print(code, '--->', end=' ')
        try:
            print(ast.unparse(ast.parse(code)))
        except Exception as e:
            print(e.__class__.__name__)

def testexpansions():
    brackets = [
        "a[i]",
        
        "a[i:j]",
        "a[i:]",
        "a[:j]",
        "a[:]",
        
        "a[i:j:k]",
        "a[i:j:]", # a[i:j]
        "a[i::k]",
        "a[:j:k]",
        "a[i::]", # a[i:]
        "a[:j:]", # a[:j]
        "a[::k]",
        "a[::]", # a[:]

        "a[i:j::k]",
        "a[i:j::]",
        "a[:j::k]",
        "a[i:::k]", # closed a[i::k], no effect by default
        "a[i:::]",  # closed a[i:], no effect by default
        "a[:j::]",
        "a[:::]", # closed a[:], no effect by default
    ]
    printexpansion(*brackets)
    print()
    braces = [code.replace("[", "{").replace("]", "}") for code in brackets]
    printexpansion(*braces)
    print()
    printexpansion("a{i, *s, j}", "a[i].{j}")

PRINT("Implemetation detail: AST expansion of extended indices")

print("Uncomment # testexpansions() if you wish to try it")
# testexpansions()

########################################
