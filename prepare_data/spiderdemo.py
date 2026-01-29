import re
import requests
import os
from lxml import etree

def getText(urlpath,headers,op):
    page_text = requests.get(url=urlpath, headers=headers).text
    ttree = etree.HTML(page_text)
    tdata =""
    if op == 0:
     text_list = ttree.xpath('//div[@class="jibingright"]/a/p')
    else:
     text_list = ttree.xpath('//div[@class="jibingright"]/p')
    for text in text_list:
        p_li_text = text.xpath('.//text()')
        if p_li_text !=[]:
            for p_text in p_li_text:
                #print(p_text)
                tdata+=p_text
    #print("overget")
    return tdata
if __name__ == '__main__':

    # if (os.path.exists('./train_data.list')):
    #     os.remove('./train_data.list')
    # if (os.path.exists('./test_data.list')):
    #     os.remove('./test_data.list')
    # if (os.path.exists('./test_path.list')):
    #     os.remove('./test_path.list')
    # if (os.path.exists('./test_label.list')):
    #     os.remove('./test_label.list')
    url= 'https://www.xumuzhuanjia.com/bing'
    native_url = 'https://www.xumuzhuanjia.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'

    }
    count = 0 # 疾病数量
    page_text = requests.get(url=url,headers=headers).text
    # with open ('./zhubing.html','w',encoding='utf-8')as fp:
    #     fp.write(page_text)
    tree = etree.HTML(page_text)
    class_xijun = ''#细菌类
    li_list = tree.xpath('//div[@class="contbox cont boder"]/dl')#id路径
    print(li_list)
    # fp_sym = open('raw_data/symptoms.txt', 'w', encoding='utf-8')#症状描述
    # fp_name = open('raw_data/disease.txt', 'w', encoding='utf-8')#疾病名称
    # fp_apy = open('raw_data/therapy.txt','w',encoding='utf-8')  #治疗
    # fp_pre = open('raw_data/prevent.txt','w',encoding='utf-8') #预防
    # fp_rea = open('raw_data/reason.txt','w',encoding='utf-8')
    fp = open('alldisease.txt', 'w+', encoding='utf-8')
    for li in li_list:
        title_list = li.xpath('./dt/text()')
        title = re.sub(r'[^0-9A-Za-z\u4e00-\u9fa5]',"",title_list[0])
        #print(title)#文本标题
        #fp = open((title + ".txt"), 'w', encoding='utf-8')
        links = li.xpath('.//dd/a')#页面a标签

        for linka in links:
            disease_title = linka.xpath('./text()')# 疾病名称 有可能为空值
            if disease_title != []:
                disease_title = disease_title[0]
                link = linka.xpath('./@href')[0]  # 获取a标签资源
                print(disease_title)
                text = "{\"id\":"+"\""+str(count)+"\","+"\"name\":"+"\""+disease_title+"\","
                # fp_name.write(disease_title+'\n')
                count+=1
                newurl = native_url +link
                new_page_text = requests.get(url=newurl, headers=headers).text
                new_tree = etree.HTML(new_page_text)

                text_list = new_tree.xpath('//div[@class="cont boder"]//div[@class="jibingright"]/a/@href')
                if text_list != []:

                    # 构造所有的症状描述
                    # # 原因
                    chuanbo_url = native_url+text_list[1]
                    # reatext = getText(chuanbo_url,headers,1)+'\n'
                    # fp_rea.write(reatext)


                    # # 症状
                    zhengzhuang_url = native_url+text_list[2]
                    # symtext = getText(zhengzhuang_url, headers, 2) + '\n'
                    # fp_sym.write(symtext)


                    # # 预防
                    yufang_url = native_url+text_list[3]
                    # pretext = getText(yufang_url,headers,3)+'\n'
                    # fp_pre.write(pretext)


                    # # 治疗
                    zhiliao_url = native_url+text_list[4]
                    # apytext = getText(zhiliao_url,headers,4)+'\n'
                    # fp_apy.write(apytext)

                    inbing_url = native_url+text_list[0]  # 综合防治网址
                    text=text+"\"describe\":"+"\""+getText(inbing_url,headers,0)+"\","  # 文本获取
                    text=text+"\"reasons\":"+"\""+getText(chuanbo_url, headers, 1)+"\","
                    text=text+"\"symptoms\":"+"\""+getText(zhengzhuang_url,headers,2)+"\","
                    text=text+"\"prevents\":"+"\""+getText(yufang_url,headers,3)+"\","
                    text=text+"\"therapys\":"+"\""+getText(zhiliao_url,headers,4)+"\"}\n"
                    fp.write(text)
            #  print(text_list)
            # else : print("[]"+link)

            # for atext in text_list:
            #     text=text+atext.xpath('./@title')[0]
            #     text=text+atext.xpath('.//text()')[0]+":\n"
            #fp.write(text)
            #print(text)
    #print(links)

    #获取五个特征文本
    # fp_sym.close()
    # fp_name.close()
    # fp_apy.close()
    # fp_pre.close()
    # fp_rea.close()
    fp.close()
    print('over!!')