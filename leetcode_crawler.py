#A web-crawler to practice request, and prepare leetcode.
#This crawler should read the all questions on leetcode site and recover question number, tile, description and starter code.
#Then use the data crawled, to build a template for each question.
import requests
import json
from bs4 import BeautifulSoup
import os
import re
import sys
import urllib2
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')


def get_alg_content(name):
    url = 'https://leetcode.com/problems/' + name
    try:
         page = requests.get(url)
    except (requests.exceptions.ReadTimeout,requests.exceptions.ConnectTimeout):
            print('time out')
            return 'time out'
    alg_page = BeautifulSoup(page.text, "html.parser")
    alg_contents = alg_page.select('.question-content')
    alg_text = ''
#for some special case(such as subscribe needed),the alg_contents' length will be 0
    if len(alg_contents) > 0:
        contents = alg_contents[0].find_all(['p','pre'])
        for ctt in contents:
            alg_text += ctt.get_text()

    page.close()
    return alg_text


def save_alg(content):
    name = 'lc'+str(content['id'])+'_'+content['title'] +'.py'
    f = open(name,'wb')
    f.write("# -*- coding: utf-8 -*-\n\"\"\"\n")
    f.write(content['content'])
    f.write("@Author Weiming Z \n\"\"\"\n")
    f.close()


if __name__ == "__main__":
    url = "https://leetcode.com/api/problems/algorithms/"
    r = requests.get(url)
    data_json = json.loads(r.text)
    algm_lst = data_json['stat_status_pairs']
    prbm_dict = {}
    if not os.path.exists('leetcode'):
        os.mkdir('leetcode')
    # change directory to leetcode for convinient
    os.chdir('leetcode')

    for a in algm_lst:
        id, title = a['stat']['question_id'], a['stat']['question__title_slug']
        content = get_alg_content(title)
        print('writing ' + str(id) + ' ' + title + '...')
        alg_dict = {'id': id, 'title': title,  'content': content}
        save_alg(alg_dict)
        print('Done!')


