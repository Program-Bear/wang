import sys
import random
import argparse
import time
from tqdm import tqdm


TOTAL = 16 # default is 4x4
DEBUG = False

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
        if (DEBUG):
            print("生成干扰项：%s"%line)
        target = random.randint(0, length - 1)
        if (line == ans):
            return []
        while(line[target] in ans):
            target = random.randint(0, length - 1)
        l.remove(target)
        if (DEBUG):
            print("删掉了%s"%line[target])

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
    
    used_wrong = []
    while(len(now_wrong) < wrong_num):
        now_line = random.randint(0, len(bank) - 1)
        while(now_line in used_wrong):
            now_line = random.randint(0, len(bank) - 1)
            
        used_wrong.append(now_line)    
        if (ans == bank[now_line]):
            continue
        #print(now_wrong)
        #print(shuffle(bank[now_line], False, ans, now_wrong))
        now_wrong += shuffle(bank[now_line], False, ans, now_wrong)
    now_wrong = now_wrong[0:wrong_num]

    return shuffle(now_ans+now_wrong, True, None, None)

def gen_output(width, height, value):
    output = ''
    assert(len(value) == width * height)

    for i in range(0, height):
        for j in range(0, width):
            output += value[i * height + j] + "  "
        output += '\n'
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--BankPath",  default='bank.txt',help='题库路径')
    parser.add_argument("--OutputPath",default='wang.txt',help='宫格输出路径')
    parser.add_argument("--AnsPath",   default='ans.txt',help='答案输出路径')
    parser.add_argument('-W','--width',type=int, default=4, help = "宫格的长，默认长度为4")
    parser.add_argument('-H','--height',type=int, default=4, help = "宫格的宽，默认宽度为4")
    parser.add_argument('--display',help = "进入展示模式", action='store_true')
    parser.add_argument('--debug', help='输出调试信息',action='store_true')

    args = parser.parse_args()
    bank_path = args.BankPath
    output_path = args.OutputPath
    ans_path = args.AnsPath
    width = args.width
    height = args.height
    TOTAL = width * height
    DEBUG = args.debug
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
        print("进入答题模式，输入n下一道，输入e退出")
        for i in pick_ans:
            answer = bank[i]
            value = gen_wrong(answer, bank)
            problem = gen_output(width, height, value)
            print(problem,end='')
            fin = False
            start = time.time()
            while(1):
                temp = input()
                if (temp == 'n'):
                    break
                if (temp == 'e'):
                    fin = True
                    break
            print("正确答案为：%s"%answer)
            spend = (time.time() - start)
            print("用时: " + str(spend) + '秒\n')
            if (fin):
                break
        print("答题结束")
    else:
        print("生成%dx%d的众里寻它"%(width, height))
        wang = open(output_path, 'w')
        ans = open(ans_path,'w')

        for i in pick_ans:
            answer = bank[i]
            if (DEBUG):
                print("开始生成%s"%answer)
            value = gen_wrong(answer, bank)
            problem = gen_output(width, height, value)
            
            wang.write(problem + "\n")
            ans.write(answer + "\n")
            if (DEBUG):
                print("\n")
        wang.close()
        ans.close()