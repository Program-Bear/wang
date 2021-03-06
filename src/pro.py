import sys
import random
import argparse
import time
#from tqdm import tqdm


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
            if (((line[i] in now_value) or (line[i] in ans)) and (i in l)):
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
        now_wrong += shuffle(bank[now_line], False, ans, now_wrong)
    now_wrong = now_wrong[0:wrong_num]

    return shuffle(now_ans+now_wrong, True, None, None)

def gen_output(width, height, value):
    output = ''
    assert(len(value) == width * height)
    count = 0
    for i in range(0, height):
        for j in range(0, width):
            output += value[count] + "  "
            count += 1
        output += '\n'
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--BankPath",  default='../Bank/bank.txt',help='题库路径')
    parser.add_argument("--AnswerPick",default='../Bank/answer_pick.txt',help='题目选择路径')
    parser.add_argument("--OutputPath",default='../Problem/wang.txt',help='宫格输出路径')
    parser.add_argument("--AnsPath",   default='../Problem/ans.txt',help='答案输出路径')
    parser.add_argument('-W','--width',type=int, default=4, help = "宫格的长，默认长度为4")
    parser.add_argument('-H','--height',type=int, default=4, help = "宫格的宽，默认宽度为4")
    parser.add_argument('--display',help = "进入展示模式", action='store_true')
    parser.add_argument('--debug', help='输出调试信息',action='store_true')
    parser.add_argument('-L','--limit',type=float,default=10, help="设置答题时长")
    args = parser.parse_args()
    bank_path = args.BankPath
    output_path = args.OutputPath
    ans_path = args.AnsPath
    pick_path = args.AnswerPick
    width = args.width
    height = args.height
    TOTAL = width * height
    DEBUG = args.debug
    limit = args.limit
    if (width < height):
        print("长小于宽？小学数学是体育老师教的？帮你交换了")
        temp = width
        width = height
        height = temp

    bank_object = open(bank_path,'r')
    bank = bank_object.readlines()
    for i in range(0, len(bank)):
        bank[i] = bank[i].strip()
    bank_object.close()
    
    pick_object = open(pick_path,'r')
    pick = pick_object.readlines()
    pick_object.close()
    pick_ans = []
    for i in pick:
        num = 0
        try:
            num = int(i.strip())
        except:
            print("pick文件不合法")
        pick_ans.append(num)
    random.shuffle(pick_ans)

    if (args.display):
        print("进入答题模式，每题时间限制%d秒，输入n下一道，输入e退出"%limit)
        count = 0
        tot = 0
        tot_time = 0
        for i in pick_ans:
            answer = bank[i]
            if (len(answer) == 0):
                continue 
            value = gen_wrong(answer, bank)
            problem = gen_output(width, height, value)
            print(problem, end='')
            fin = False
            start = time.time()
            while(1):
                temp = input()
                if (temp == 'n'):
                    break
                if (temp == 'e'):
                    fin = True
                    break
            if (fin):
                break
            print("正确答案为：%s"%answer)
            count += 1
            spend = (time.time() - start)
            if (spend > limit):
                tot += 1
            tot_time += spend
            print("用时: " + str(spend) + '秒\n')
        print("答题结束")
        print("你一共答了%d题，其中有%d题用时超过了时间限制"%(count,tot))
        print("平均用时:%s秒, 超时比例:%s"%(str(float(tot_time)/count), str(float(tot)/count)))
    else:
        print("生成%dx%d的众里寻他"%(width, height))
        wang = open(output_path, 'w')
        ans = open(ans_path,'w')

        for i in pick_ans:
            answer = bank[i]
            if (len(answer) == 0):
                continue
            if (DEBUG):
                print("生成%s"%answer)
            value = gen_wrong(answer, bank)
            if (DEBUG):
                print(value)
            problem = gen_output(width, height, value)
            
            wang.write(problem + "\n")
            ans.write(answer + "\n")
            if (DEBUG):
                print("\n")
        wang.close()
        ans.close()
