import os
import re
from concurrent.futures import ThreadPoolExecutor
import requests
import winsound
import m3u8_downloader

obj_title = re.compile(r'<title>(?P<title>.*?)(SP|第.*?集|PV|OVA|全集|高清).*?</title>', re.S)  #
obj_name = re.compile(r'<title>(?P<name>.*?)</title>', re.S)
obj_link = re.compile(r'","link_pre":.*?,"url":"(?P<link>.*?)","url_next":"', re.S)


def set_t():  # 设定开始集数
    while 1:
        t = input('从第几集开始 (如果是第一集开始直接按回车即可):')
        print('')
        if len(t) == 0:
            t = 1
            break
        else:
            try:
                t = int(t)
                break
            except ValueError:
                print('请确保输入的是数字！！！\n')
    return t


def mkdir(path):  # 创建文件夹
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        return False


def config():
    with open('config.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.find('番剧下载路径=') != -1:
                download_path = line.split('=')[1].replace('\n', '').replace('/', '\\') + '\\'
            if line.find('下载线程数 (尽量不要超过5)') != -1:
                try:
                    thread = int(line.split('=')[1].replace('\n', ''))
                except ValueError:
                    print('线程数必须为数字！')
                    return False
        if len(download_path) == 0:
            download_path = False
    with open('下载队列.txt', 'r', encoding='utf-8') as f:
        download_list = []
        lines = f.readlines()
        for line in lines:
            if line.find('https://www.ysjdm.net/') != -1:
                download_list.append(line.replace('\n', ''))
    return download_path, thread, download_list


def download(url, name):
    count = 0
    while 1:
        try:
            with open(name, 'wb') as f:
                f.write(requests.get(url, timeout=2).content)
                break
        except requests.exceptions.RequestException:
            count += 1
            print(f'{name} 下载失败，进行第 {count} 次重试')
    print(f'{name}下载完毕\n', end='')


def pa(url, i):
    global state, tt, all_tt, download_path
    if state == 0:
        while 1:
            try:
                ual = url + str(i)
                rest = requests.get(ual, timeout=2)
                rest.encoding = "utf-8"
                title = obj_title.search(rest.text).group("title").replace(":", "").replace("/", ""). \
                    replace('高清资源在线播放_新番 - 異世界動漫', '').replace(' ', '').replace('\\', '')
                name = obj_name.search(rest.text).group("name").replace(":", "").replace("/", ""). \
                    replace('高清资源在线播放_新番 - 異世界動漫', '').replace(' ', '').replace('\\', '')
                link = obj_link.search(rest.text).group("link").replace("\/", "/")
                film = first_dir + title  # 'E:\番\彩绿
                download_path = film
                if len(link) != 0:
                    if name.find("PV") == -1 and name.find("SP") == -1:
                        mkdir(film)
                        if len(name) >= 45:
                            name = "第" + name.split("第")[1]
                        video_file = film + '\\' + name  # 'E:\番\彩绿\彩绿第5集BD'
                        if ".m3u8" in link:
                            video_file = video_file + '.m3u8'
                        elif ".mp4" in link:
                            video_file = video_file + '.mp4'
                        download(link, video_file)
                        tt += 1
                    else:
                        print(f"{name}  这个是pv或者sp，不进行下载\n", end='')
                    all_tt += 1
                else:
                    state += 1
                rest.close()
                break
            except requests.exceptions.RequestException:
                pass


def change_url(url: str):  # 把用户输入的详情页链接转换成第一集的
    if url.find('detail') != -1:
        url = url.replace('detail', 'play').replace('.html', '') + '/sid/1/nid/1.html'
    return url


def launcher():
    print(f'视频下载路径为   {first_dir}\n下载线程为   {thread}')
    if len(download_lists) == 0:
        while 1:
            baseurl = input("\n---------在下方输入下载链接---------\n").strip()
            if len(baseurl) == 0:
                return
            t = set_t()
            main(baseurl, t)
            winsound.MessageBeep(100)
    else:
        global state
        for baseurl in download_lists:  # 队列下载
            t = 1
            state = 0
            main(baseurl, t)
        with open('下载队列.txt', 'w') as f:
            pass
        winsound.MessageBeep(100)
        i = input('队列全部下载完成！！！')


def main(baseurl, t):
    global tt, all_tt
    tt = 0
    all_tt = 0
    baseurl = change_url(baseurl)
    url = re.sub('/nid/.*', "/nid/", baseurl)  # 使用正则转换成普通ual
    with ThreadPoolExecutor(5) as f:
        for i in range(t, 40):
            f.submit(pa, url, i)
    # for i in range(t,40):
    #     pa(url,i)
    if tt != 0:
        print(f'\n获取文件完成一共 {tt}/{all_tt} 个视频\n即有 {all_tt - tt} 个 PV & SP')
        m3u8_downloader.main(download_path, thread)
    else:
        print('没有下载到内容，请检查输入链接是否正确！')


if __name__ == '__main__':
    download_path = ''
    config = config()
    first_dir, thread, download_lists = config[0], config[1], config[2]  # 从config文件中拿到 下载路径 , m3u8下载线程,下载列表

    state = 0
    all_tt = 0
    tt = 0  # 实际下载的视频数量
    if first_dir:
        launcher()
    else:
        input('请检查 config 里的 路径是否正确！！！')
