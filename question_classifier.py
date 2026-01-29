#!/usr/bin/env python3
# coding: utf-8


import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.disease_path = os.path.join(cur_dir, 'dict/Diseases.txt')
        self.prevent_path = os.path.join(cur_dir, 'dict/Prevents.txt')
        self.reason_path = os.path.join(cur_dir, 'dict/Reasons.txt')
        self.therapy_path = os.path.join(cur_dir, 'dict/Therapies.txt')
        self.symptom_path = os.path.join(cur_dir, 'dict/Symptoms.txt')
        # 加载特征词
        self.disease_wds= [i.strip() for i in open(self.disease_path,encoding = 'utf-8') if i.strip()]
        self.prevent_wds= [i.strip() for i in open(self.prevent_path,encoding = 'utf-8') if i.strip()]
        self.reason_wds= [i.strip() for i in open(self.reason_path,encoding = 'utf-8') if i.strip()]
        self.therapy_wds= [i.strip() for i in open(self.therapy_path,encoding = 'utf-8') if i.strip()]
        self.symptom_wds= [i.strip() for i in open(self.symptom_path,encoding = 'utf-8') if i.strip()]
        self.region_words = set(self.disease_wds + self.prevent_wds + self.reason_wds + self.therapy_wds + self.symptom_wds)
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现']
        self.reason_qwds = ['原因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
        self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止','躲避','逃避','避开','免得','逃开','避开','避掉','躲开','躲掉','绕开',
                             '怎样才能不', '怎么才能不', '咋样才能不','咋才能不', '如何才能不',
                             '怎样才不', '怎么才不', '咋样才不','咋才不', '如何才不',
                             '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                             '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        self.therapy_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']
        self.disease_qwds = ['什么病', '啥病', '啥毛病', '什么疾病']

        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}#字典类型
        medical_dict = self.check_medical(question)

        if not medical_dict:
            return {}
        data['args'] = medical_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 症状
        if self.check_words(self.symptom_qwds, question) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)

    
        # 原因
        if self.check_words(self.reason_qwds, question) and ('disease' in types):
            question_type = 'disease_reason'
            question_types.append(question_type)


        #　症状防御
        if self.check_words(self.prevent_qwds, question) and 'disease' in types:
            question_type = 'disease_prevent'
            question_types.append(question_type)

        # 疾病治疗方式
        if self.check_words(self.therapy_qwds, question) and 'disease' in types:
            question_type = 'disease_therapy'
            question_types.append(question_type)

        #依据症状查疾病
        if self.check_words(self.disease_qwds, question) and ('symptom' in types):
            question_type = 'disease'
            question_types.append(question_type)


        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'disease' in types:
            question_types = ['disease_desc']

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'symptom' in types:
            question_types = ['symptom_disease']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        #print(question_types)
        return data
 #'''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        print(type(wd_dict))
        for wd in self.region_words: #for wd in li
            wd_dict[wd] = []

            # print(type(wd)) #wd数组类型
            # print(type(self.region_words))#集合

            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.prevent_wds:
                wd_dict[wd].append('prevent')
            if wd in self.reason_wds:
                wd_dict[wd].append('reason')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
            if wd in self.therapy_wds:
                wd_dict[wd].append('therapy')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)