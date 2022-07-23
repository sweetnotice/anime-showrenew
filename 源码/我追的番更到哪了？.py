import re
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import os

head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}


def config():  # 拿到下载器的地址
    path = (os.getcwd() + r'\异世界动漫网下载器.exe')
    # print(path)
    # os.startfile(path)
    return path


def get_today_date():
    today_date = time.strftime('%m-%d')
    return today_date


def get_links():
    with open(file, 'r+', encoding='utf-8') as f:
        links = []
        name = []
        for line in f.readlines():
            if line != '\n':
                name.append(line.split('?')[0])
                links.append(line.split('?')[1].replace('\n', '').replace('.html', '') + '.html')
        return name, links


def finish_anime_name_link():
    if len(finish_anime_urls) != 0:
        show_finish_list = '\n'.join(finish_anime_urls)
        delete = input(f'{show_finish_list}\n\n这 {len(finish_anime_urls)} 部 已完结是否要删除(y or n)')
        if delete == 'y':
            with open(file, 'r', encoding='utf-8') as f, open('./anime1.txt', 'w', encoding='utf-8') as f1:
                for line in f.readlines():
                    if line != '\n':
                        # a = line.split('?')
                        if line.split('?')[1].replace('\n',
                                                      '') not in finish_anime_urls:  # 把每一行和要删的列表进行匹配，如果没匹配到就写入,匹配到就输出
                            f1.write(line)
                        else:
                            show_link = line.replace('?', ' ').replace('.html', '').replace('\n', '') + '.html'
                            print(show_link)
                            copy_link = line.split('?')[1].replace('.html', '').replace('\n', '').replace('detail',
                                                                                                          'play') \
                                        + '/sid/1/nid/1.html'  # 第一集的链接
                            # print(show_link)
                            # time.sleep(0.6)
                            # pyperclip.copy(copy_link)
                            with open('下载队列.txt', 'a+') as f:
                                f.write(f'\n{copy_link}\n')
            os.remove(file)
            os.rename('./anime1.txt', file)
            os.startfile(downloader_path)


def show_anime_list():
    global show_anime_lists
    for i in show_anime_lists:
        print(i)


def write_renew(txt):
    file = './anime_renew.txt'
    today_date = get_today_date()
    with open(file, 'a+', encoding='utf-8') as f:
        f.seek(0, 0)
        lines = f.readlines()
        file_long = len(lines)
        w = open(file, 'w', encoding='utf-8')
        for line in lines:
            if line.replace('\n', '') == today_date:
                break
            else:
                w.write(line)
        w.write(txt)
        w.write('-' * 80 + '\n')
        w.close()
        del_than_max()


def del_than_max():
    with open('anime_renew.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        split = '-' * 80 + '\n'
        cnt = lines.count(split)
        Max = 4
        if cnt > Max:
            with open('anime_renew.txt', 'w+', encoding='utf-8') as ff:
                del_num = cnt - Max  # 应该删掉几行
                j = 0
                for line in lines:
                    if line == split and j < del_num:
                        j += 1
                    elif j >= del_num:
                        ff.write(line)


def show_renew():
    if len(renew) == 0:
        print('今日没有番更新')
    else:
        today_date = get_today_date()
        today_renew = f'{today_date}\n' + '\n'.join(renew) + '\n'
        print(f'今日更新的番为  这 {len(renew)} 部\n' + '\n'.join(renew) + '\n')
        # print(renew)
        write_renew(today_renew)


def get_url_from_map(local_urls):
    global show_anime_lists, cout
    url = 'https://www.ysjdm.net/index.php/map/index.html'
    resp = requests.get(url, headers=head, timeout=3).text
    obj_today_anime = re.compile(
        rf'<li class="ranklist_item">.*?<a title="(?P<title>.*?)".href="(?P<url>.*?)">.*?<p><span class="vodlist_sub">状态：(?P<cnt>.*?)</span></p>',
        re.S)
    obj_data = re.compile('<em>(?P<data>.*?)</em></span>')
    gets = obj_today_anime.finditer(resp)
    datas = obj_data.finditer(resp)
    web_list = []
    for get, data in zip(gets, datas):
        link = 'https://www.ysjdm.net' + get.group('url').replace('.html', '') + '.html'
        title = get.group('title')
        cnt = get.group('cnt')
        data = data.group('data')
        if link in local_urls:
            web_list.append(link)
            show_anime_lists.append(f'{link}\t\t{title}\n{cnt}/{data}')
            cout += 1
            if cnt.find('已完结') != -1:
                finish_anime_urls.append(link)  # 加入列表的是网站里的链接
            if data == today_date:
                renew.append(f'{cnt}\t{title}')
    other_need_asks = set(local_urls) - set(web_list)
    return other_need_asks


def get_all_And_add_finish(url, name_d):
    global cout
    try:
        resp = requests.get(url, timeout=3).text
        count = obj_find_count_date.search(resp).group('count')  # 集数
        date = obj_find_count_date.search(resp).group('date')  # 更新日期
        name = obj_find_name.search(resp).group('name').strip()  # 番名
        if count.find('已完结') != -1:
            finish_anime_urls.append(url)  # 加入列表的是本地文件里的网页链接
        if date == today_date:  # 检测今日更新
            renew.append(f'{count}\t{name}')
        show_anime_lists.append(f'{url}\t\t{name.ljust(name_d)}\n{count}/{date}')  # 先把之后要打印的加入待打印列表  地址 名字  \n集数/更新日期
        cout += 1
        # print(cout)
    except requests.exceptions.RequestException:
        return


def main():
    global cout, renew, finish_anime_urls, show_anime_lists
    get_link = get_links()
    names, links = get_link[0], get_link[1]  # 从本地anime获取番剧名字，链接
    name_d = max(map(len, names))
    # link_d = max(map(len, links))

    count_retry = 1
    while 1:
        try:
            cout, renew, finish_anime_urls, show_anime_lists = 0, [], [], []
            start = time.time()
            other_links = get_url_from_map(links)  # 从最近更新页面获取
            with ThreadPoolExecutor(10) as f:
                for link in other_links:
                    f.submit(get_all_And_add_finish, link, name_d)
            if count_retry >= 5:
                print('当前网络情况不太好，请稍后再试')
                return
            if cout != len(names):  # 判断访问的是否和追番列表数量一样
                print(f"-----------第{count_retry}次运行超时-------------\n")
                count_retry += 1
                raise
            break
        except RuntimeError:
            pass
    show_anime_list()
    print(f'\n共 {len(names)} 部\n')
    show_renew()  # 展示renew列表
    finish = time.time()
    print('查询耗时' + str(round((finish - start), 1)) + 's\n')
    finish_anime_name_link()


if __name__ == '__main__':
    file = './anime.txt'
    obj_find_count_date = re.compile(
        r'<li class="data"><span>状态：</span><span class="data_style">(?P<count>.*?)</span>&nbsp;/&nbsp;<em>(?P<date>.*?)</em></li>')
    obj_find_name = re.compile(r'<h2 class="title">(?P<name>.*?)</h2>', re.S)
    downloader_path = config()
    show_anime_lists = []
    finish_anime_urls = []
    renew = []
    cout = 0
    today_date = get_today_date()

    main()
    for i in range(91):
        print(f'程序运行完毕将在 {90 - i} 秒后自动关闭', end='')
        time.sleep(1)
        print('\r', end='', flush=True)
