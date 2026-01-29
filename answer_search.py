#!/usr/bin/env python3
# coding: utf-8

from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="Neo4j")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_reason':
            desc = [i['m.des_reason'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            desc = [i['m.des_prevent'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'disease_therapy':
            desc = [i['m.des_therapy'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可以尝试如下治疗：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'disease_desc':
            desc = [i['m.descibe'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0},熟悉一下：{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_check':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'check_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()