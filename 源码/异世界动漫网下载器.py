import os
import re
from concurrent.futures import ThreadPoolExecutor
import requests

obj_title = re.compile(r'<title>(?P<title>.*?)(S|第|P|O).*?</title>', re.S)
obj_name = re.compile(r'<title>(?P<name>.*?)</title>', re.S)
obj_link = re.compile(r'","link_pre":.*?,"url":"(?P<link>.*?)","url_next":"', re.S)


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
                download_path = line.split('=')[1].replace('\n', '').replace('\\', '/') + '/'
            if line.find('m3u8下载器路径=') != -1:
                downloader_path = line.split('=')[1].replace('\n', '').replace('\\', '/') + '/N_m3u8DL-CLI-SimpleG.exe'
        if len(download_path) == 0 or len(downloader_path) == 0:
            download_path = False
    return downloader_path, download_path


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
    global c, tt, all_tt
    if c == 0:
        ual = url + str(i)
        rest = requests.get(ual)
        rest.encoding = "utf-8"
        title = obj_title.search(rest.text).group("title"). \
            replace(":", "").replace("/", "").replace('高清资源在线播放_新番 - 異世界動漫', '').strip()
        name = obj_name.search(rest.text).group("name"). \
            replace(":", "").replace("/", "").replace('高清资源在线播放_新番 - 異世界動漫', '').strip()
        link = obj_link.search(rest.text).group("link").replace("\/", "/")
        film = first_dir + title  # 'E:/番/彩绿
        if len(link) != 0:
            if name.find("PV") == -1 and name.find("SP") == -1:
                mkdir(film)
                if len(name) >= 45:
                    name = "第" + name.split("第")[1]
                video_file = film + '/' + name  # 'E:/番/彩绿/彩绿第5集BD'
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
            c += 1
        rest.close()


if __name__ == '__main__':
    config = config()
    downloader_path, first_dir = config[0], config[1]  # 从config文件中拿到 下载器路径 和 m3u8下载路径
    if downloader_path and first_dir:
        m3u8_downloader = downloader_path
        print(f'm3u8下载路径为   {first_dir}\nm3u8下载器路径为   {m3u8_downloader}')
        while 1:
            baseual = input("---------在下方输入下载链接---------\n").strip()
            if len(baseual) == 0:
                break
            url = re.sub('/nid/.*', "/nid/", baseual)  # 使用正则转换成普通ual
            t = input("从第几集开始>>>")
            print('')
            if len(t) == 0:
                t = 1
            else:
                t = int(t)
            c = 0
            all_tt = 0
            tt = 0  # 实际下载的视频数量
            with ThreadPoolExecutor(10) as f:
                for i in range(t, 40):
                    f.submit(pa, url, i)
            # for i in range(t,40):
            #     pa(url,i)
            if all_tt != 0:
                os.startfile(first_dir)
                print(m3u8_downloader)
                os.startfile(m3u8_downloader)
                print(f'\n全部下载完成一共 {tt}/{all_tt} 个视频\n即有 {all_tt - tt} 个 PV & SP')
            else:
                print('没有下载到内容，请检查输入链接是否正确！')
    else:
        input('请检查 config 里的 路径是否正确！！！')
