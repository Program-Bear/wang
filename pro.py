import sys
import random
import argparse
from tqdm import tqdm


TOTAL = 16 # default is 4x4

def same_num(str1, str2):
    count = 0
    if (str1 == str2):
        return -1
    for i in str1:
        if (i in str2):
            count += 1
    return count

def shuffle(line, is_ans, ans, now_value):
    length = len(line)
    if (length == 0):
        return []
    
    l = [i for i in range(0, length)]

    if (is_ans):
        random.shuffle(l)
    else:
        target = random.randint(0, length - 1)
        if (line == ans):
            return []
        while(line[target] in ans):
            target = random.randint(0, length - 1)
        l.remove(target)

        for i in range(0, length):
            if (line[i] in now_value and (i in l)):
                l.remove(i)
        
        random.shuffle(l)

    value = []
    for i in l:
        value.append(line[i])
    return value

def gen_wrong(ans, bank):
    max_same = 0
    max_line = ''

    now_ans = shuffle(ans, True, None, None)
    #get max line
    for line in bank:
        now_same = same_num(ans,line)
        if (now_same > max_same):
            max_line = line
            max_same = now_same

    now_wrong = shuffle(max_line, False, ans, [])
    wrong_num = TOTAL - len(ans)
    while(len(now_wrong) < wrong_num):
        now_line = random.randint(0, len(bank) - 1)
        #print(now_wrong)
        #print(shuffle(bank[now_line], False, ans, now_wrong))
        now_wrong += shuffle(bank[now_line], False, ans, now_wrong)
    now_wrong = now_wrong[0:wrong_num]

    return shuffle(now_ans+now_wrong, True, None, None)

def gen_output(width, height, value):
    output = ''
    assert(len(value) == width * height)
    assert(width > height)

    for i in range(0, height):
        for j in range(0, width):
            output += value[i * height + j] + "  "
        output += '\n'
    output += '\n'
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--BankPath",  default='bank.txt',help='题库路径')
    parser.add_argument("--OutputPath",default='wang.txt',help='宫格输出路径')
    parser.add_argument("--AnsPath",   default='ans.txt',help='答案输出路径')
    parser.add_argument('-W','--width',type=int, default=4, help = "宫格的长，默认长度为4")
    parser.add_argument('-H','--height',type=int, default=4, help = "宫格的宽，默认宽度为4")
    parser.add_argument('-display',help = "进入展示模式", action='store_true')

    args = parser.parse_args()
    bank_path = args.BankPath
    output_path = args.OutputPath
    ans_path = args.AnsPath
    width = args.width
    height = args.height
    TOTAL = width * height
    
    if (width < height):
        print("长小于宽？小学数学是体育老师教的？帮你交换了")
        temp = width
        width = height
        height = temp

    bank = open(bank_path,'r').readlines()
    for i in range(0, len(bank)):
        bank[i] = bank[i].strip()

    pick_ans = [i for i in range(0, len(bank))]
    random.shuffle(pick_ans)

    if (args.display):
        print("目前还不支持展示功能")
        pass
    else:
        print("开始生成%dx%d的众里寻它"%(width, height))
        wang = open(output_path, 'w')
        ans = open(ans_path,'w')

        for i in tqdm(pick_ans):
            answer = bank[i]
            #print("开始生成%s"%answer)
            value = gen_wrong(answer, bank)
            #print(value)
            problem = gen_output(width, height, value)
            
            wang.write(problem)
            ans.write(answer + "\n")
        
        wang.close()
        ans.close()