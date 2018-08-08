import sys
import random
if __name__ == "__main__":
    read_object = open("../Bank/bank.txt",'r')
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

    write_object = open("../Bank/answer_pick.txt",'w')
    for i in pick:
        write_object.write(str(i)+'\n')
    write_object.close()
