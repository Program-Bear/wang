import sys
import random
if __name__ == "__main__":
    read_object = open("tot_bank.txt",'r')
    lines = read_object.readlines()
    read_object.close()

    num = int(sys.argv[1])
    pick = []
    while(len(pick) < num):
        now = random.randint(0, len(lines)-1)
        while(now in pick):
            now = random.randint(0, len(lines)-1)
        pick.append(now)
    random.shuffle(pick)

    write_object = open("bank.txt",'w')
    for i in pick:
        write_object.write(lines[i])
    write_object.close()
    