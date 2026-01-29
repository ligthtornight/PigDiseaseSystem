# -*-coding:utf-8 -*-
import jieba.analyse
import jieba
import os

# 添加专有名词，增加分词力度
df = open("./raw_data/disease.txt",'r+',encoding='utf-8')
text1 = df.readlines()
df.close()
for i in range(len(text1)):
    disease_text = text1[i]
    disease_text = disease_text[:-1]
    #print(disease_text)
    jieba.suggest_freq(disease_text,tune=True)

raw_data_path = './raw_data/'
cut_data_path = './cut/'
stop_word_path = 'cut/cn_stopwords.txt'


def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'rb').readlines()]
    return stopwords


def cut_word(raw_data_path, cut_data_path):
    data_file_list = os.listdir(raw_data_path)
    corpus = ''
    temp = 0

    stop = open(stop_word_path,'r+',encoding='utf-8')
    #stopwords = stopwordslist(stop_word_path)  # 这里加载停用词的路径
    text2 =stop.read()
    stopwords = text2.splitlines()
    #print(type(stopwords))

    for file in data_file_list:
        with open( raw_data_path+file, 'rb') as f: #raw_data_path + file
            print(temp + 1)
            temp += 1
            document = f.read()
            document_cut = jieba.cut(document, cut_all=False)
            # print('/'.join(document_cut))
            result = '\n'.join(document_cut)
            #corpus += result
            print(result)
        with open(cut_data_path + 'cut_'+file, 'w', encoding='utf-8') as f:
            f.write(result)  # 读取的方式和写入的方式要一致
            f.close()
        with open(cut_data_path + 'cut_'+file, 'r+', encoding='utf-8') as f:# 读取转移后的文本
            document_cut = f.read()
            outstr = ''
            for word in document_cut:
                if word not in stopwords:
                    if word != '\t':
                            outstr += word
                            #outstr += ""
        with open(cut_data_path + 'key_'+file, 'w', encoding='utf-8') as tf:
            tf.write(outstr)  # 读取的方式和写入的方式要一致
            tf.close()
            f.close()


if __name__ == "__main__":
    cut_word(raw_data_path, cut_data_path)
