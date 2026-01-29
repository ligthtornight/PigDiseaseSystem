#!/usr/bin/env python3
# coding: utf-8


class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'disease_symptom':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_reason':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_prevent':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))


            elif question_type == 'disease_therapy':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))

            elif question_type == 'disease_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))


            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []

        # 查询疾病有哪些症状
        if question_type == 'disease_symptom':
            sql = [ "MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病的原因
        elif question_type == 'disease_reason':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.des_reason".format(i) for i in entities]

        # 查询疾病的防御措施
        elif question_type == 'disease_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.des_prevent".format(i) for i in entities]

        # 查询疾病的治疗方式
        elif question_type == 'disease_therapy':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.des_therapy".format(i) for i in entities]

        # 查询疾病的相关介绍
        elif question_type == 'disease_desc' :
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.descibe".format(i) for i in entities]

        # 查询症状会导致哪些疾病
        elif question_type == 'disease':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'symptom_disease':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        return sql



if __name__ == '__main__':
    handler = QuestionPaser()
