import  os
import  json
from py2neo import Graph,Node


class pigdiseaseGraph:
    def __init__(self,datapath):
        self.data_path = datapath
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="Neo4j")

    '''读取文件'''

    def read_nodes(self):
        #生猪疾病防治
        diseases = []  # 疾病
        disease_infos = []# 生猪疾病信息
        prevents = [] #预防
        symptoms = [] # 症状
        reasons = [] #原因
        therapies = [] # 治疗措施
        # rels_category = []  # 疾病与类别之间的关系

        #构建节点实体关系
        rels_d_class = []# 疾病-类别关系
        rels_symptom = []# 疾病症状关系
        rels_therapy = []  # 疾病－治疗措施关系
        rels_prevent = []
        rels_reason = []

        count = 0
        for data in open(self.data_path, 'r', encoding='utf-8'):
            disease_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data)
            print(data)
            disease = data_json['name']
            disease_dict['name'] = disease
            diseases.append(disease)
            disease_dict['describe'] = ''
            disease_dict['prevent'] = ''
            disease_dict['reason'] = ''
            disease_dict['symptom'] = ''

            if 'symptom' in data_json:
                symptoms += data_json['symptom']
                for symptom in data_json['symptom']:
                    rels_symptom.append([disease, symptom])

            if 'describe' in data_json:
                disease_dict['describe'] = data_json['describe']
            if 'symptoms' in data_json:
                disease_dict['des_sym'] = data_json['symptoms']
            if 'prevents' in data_json:
                disease_dict['des_pre'] = data_json['prevents']
            if 'therapys' in data_json:
                disease_dict['des_ther'] = data_json['therapys']
            if 'reasons' in data_json:
                disease_dict['des_rea'] = data_json['reasons']

            if 'prevent' in data_json:
                prevents += data_json['prevent']
                for prevent in data_json['prevent']:
                    rels_prevent.append([disease, prevent])

            if 'reason' in data_json:
                reasons += data_json['reason']
                for reason in data_json['reason']:
                    rels_reason.append([disease, reason])
            if 'therapy' in data_json:
                therapies += data_json['therapy']
                for therapy in data_json['therapy']:
                    rels_therapy.append([disease, therapy])
            disease_infos.append(disease_dict)
        return  set(symptoms), set(prevents),set(reasons),set(therapies),set(diseases),disease_infos, \
               rels_symptom,rels_prevent, rels_reason,rels_therapy

    '''建立节点'''

    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱中心疾病的节点'''

    def create_diseases_nodes(self, disease_infos):
        count = 0
        for disease_dict in disease_infos:
            node = Node("Disease", name=disease_dict['name'], describe=disease_dict['describe'],
                        des_prevent=disease_dict['des_pre'], des_reason=disease_dict['des_rea'],
                        des_therapy=disease_dict['des_ther'], des_symptom=disease_dict['des_sym'],)
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema'''

    def create_graphnodes(self):
        Symptoms,Prevents, Reasons,Therapies,Disease,disease_infos, rels_symptom,rels_prevent, rels_reason,rels_therapy = self.read_nodes()
        self.create_diseases_nodes(disease_infos)
        self.create_node('Prevents', Prevents)
        print(len(Prevents))
        self.create_node('Reasons', Reasons)
        print(len(Reasons))
        self.create_node('Therapies', Therapies)
        print(len(Therapies))
        self.create_node('Symptom', Symptoms)
        return

    '''创建实体关系边'''

    def create_graphrels(self):
        Symptoms, Prevents, Reasons, Therapies,Disease, disease_infos, rels_symptom, rels_prevent, rels_reason, rels_therapy = self.read_nodes()
        self.create_relationship('Disease', 'Prevents', rels_prevent, 'prevent_measure', '预防措施')
        self.create_relationship('Disease', 'Reasons', rels_reason, 'dis_reason', '发病原因')
        self.create_relationship('Disease', 'Therapies', rels_therapy, 'threapy_measure', '治疗措施')
        self.create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '症状')

    '''创建实体关联边'''

    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''

    def export_data(self,path):
        Symptoms, Prevents, Reasons, Therapies,Diseases, disease_infos, rels_symptom, rels_prevent, rels_reason, rels_therapy = self.read_nodes()
        f_Prevents = open(path+'Prevents.txt', 'w+',encoding='utf-8')
        f_Reasons = open(path+'Reasons.txt', 'w+',encoding='utf-8')
        f_Therapies = open(path+'Therapies.txt', 'w+',encoding='utf-8')
        f_symptom = open(path+'Symptoms.txt', 'w+',encoding='utf-8')
        f_disease = open(path+'Diseases.txt', 'w+',encoding='utf-8')

        f_Prevents.write('\n'.join(list(Prevents)))
        f_Reasons.write('\n'.join(list(Reasons)))
        f_Therapies.write('\n'.join(list(Therapies)))
        f_symptom.write('\n'.join(list(Symptoms)))
        f_disease.write('\n'.join(list(Diseases)))

        f_Prevents.close()
        f_Reasons.close()
        f_Therapies.close()
        f_symptom.close()
        f_disease.close()

        return


if __name__ == '__main__':
    # for i in range(52):
    #     path = "json/"+str(i)+".json"
        handler = pigdiseaseGraph('./data/pig_disease.json')

        print("step1:导入图谱节点中")
        handler.create_graphnodes()
        print("step2:导入图谱边中")
        handler.create_graphrels()
        handler.export_data('./export/')

