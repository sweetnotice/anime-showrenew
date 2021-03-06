import re
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import os


def get_anime():
    anime = []
    with open('./anime.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line != '\n':
                anime.append(line.replace('\n', '').split('?')[1])
    return anime


def main(url):
    resp = requests.get(url).text
    # print(resp)
    states = obj_state.finditer(resp)
    re_finds = obj_find_name_link.finditer(resp)
    for re_find, state in zip(re_finds, states):
        state = state.group('state')
        if state.find('已完结') == -1:  # 过滤已完结的
            global count
            name = re_find.group('name')
            link = 'https://www.ysjdm.net/index.php/vod/detail/id/' + re_find.group('link') + '.html'
            if link not in have_anime:
                show = name + '?' + link
                count += 1
                print(show + f'\n{state}\n')
    print(f'\n{count}部')


if __name__ == '__main__':
    obj_find_name_link = re.compile(r'<a title="(?P<name>.*?)" href="/index.php/vod/detail/id/(?P<link>.*?).html">')
    obj_state = re.compile(r'<span class="vodlist_sub">状态：(?P<state>.*?)</span></p>')  # 查找番剧当前状态  即是否完结
    url = 'https://www.ysjdm.net/index.php/map/index.html'
    count = 0
    have_anime = get_anime()
    main(url)
    i = input()
