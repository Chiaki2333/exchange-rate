#!/usr/bin/python
# -*- coding: gbk -*-
'''
�������У����й��ڵغ��й���ۣ�ʵʱ���ʲ�ѯ�ԱȽű���
Github: https://github.com/Chiaki2333/exchange-rate
version: 1.0
'''

import requests
import re
import json
import math
from requests_html import HTMLSession
import multiprocessing


HKD = "�۱�"
USD = "��Ԫ"
EUR = "ŷԪ"
JPY = "��Ԫ"

# �й�����
def boc():
    boc_url = "https://www.boc.cn/sourcedb/whpj/index.html"
    r = requests.get(boc_url)
    r.encoding = 'utf-8'
    #print(r.encoding)
    #print(r.text)
    jiange1 = '������Զ��Υ��Υ����㽻�׵ķ�����ʾ��</a></div></td>\n\t\t</tr>\n\t</table>\n\t</div>\n</form>\t \n\n</div>\n\n                <table cellpadding="0" align="left" cellspacing="0" width="100%">\n                \t<tr>\n                    \t'
    jiange2 = "\n                    </tr>\n\t\t                 \n            </table></div>\n            </div><!--����-end-->"
    # <th>��������</th><th>�ֻ������</th><th>�ֳ������</th><th>�ֻ�������</th><th>�ֳ�������</th><th>���������</th><th>��������</th><th>����ʱ��</th>
    res = r.text.split(jiange1)[1].split(jiange2)[0].replace("\t","").replace("\n","").replace(" ","").split("</tr><tr>")
    res[0] = res[0].replace("</th>"," ").replace("<th>"," ").split()
    for i in range(1, len(res)):
        res[i] = res[i].replace("</td>"," ").replace("<td>"," ").replace('<tdclass="pjrq">'," ").split()
        if len(res[i]) == 8:
            res[i][6] = res[i][6][:10]
        elif len(res[i]) == 6:
            res[i][4] = res[i][4][:10]
    return(res)
#print(boc())

def print_all(price):
    for i in price:
        print(i, end = "\t")
    print()

def boc_cha(currency):
    price = boc()
    ans = ""
    for i in range(len(price)):
        if price[i][0] == currency:
            ans += ("���й����С�") + "\n"
            ans += ("��������\t�ֻ������\t�ֳ������\t�ֻ�������\t�ֳ�������\t���������\t��������\t����ʱ��") + "\n"
            ans += ("%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t%s" % (price[i][0], price[i][1], price[i][2], price[i][3], price[i][4], price[i][5], price[i][6], price[i][7])) + "\n"
            ans += ("-"*50)
            break
    print(ans)
#boc_cha(HKD)

# �������
def bochk():
    bochk_url = "https://www.bochk.com/whk/rates/exchangeRatesHKD/exchangeRatesHKD-input.action?lang=cn"
    r = requests.get(bochk_url)
    r.encoding = 'utf-8'
    jiange1 = '<col span="1" style="width:25%;">\n\t\t\t\t   \t<col span="1" style="width:25%;">\n\t\t\t\t</colgroup>\n\t\t\t\t<tr>\n\t\t\t\t\t<th>'
    jiange2 = '\n\t\t\t\t\t</b></td>\n\t\t\t\t</tr>\n\t\t\t\t<tr>\n\t\t\t\t\t<td>\n\t\t\t\t\t\t\n\t\t\t\t\t\t<!--<link rel="stylesheet" href="/etc.clientlibs/wcm/foundation/clientlibs/accessibility.css" type="text/css">-->'
    res = r.text.split(jiange1)[1].split(jiange2)[0].replace('</tr>\n\t\t\t\t\n\t\t\t</table>\n\t\t\t\n\t\t\t<table class="form_table">\n\t\t\t\t<colgroup>\n\t\t\t\t\t<col span="1" style="width:100%;">\n\t\t\t\t</colgroup>\n\t\t\t\t<tr>\n\t\t\t\t\t<td><b>\n\t\t\t\t\t\t',"").split("\n\t\t\t\t</tr>\n\t\t\t\t\n\t\t\t\t<tr>\n\t\t\t\t\t")
    res[0] = res[0].replace("</th>"," ").replace("<tr>"," ").replace("</tr>"," ").replace("<th>"," ").split()
    for i in range(1, len(res)):
        res[i] = res[i].replace("</td>"," ").replace("<td>"," ").split()
    res[-1], flag = res[-1][0:3], res[-1][-3]+res[-1][-2]+" "+res[-1][-1]
    res.append(flag)
    return res
#print(bochk())

def bochk_cha(currency):
    if currency == "ŷԪ":
        currency = "ŷ��"
    elif currency == "�۱�":
        currency = "�����"
    elif currency == "��Ԫ":
        currency = "��Բ"
    price = bochk()
    flag = 0
    ans = ""
    for i in range(len(price)):
        if currency in price[i][0]:
            if flag == 0:
                ans += ("��������ۡ����۱ң�" + price[-1]) + "\n"
                ans += ("����\t�ͻ�����\t�ͻ�����") + "\n"
            ans += ("%s\t%s\t%s" % (price[i][0], price[i][1], price[i][2])) + "\n"
            flag += 1
            if flag >= 1 and currency != "�����":
                break
            elif flag >= 2:
                break
    ans += ("-"*50)
    print(ans)
#bochk_cha(USD)

# ��ҵ����
def cib():
    cib_url1 = "https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery.do"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    r1 = requests.get(cib_url1, headers = headers)
    r1.encoding = 'utf-8'
    cookie = {}
    for i in r1.cookies:
        cookie[i.name] = i.value
        #print(r1.cookies[i].name)
    #print(cookie)
    cib_url2 = "https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery/list?_search=false&dataSet.nd=&dataSet.rows=80&dataSet.page=1&dataSet.sidx=&dataSet.sord=asc"
    r2 = requests.get(cib_url2, headers = headers, cookies = cookie)
    r2.encoding = 'utf-8'
    return json.loads(r2.text)
#print(cib()['rows'])

def cib_cha(currency):
    price = cib()
    ans = ""
    for i in price['rows']:
        #print(i['cell'][0])
        if i['cell'][0] == currency:
            ans += ("����ҵ���С�") + "\n"
            ans += ("��������	���ҷ���	���ҵ�λ	�ֻ�����۸�	�ֻ������۸�	�ֳ�����۸�	�ֳ������۸�") + "\n"
            ans += ("%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t" % (i['cell'][0], i['cell'][1], i['cell'][2], i['cell'][3], i['cell'][4], i['cell'][5], i['cell'][6])) + "\n"
            ans += ("��������Żݼ�\t")
            ans += ("%s" % i['cell'][1] + "\t\t")
            ans += ("100.00" + "\t\t")
            # �ֻ�����۸� i['cell'][3]
            # �ֻ������۸� i['cell'][4]
            # �ֳ�����۸� i['cell'][5]
            # �ֳ������۸� i['cell'][6]
            zhongjianjia = (float(i['cell'][3]) + float(i['cell'][4])) / 2
            feilv1 = abs(zhongjianjia-float(i['cell'][3]))
            feilv2 = abs(zhongjianjia-float(i['cell'][4]))
            ans += ("%.3f"%(float(i['cell'][3]) + feilv1/2) + "\t\t")
            ans += ("%.3f"%(float(i['cell'][4]) - feilv2/2) + "\n")
            ans += ("-"*50)
            break
    print(ans)
#cib_cha(USD)

# ��������
'''
def fusionbank_cha(currency):
    
    fusionbank_url1 = "https://www.fusionbank.com/remittance.html?lang=sc"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    r1 = requests.get(fusionbank_url1, headers = headers, allow_redirects = True)
    r1.encoding = 'utf-8'
    cookie = {}
    for i in r1.cookies:
        cookie[i.name] = i.value
        #print(r1.cookies[i].name)
    #print(cookie)
    print(r1.text.split("�������ƻ���#")[0])
    
    session = HTMLSession()  # ��ȡʵ����session����
    r = session.get(fusionbank_url1, headers = headers, allow_redirects = True)
    r.html.render()
    get_html = r.html.html  # requests_html�еķ���
    print(get_html)'''
#fusionbank_cha(HKD)

# ������
def hsbchk():
    hsbchk_url = "https://rbwm-api.hsbc.com.hk/digital-pws-tools-investments-eapi-prod-proxy/v1/investments/exchange-rate?locale=zh_CN"
    r = requests.get(hsbchk_url)
    r.encoding = 'utf-8'
    return json.loads(r.text)
#print(hsbchk())

def hsbchk_cha(currency):
    if currency == "ŷԪ":
        currency = "ŷ��"
    elif currency == "�۱�":
        currency = "�����"
    elif currency == "��Ԫ":
        currency = "��Բ"
    price = hsbchk()
    ans = ""
    for i in price['detailRates']:
        if i['ccyName'] == currency:
            ans += ("�������ۡ����۱ң�") + "\n"
            #print("ccy     ccyName lastUpdateDate  ttBuyRt ttSelRt bankBuyRt       bankSellRt")
            ans += ("����\t�����������\t�����������\t�ֳ���������\t�ֳ���������\t������") + "\n"
            ans += ("%s\t%s\t\t%s\t\t%s\t\t%s\t\t%s" % (i['ccyName'], i['ttBuyRt'], i['ttSelRt'], i['bankBuyRt'], i['bankSellRt'], i['lastUpdateDate'])) + "\n"
            ans += ("-"*50)
            break
    print(ans)
#hsbchk_cha(USD)

def bank(currency):
    process1 = multiprocessing.Process(target=bochk_cha(currency))
    process2 = multiprocessing.Process(target=boc_cha(currency))
    process3 = multiprocessing.Process(target=hsbchk_cha(currency))
    process4 = multiprocessing.Process(target=cib_cha(currency))
    
    
    process1.start()
    process2.start()
    process3.start()
    process4.start()

    process1.join()
    process2.join()
    process3.join()
    process4.join()
    
    '''
    bochk_cha(currency)
    hsbchk_cha(currency)
    boc_cha(currency)
    cib_cha(currency)
    '''
    

if __name__ == '__main__':
    while True:
        currency = input("����������Ҫ�鿴���ʵı��֣�֧�֡��۱ҡ���Ԫ��ŷԪ����Ԫ��������Ctrl+C�˳���")
        print("-"*50)
        if currency != "":
            bank(currency)
    #bank(HKD)
    #bank(USD)
    #bank(EUR)
    #bank(JPY)
    