import random
read_object = open("bank.txt",'r')
lines = read_object.readlines()
read_object.close()

write_object = open("new_bank.txt",'w')
for i in lines:
    if(random.randint(0,1) == 1):
        write_object.write(i)
write_object.close()