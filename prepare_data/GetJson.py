import re

# 打开文件
k_s ='\"symptoms\":'
t_s = '\"symptom\":'
fo = open("../dict/key_symptoms_after.txt", "r+", encoding="utf-8")

# k_s ='\"prevents\":'
# t_s = '\"prevent\":'
# fo = open("./dict/key_prevent_after.txt", "r+", encoding="utf-8")

# k_s = '\"therapys\":'
# t_s = '\"therapy\":'
# fo = open("./dict/key_therapy -after.txt", "r+", encoding="utf-8")

# k_s = '\"reasons\":'
# t_s = '\"reason\":'
# fo = open("./dict/\key_reason(new).txt", "r+", encoding="utf-8")



#print("文件名为: ", fo.name)

f = open("./alldisease1.txt", "r+", encoding="utf-8")  # 返回一个文件对象

list = []
fd =open("./raw_data/disease.txt", "r+", encoding="utf-8")
for i in range(52):
    newfdr = ''
    fdr = fd.readline()
    for j in range(len(fdr)-1):
        newfdr += fdr[j]
    list.append(newfdr)

print(list)
print(len(list))
fd.close()

#list = ['猪大肠杆菌病','猪副嗜血杆菌病','猪链球菌病','猪布鲁氏杆菌病']
#res = 'symptoms:'
cont = ''

def find_(tit):
    nn = 0
    for i in range(len(list)):
        if tit == list[i]:
            nn += 1
    return nn

i = 0
res = ''
n = 0
flag = 0
num = 0
add = 1
for i in range(8000):
    line = fo.readline()
    if (len(line)>1 and line!=' '):
        check = ''
        for j in range(len(line) - 1):
            check += line[j]
        if find_(check)==0:
            j = 0
            if n == 0:
                #print("#######")
                res =res+t_s+'[\"'
                res +=''
                for j in range(len(line) - 1):
                    res += line[j]
                    n = 1
                #print(res)
            else:
                res += '\",\"'
                for j in range(len(line) - 1):
                    res += line[j]
            flag = 1
            #print(res)
            # print("读取的字符串为: %s" % (res))
        else:
            #print(res)
            if flag==1:
                res += '\"]'+","+k_s
                print(res)
                print(add)
                add += 1
                #insert(res, num)
                ff = f.readline()
                ss = ff.find(k_s)
                if ss >= 0:
                    newff = ff.replace(k_s, res)
                    cont += newff
                #else:
                #    cont += ff
                #    ff = f.readline()
                #    newff = ff.replace('symptoms:', res)
                #    cont += newff
                res = ''
                n = 0
print(res)
print(add)
ff = f.readline()
newff = ff.replace(k_s, res)
cont += newff
print(cont)
with open("alldisease2.txt", 'w', encoding="utf-8") as newfile:
    newfile.write(cont)

# 关闭文件
fo.close()
f.close()