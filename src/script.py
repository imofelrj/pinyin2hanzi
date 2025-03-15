import sys

try:
    a = sys.argv[1]
except IndexError:
    a = 2

print(a) 