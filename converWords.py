import sys
import string

filename = sys.argv[1]

with open(filename, "r") as f:
    for word in f.read().split():
        if "-" not in word and not string.digits in word and 2 < len(word) < 16:
            print(word.upper())
