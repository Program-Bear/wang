import sys
import random

def same_num(str1, str2):
    count = 0
    for i in str1:
        if (i in str2):
            count += 1
    return count

if __name__ == "__main__":
    print(same_num(sys.argv[1], sys.argv[2]))