# -*- coding: utf-8 -*-
# @Time    : 2022/6/7 21:54

from bs4 import BeautifulSoup

import os
import random
import csv
import requests

cookies = {
    '_pk_id.10.1f5c': 'f1e12d9aa6c98936.1654600007.',
    'ASP.NET_SessionId': 'oel2zntx1rfibhn2vk202uai',
    '_pk_ref.10.1f5c': '%5B%22%22%2C%22%22%2C1654649121%2C%22https%3A%2F%2Flink.csdn.net%2F%3Ftarget%3Dhttps%3A%2F%2Fcn.etherscan.com%2F%22%5D',
    '_pk_ses.10.1f5c': '1',
    '__cf_bm': 'jvhJr891EojPRXCC7RsZSi5L64y1s.NI4wCITLdLNgw-1654649218-0-ATqrYTgLbjhlA3wukuTqsOtazGiltFGGWH2lm0QEhK2gMKKrwek37qIn9038Hr2wYJ4cx6lIHWHgxGMls4jZUe6V1EWu07vUzterTaGVzRL9VMyhml6TfXVijhj3IiCYhA==',
}

headers = {
    'authority': 'cn.etherscan.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_pk_id.10.1f5c=f1e12d9aa6c98936.1654600007.; ASP.NET_SessionId=oel2zntx1rfibhn2vk202uai; _pk_ref.10.1f5c=%5B%22%22%2C%22%22%2C1654649121%2C%22https%3A%2F%2Flink.csdn.net%2F%3Ftarget%3Dhttps%3A%2F%2Fcn.etherscan.com%2F%22%5D; _pk_ses.10.1f5c=1; __cf_bm=jvhJr891EojPRXCC7RsZSi5L64y1s.NI4wCITLdLNgw-1654649218-0-ATqrYTgLbjhlA3wukuTqsOtazGiltFGGWH2lm0QEhK2gMKKrwek37qIn9038Hr2wYJ4cx6lIHWHgxGMls4jZUe6V1EWu07vUzterTaGVzRL9VMyhml6TfXVijhj3IiCYhA==',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33',
}

pause = random.random() * 10


def getTransaction(filepath):
    list_ = []
    for root, dirs, files in os.walk(filepath):
        for filename in files:
            fileList = []
            filename_ = filename.split('_')[0]
            fileList.append(filename_)
            url = 'https://cn.etherscan.com/address/' + str(filename_)
            response = requests.get(url=url, cookies=cookies, headers=headers,timeout=5000)
            response.close()
            response.encoding='utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            #Crawling content
            content="#transactions > div.d-md-flex.align-items-center.mb-3 > p"
            #ContentPlaceHolder1_topPageDiv > p > span.d-flex.align-items-center
            a=soup.select(content)
            for i in range(0,len(a)):
                a[i] = a[i].text
                fileList.append(str(a[i]).strip())
                # fo.write(a[i]+'\n')
            list_.append(fileList)
    return list_

# output_filepath:  xxx.csv
def getRes(input_filepath,output_filepath):
    fo = open(output_filepath,'a',encoding="utf-8")
    writer = csv.writer(fo)
    res = getTransaction(input_filepath)
    for i in res:
        if len(i) == 2:
            if i[0] == '' or i[1] == ''or i[0] == '\n' or i[1] == '\n':
                continue
            else:
                _list = []
                _list.append(i[0].strip())
                _list.append(i[1].strip().split(" ")[6])
                writer.writerow(_list)
    fo.close()

if __name__ == '__main__':
    filepath = ''
    outputFilepath = '.csv'
    getTransaction(filepath)
    getRes(filepath,outputFilepath)