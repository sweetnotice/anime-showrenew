import re
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import os
import datetime
from goto import with_goto
import pyperclip

def get_today_date():
    today_date = time.strftime('%m-%d')
    return today_date

def get_links():
    with open(file, 'r+', encoding='utf-8') as f:
        links = []
        name = []
        for line in f.readlines():
            name.append(line.split('?')[0])
            links.append(line.split('?')[1].replace('\n', '').replace('.html', '') + '.html')
        return name, links


def finish_anime_name_link():
    if len(finish_names) != 0:
        show_finish_list = str(finish_names).replace("['", '').replace("']", '').replace("'", '').replace(',', '\n')
        delete = input(f'{show_finish_list}\n\n这 {len(finish_names)} 部 已完结是否要删除(y or n)')
        if delete == 'y':
            with open(file, 'r', encoding='utf-8') as f, open('./anime1.txt', 'w', encoding='utf-8') as f1:
                for line in f.readlines():
                    if line.split('?')[0] not in finish_names:  # 把每一行和要删的列表进行匹配，如果没匹配到就写入,匹配到就输出
                        f1.write(line)
                    else:
                        show_link = line.replace('?', ' ').replace('.html', '').replace('\n', '').replace('detail', 'play') + \
                        '/sid/1/nid/1.html'
                        print(show_link)  # 直接把输出的链接变成第一集的链接
                        show_link = line.split('?')[1].replace('.html', '').replace('\n', '').replace('detail', 'play') + \
                        '/sid/1/nid/1.html'
                        # print(show_link)
                        time.sleep(0.6)
                        pyperclip.copy(show_link)
            os.startfile('C:/Users/sweetnotice/PycharmProjects/pythonProject1/代码/爬/dist/异世界的最终形态(大概).exe')
            os.remove(file)
            os.rename('./anime1.txt', file)


def show_renew():
    if len(renew) == 0:
        print('今日没有番更新')
    else:
        print(f'今日更新的番为  这 {len(renew)} 部\n' + \
              str(renew).replace("[", '').replace("]", '').replace(" '", '').replace("'", '').replace(",", '\n') + '\n')
        # print(renew)


def print_all_And_add_finish(url, filename,name_d):
    global choose, cout
    today_date = get_today_date()
    try:
        resp = requests.get(url, timeout=3).text
        count = obj_find_count_date.search(resp).group('count')  # 集数
        date = obj_find_count_date.search(resp).group('date')  # 更新日期
        name = obj_find_name.search(resp).group('name').strip()  # 番名
        if count.find('已完结') != -1:
            finish_names.append(filename)  # 加入列表的是本地文件里的名字
        if date == today_date:  # 检测今日更新
            renew.append(f'{count}  {name}')
        # if len(name) < name_d//4:
        #     name = name + ' '*len(name)
        print(f'{url}  {count}/{date}     {name.center(name_d)}\n', end='')  # 地址 集数/更新日期  名字
        cout += 1
        # print(cout)
    except requests.exceptions.RequestException:
        return


@with_goto
def main():
    global cout, renew, finish_names
    get_link = get_links()
    names,links = get_link[0],get_link[1]
    name_d = max(map(len, names))
    # link_d = max(map(len, links))

    label.begin
    cout, renew, finish_names = 0, [], []

    start = time.time()
    with ThreadPoolExecutor(50) as f:
        for name, link in zip(names, links):
            f.submit(print_all_And_add_finish, link, name,name_d)
    if cout != len(names):  # 判断访问的是否和追番列表数量一样
        print("-----------运行超时-------------\n" * 4)
        goto.begin

    print(f'共 {len(names)} 部\n')
    show_renew()  # 展示renew列表
    finish = time.time()
    print('查询耗时' + str(round((finish - start), 1)) + 's\n')


if __name__ == '__main__':
    file = './anime.txt'
    obj_find_count_date = re.compile(
        r'<li class="data"><span>状态：</span><span class="data_style">(?P<count>.*?)</span>&nbsp;/&nbsp;<em>(?P<date>.*?)</em></li>')
    obj_find_name = re.compile(r'<h2 class="title">(?P<name>.*?)</h2>', re.S)

    finish_names = []
    renew = []
    cout = 0

    main()
    finish_anime_name_link()
    i = input('')
